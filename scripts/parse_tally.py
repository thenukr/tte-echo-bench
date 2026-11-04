"""Build per-section report templates and expert answer keys from the Tally echo findings form.

Inputs (both are raw outputs of the Tally MCP tools, saved as JSON):
  --form         output of `load_form`   ({"data": {...}, "context": {"ledger": "..."}})
  --submissions  output of `fetch_submissions` ({"data": {"questions": [...], "submissions": [...]}})

Outputs:
  <templates-dir>/<section>.json      empty forms the agent fills out
  <answers-dir>/<section>.json        expert answers, keyed by the same field/option slugs
  <answers-dir>/experts.json          anonymised expert ids -> submission metadata (no emails)
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tally_form import parse_logic, parse_questions  # noqa: E402

SECTIONS = {
    "Left Ventricle": "left_ventricle",
    "Interventricular Septum": "interventricular_septum",
    "Right Ventricle": "right_ventricle",
    "Left Atrium": "left_atrium",
    "Right Atrium": "right_atrium",
    "Interatrial Septum": "interatrial_septum",
    "Aortic Valve": "aortic_valve",
    "Mitral Valve": "mitral_valve",
    "Pulmonic Valve": "pulmonic_valve",
    "Tricuspid Valve": "tricuspid_valve",
    "Prosthetic Valves or Repaired Valves": "prosthetic_or_repaired_valves",
    "Pericardium": "pericardium",
    "Aorta": "aorta",
    "Pulmonary Artery": "pulmonary_artery",
    "Inferior Vena Cava": "inferior_vena_cava",
    "Extracardiac": "extracardiac",
}

INSTRUCTIONS = (
    "Fill in 'answer' for every field. 'single' fields take exactly one option (a string); "
    "'multi' fields take a list of every option that applies; 'text' fields take a short free-text string. "
    "A field with 'only_if' is only answered when its condition holds: each listed field's answer must "
    "include one of the listed options (all listed fields must match; for 'only_if_any', at least one "
    "entry must match). A field is also skipped when the field it depends on was itself skipped. "
    "Use null for skipped fields. Fields marked 'optional' may be left null (or [] for multi) even when shown. "
    "'cannot_evaluate' means the finding cannot be evaluated from the data provided."
)

# Standard options whose meaning is documented in INSTRUCTIONS instead of option_labels.
STANDARD = {"Cannot evaluate from present data": "cannot_evaluate"}

ACUITY = {
    "Routine — no special prioritization": "routine",
    "Significant — highlight in the summary; consider consultation or follow-up testing": "significant",
    "Urgent — clinical action within hours; direct notification of the care team": "urgent",
    "Critical — threat to life; immediate verbal notification (within minutes)": "critical",
    "Not applicable (finding absent or not evaluable)": "not_applicable",
}

OPTION_OVERRIDES = {
    **STANDARD,
    **ACUITY,
    "Cannot identify from present data": "cannot_identify",
    "Not determinable from present data": "not_determinable",
    ">70%": "over_70_pct",
    "Same brightness as heart muscle (isoechoic)": "isoechoic",
    "Prominent normal structure (Eustachian valve, Chiari network, crista terminalis)": "prominent_normal_structure",
    "Grade 1 (I)": "grade_1",
    "Grade 2 (II)": "grade_2",
    "Grade 3 (III)": "grade_3",
    "Less than 1.0 (net right-to-left)": "less_than_1_0",
    "Excessive (rocking, dehiscence)": "excessive",
    "Conduction abnormality (bundle branch block, pacing)": "conduction_abnormality",
}

# Section-name prefixes stripped from question titles when deriving field keys.
PREFIXES = [
    r"left ventricular", r"left ventricle", r"lv", r"right ventricular", r"right ventricle", r"rv",
    r"left atrial", r"left atrium", r"la", r"right atrial", r"right atrium", r"ra",
    r"interatrial septum", r"interatrial septal", r"atrial septal", r"aortic valve", r"mitral valve",
    r"pulmonic valve", r"tricuspid valve", r"prosthetic or repaired valve", r"aorta", r"aortic",
    r"pulmonary artery", r"inferior vena cava", r"extracardiac", r"ventricular septal",
]

# Explicit field keys (section_key, form title) -> field key, where the derived key is unclear or clashes.
FIELD_OVERRIDES = {
    ("left_ventricle", "Left ventricular mass"): "lv_mass_index",
    ("left_ventricle", "Left ventricular mass severity"): "lv_mass_index_severity",
    ("left_ventricle", "Left ventricular mass: acuity of finding"): "lv_mass_index_acuity",
    ("left_ventricle", "Intracavitary or myocardial masses: does this parameter need to be in the report?"): "intracavitary_mass_in_report",
    ("left_ventricle", "LV mass: suspected etiology (consistent with)"): "intracavitary_mass_etiology",
    ("left_ventricle", "LV mass: location"): "intracavitary_mass_location",
    ("left_ventricle", "LV mass: size (largest dimension)"): "intracavitary_mass_size",
    ("left_ventricle", "LV mass: echogenicity"): "intracavitary_mass_echogenicity",
    ("left_ventricle", "LV mass: shape and attachment"): "intracavitary_mass_shape",
    ("left_ventricle", "LV mass: describe 'Other'"): "intracavitary_mass_other_description",
    ("left_ventricle", "LV mass: mobility"): "intracavitary_mass_mobility",
    ("left_ventricle", "Left ventricle intracavitary or myocardial masses: acuity of finding"): "intracavitary_mass_acuity",
    ("left_ventricle", "Upper septal finding"): "upper_septal_morphology_finding",
    ("left_ventricle", "Upper septal morphology: hemodynamic consequence"): "upper_septal_morphology_hemodynamic_consequence",
    ("left_ventricle", "Aneurysm, pseudoaneurysm or diverticulum: does this parameter need to be in the report?"): "aneurysm_in_report",
    ("left_ventricle", "Aneurysm, pseudoaneurysm or diverticulum: type"): "aneurysm_type",
    ("left_ventricle", "Aneurysm, pseudoaneurysm or diverticulum: location"): "aneurysm_location",
    ("left_ventricle", "Aneurysm, pseudoaneurysm or diverticulum: size (largest dimension)"): "aneurysm_size",
    ("left_ventricle", "Aneurysm, pseudoaneurysm or diverticulum: associated thrombus or mass"): "aneurysm_associated_thrombus_or_mass",
    ("left_ventricle", "Aneurysm, pseudoaneurysm or diverticulum: acuity of finding"): "aneurysm_acuity",
    ("left_ventricle", "Obstructive lesion: peak gradient at rest (mmHg)"): "obstructive_lesion_peak_gradient_rest",
    ("left_ventricle", "Obstructive lesion: peak gradient with physiologic maneuver (mmHg)"): "obstructive_lesion_peak_gradient_maneuver",
    ("left_ventricle", "Regional wall motion abnormalities"): "rwma",
    ("left_ventricle", "Regional wall motion: walls involved (select all that apply)"): "rwma_walls",
    ("left_ventricle", "Regional wall motion abnormalities: acuity of finding"): "rwma_acuity",
    ("left_ventricle", "Obstructive lesions (dynamic or structural): does this parameter need to be in the report?"): "obstructive_lesion_in_report",
    ("left_ventricle", "Obstructive lesions: acuity of finding"): "obstructive_lesion_acuity",
    ("left_ventricle", "Myocardial strain: does this parameter need to be in the report?"): "strain_in_report",
    ("left_ventricle", "Global longitudinal strain value (GLS, %)"): "gls_value",
    ("left_ventricle", "Global longitudinal strain"): "gls",
    ("left_ventricle", "Myocardial strain: acuity of finding"): "strain_acuity",
    ("left_ventricle", "Diastolic function or LV relaxation"): "diastolic_function",
    ("left_ventricle", "Diastolic function or LV relaxation: acuity of finding"): "diastolic_function_acuity",
    ("left_ventricle", "Grade of LV diastolic dysfunction"): "diastolic_dysfunction_grade",
    ("left_ventricle", "Grade of LV diastolic dysfunction: acuity of finding"): "diastolic_dysfunction_grade_acuity",
    ("left_ventricle", "Ejection fraction"): "ef",
    ("left_ventricle", "Ejection fraction value"): "ef_value",
    ("left_ventricle", "Ejection fraction method (select all that apply)"): "ef_method",
    ("left_ventricle", "Ejection fraction: acuity of finding"): "ef_acuity",
    ("left_ventricle", "Apex: grade (select all that apply)"): "rwma_apex_grade",
    ("interventricular_septum", "Ventricular septal defect: does this parameter need to be in the report?"): "vsd_in_report",
    ("interventricular_septum", "Ventricular septal defect: type"): "vsd_type",
    ("interventricular_septum", "Ventricular septal defect: size"): "vsd_size",
    ("interventricular_septum", "Ventricular septal defect: number"): "vsd_number",
    ("interventricular_septum", "Ventricular septal defect: acuity of finding"): "vsd_acuity",
    ("interventricular_septum", "Ventricular septal shunt: does this parameter need to be in the report?"): "shunt_in_report",
    ("interventricular_septum", "Ventricular septal shunt: direction"): "shunt_direction",
    ("interventricular_septum", "Ventricular septal shunt: detection technique (select all that apply)"): "shunt_detection_technique",
    ("interventricular_septum", "Ventricular septal shunt: peak gradient across the defect (mmHg)"): "shunt_peak_gradient",
    ("interventricular_septum", "Ventricular septal shunt: acuity of finding"): "shunt_acuity",
    ("interventricular_septum", "Abnormal septal motion: reason or explanation"): "abnormal_septal_motion_reason",
    ("interventricular_septum", "Abnormal septal motion: reason or explanation: describe 'Other'"): "abnormal_septal_motion_reason_other_description",
    ("right_ventricle", "Intracavitary or myocardial masses: does this parameter need to be in the report?"): "intracavitary_mass_in_report",
    ("right_ventricle", "RV mass: suspected etiology (consistent with)"): "intracavitary_mass_etiology",
    ("right_ventricle", "RV mass: location"): "intracavitary_mass_location",
    ("right_ventricle", "RV mass: size (largest dimension)"): "intracavitary_mass_size",
    ("right_ventricle", "RV mass: echogenicity"): "intracavitary_mass_echogenicity",
    ("right_ventricle", "RV mass: shape and attachment"): "intracavitary_mass_shape",
    ("right_ventricle", "RV mass: describe 'Other'"): "intracavitary_mass_other_description",
    ("right_ventricle", "RV mass: mobility"): "intracavitary_mass_mobility",
    ("right_ventricle", "Right ventricle intracavitary or myocardial masses: acuity of finding"): "intracavitary_mass_acuity",
    ("right_ventricle", "Catheters or device leads: does this parameter need to be in the report?"): "catheter_or_lead_in_report",
    ("right_ventricle", "Catheter or device lead: type"): "catheter_or_lead_type",
    ("right_ventricle", "Catheter or device lead: type: describe 'Other'"): "catheter_or_lead_type_other_description",
    ("right_ventricle", "Catheter or device lead: location"): "catheter_or_lead_location",
    ("right_ventricle", "Catheter or device lead: location: describe 'Other'"): "catheter_or_lead_location_other_description",
    ("right_ventricle", "Catheter or device lead: associated masses"): "catheter_or_lead_associated_masses",
    ("right_ventricle", "Right ventricle catheters or device leads: acuity of finding"): "catheter_or_lead_acuity",
    ("right_ventricle", "Right ventricular regional wall motion abnormalities: does this parameter need to be in the report?"): "rwma_in_report",
    ("right_ventricle", "RV regional wall motion: walls involved (select all that apply)"): "rwma_walls",
    ("right_ventricle", "RV free wall: level (select all that apply)"): "rwma_free_wall_level",
    ("right_ventricle", "RV free wall: grade (select all that apply)"): "rwma_free_wall_grade",
    ("right_ventricle", "RV apex: grade (select all that apply)"): "rwma_apex_grade",
    ("right_ventricle", "Right ventricular regional wall motion abnormalities: acuity of finding"): "rwma_acuity",
    ("left_atrium", "Intracavitary masses: does this parameter need to be in the report?"): "intracavitary_mass_in_report",
    ("left_atrium", "LA mass: suspected etiology (consistent with)"): "intracavitary_mass_etiology",
    ("left_atrium", "LA mass: location"): "intracavitary_mass_location",
    ("left_atrium", "LA mass: size (largest dimension)"): "intracavitary_mass_size",
    ("left_atrium", "LA mass: echogenicity"): "intracavitary_mass_echogenicity",
    ("left_atrium", "LA mass: shape and attachment"): "intracavitary_mass_shape",
    ("left_atrium", "LA mass: describe 'Other'"): "intracavitary_mass_other_description",
    ("left_atrium", "LA mass: mobility"): "intracavitary_mass_mobility",
    ("left_atrium", "Left atrium intracavitary masses: acuity of finding"): "intracavitary_mass_acuity",
    ("left_atrium", "Left atrial appendage: intracavitary masses: does this parameter need to be in the report?"): "laa_mass_in_report",
    ("left_atrium", "Left atrial appendage mass: suspected etiology (consistent with)"): "laa_mass_etiology",
    ("left_atrium", "Left atrial appendage mass: location"): "laa_mass_location",
    ("left_atrium", "Left atrial appendage mass: size (largest dimension)"): "laa_mass_size",
    ("left_atrium", "Left atrial appendage mass: echogenicity"): "laa_mass_echogenicity",
    ("left_atrium", "Left atrial appendage mass: shape and attachment"): "laa_mass_shape",
    ("left_atrium", "Left atrial appendage mass: mobility"): "laa_mass_mobility",
    ("left_atrium", "Left atrial appendage mass: describe 'Other'"): "laa_mass_other_description",
    ("left_atrium", "Left atrial appendage intracavitary masses: acuity of finding"): "laa_mass_acuity",
    ("left_atrium", "Left atrial appendage: spontaneous echo contrast: does this parameter need to be in the report?"): "laa_sec_in_report",
    ("left_atrium", "Left atrial appendage: spontaneous echo contrast grade"): "laa_sec_grade",
    ("left_atrium", "Left atrial appendage spontaneous echo contrast: acuity of finding"): "laa_sec_acuity",
    ("left_atrium", "Left atrial appendage: devices: does this parameter need to be in the report?"): "laa_device_in_report",
    ("left_atrium", "Left atrial appendage device: type"): "laa_device_type",
    ("left_atrium", "Left atrial appendage device: size (mm)"): "laa_device_size",
    ("left_atrium", "Left atrial appendage device: type: describe 'Other'"): "laa_device_type_other_description",
    ("left_atrium", "Left atrial appendage device: pathologic findings (select all that apply)"): "laa_device_pathologic_findings",
    ("left_atrium", "Left atrial appendage devices: acuity of finding"): "laa_device_acuity",
    ("left_atrium", "Left atrial strain: does this parameter need to be in the report?"): "strain_in_report",
    ("left_atrium", "Left atrial strain"): "strain",
    ("left_atrium", "Left atrial reservoir strain value (%)"): "reservoir_strain_value",
    ("left_atrium", "Left atrial strain: acuity of finding"): "strain_acuity",
    ("right_atrium", "Intracavitary masses: does this parameter need to be in the report?"): "intracavitary_mass_in_report",
    ("right_atrium", "RA mass: suspected etiology (consistent with)"): "intracavitary_mass_etiology",
    ("right_atrium", "RA mass: location"): "intracavitary_mass_location",
    ("right_atrium", "RA mass: size (largest dimension)"): "intracavitary_mass_size",
    ("right_atrium", "RA mass: echogenicity"): "intracavitary_mass_echogenicity",
    ("right_atrium", "RA mass: shape and attachment"): "intracavitary_mass_shape",
    ("right_atrium", "RA mass: describe 'Other'"): "intracavitary_mass_other_description",
    ("right_atrium", "RA mass: mobility"): "intracavitary_mass_mobility",
    ("right_atrium", "Right atrium intracavitary masses: acuity of finding"): "intracavitary_mass_acuity",
    ("right_atrium", "Spontaneous echo contrast: does this parameter need to be in the report?"): "sec_in_report",
    ("right_atrium", "Right atrial spontaneous echo contrast grade"): "sec_grade",
    ("right_atrium", "Right atrium spontaneous echo contrast: acuity of finding"): "sec_acuity",
    ("right_atrium", "Catheters or device leads: does this parameter need to be in the report?"): "catheter_or_lead_in_report",
    ("right_atrium", "Right atrial catheter or device lead: type"): "catheter_or_lead_type",
    ("right_atrium", "Right atrial catheter or device lead: type: describe 'Other'"): "catheter_or_lead_type_other_description",
    ("right_atrium", "Right atrial catheter or device lead: location"): "catheter_or_lead_location",
    ("right_atrium", "Right atrial catheter or device lead: location: describe 'Other'"): "catheter_or_lead_location_other_description",
    ("right_atrium", "Right atrial catheter or device lead: associated masses"): "catheter_or_lead_associated_masses",
    ("right_atrium", "Right atrium catheters or device leads: acuity of finding"): "catheter_or_lead_acuity",
    ("interatrial_septum", "Structural abnormalities"): "structure",
    ("interatrial_septum", "Interatrial septum: abnormality (select all that apply)"): "structural_abnormality",
    ("interatrial_septum", "Interatrial septum: bowing direction"): "bowing_direction",
    ("interatrial_septum", "Atrial septal defect: type"): "asd_type",
    ("interatrial_septum", "Interatrial septal communications: does this parameter need to be in the report?"): "communication_in_report",
    ("interatrial_septum", "Interatrial septal communication"): "communication",
    ("interatrial_septum", "Interatrial septal communication: type"): "communication_type",
    ("interatrial_septum", "Interatrial septal communication: size (largest dimension)"): "communication_size",
    ("interatrial_septum", "Interatrial septal communication: type: describe 'Other'"): "communication_type_other_description",
    ("interatrial_septum", "Interatrial septal communications: acuity of finding"): "communication_acuity",
    ("interatrial_septum", "Interatrial septal devices: does this parameter need to be in the report?"): "device_in_report",
    ("interatrial_septum", "Atrial septal device: type"): "device_type",
    ("interatrial_septum", "Atrial septal device: size (mm)"): "device_size",
    ("interatrial_septum", "Atrial septal device: type: describe 'Other'"): "device_type_other_description",
    ("interatrial_septum", "Atrial septal device: pathologic findings (select all that apply)"): "device_pathologic_findings",
    ("interatrial_septum", "Interatrial septal devices: acuity of finding"): "device_acuity",
    ("interatrial_septum", "Interatrial shunt: does this parameter need to be in the report?"): "shunt_in_report",
    ("interatrial_septum", "Interatrial shunt: direction"): "shunt_direction",
    ("interatrial_septum", "Interatrial shunt: location"): "shunt_location",
    ("interatrial_septum", "Interatrial shunt: detection technique (select all that apply)"): "shunt_detection_technique",
    ("interatrial_septum", "Interatrial shunt: Qp:Qs"): "shunt_qp_qs",
    ("interatrial_septum", "Interatrial shunt: acuity of finding"): "shunt_acuity",
    ("aortic_valve", "Aortic valve structure"): "structure",
    ("aortic_valve", "Aortic valve: number of leaflets"): "number_of_leaflets",
    ("aortic_valve", "Bicuspid aortic valve: type"): "bicuspid_type",
    ("aortic_valve", "Aortic stenosis: does this parameter need to be in the report?"): "stenosis_in_report",
    ("aortic_valve", "Aortic stenosis severity"): "stenosis_severity",
    ("aortic_valve", "Aortic stenosis: mechanism"): "stenosis_mechanism",
    ("aortic_valve", "Aortic stenosis: mechanism: describe 'Other'"): "stenosis_mechanism_other_description",
    ("aortic_valve", "Aortic stenosis: acuity of finding"): "stenosis_acuity",
    ("aortic_valve", "Aortic regurgitation"): "regurgitation",
    ("aortic_valve", "Aortic regurgitation severity"): "regurgitation_severity",
    ("aortic_valve", "Aortic regurgitation: mechanism"): "regurgitation_mechanism",
    ("aortic_valve", "Aortic regurgitation: mechanism: describe 'Other'"): "regurgitation_mechanism_other_description",
    ("aortic_valve", "Aortic regurgitation: acuity of finding"): "regurgitation_acuity",
    ("mitral_valve", "Mitral valve structure"): "structure",
    ("mitral_valve", "Mitral stenosis: does this parameter need to be in the report?"): "stenosis_in_report",
    ("mitral_valve", "Mitral stenosis severity"): "stenosis_severity",
    ("mitral_valve", "Mitral stenosis: mechanism"): "stenosis_mechanism",
    ("mitral_valve", "Mitral stenosis: mechanism: describe 'Other'"): "stenosis_mechanism_other_description",
    ("mitral_valve", "Mitral stenosis: acuity of finding"): "stenosis_acuity",
    ("mitral_valve", "Mitral regurgitation"): "regurgitation",
    ("mitral_valve", "Mitral regurgitation severity"): "regurgitation_severity",
    ("mitral_valve", "Mitral regurgitation: mechanism"): "regurgitation_mechanism",
    ("mitral_valve", "Mitral regurgitation: mechanism: describe 'Other'"): "regurgitation_mechanism_other_description",
    ("mitral_valve", "Mitral regurgitation: acuity of finding"): "regurgitation_acuity",
    ("pulmonic_valve", "Pulmonic valve structure"): "structure",
    ("pulmonic_valve", "Pulmonic stenosis"): "stenosis",
    ("pulmonic_valve", "Pulmonic stenosis severity"): "stenosis_severity",
    ("pulmonic_valve", "Pulmonic stenosis: acuity of finding"): "stenosis_acuity",
    ("pulmonic_valve", "Pulmonic regurgitation"): "regurgitation",
    ("pulmonic_valve", "Pulmonic regurgitation severity"): "regurgitation_severity",
    ("pulmonic_valve", "Pulmonic regurgitation: acuity of finding"): "regurgitation_acuity",
    ("tricuspid_valve", "Tricuspid valve structure"): "structure",
    ("tricuspid_valve", "Tricuspid valve: number of leaflets"): "number_of_leaflets",
    ("tricuspid_valve", "Tricuspid stenosis"): "stenosis",
    ("tricuspid_valve", "Tricuspid stenosis: acuity of finding"): "stenosis_acuity",
    ("tricuspid_valve", "Tricuspid regurgitation"): "regurgitation",
    ("tricuspid_valve", "Tricuspid regurgitation severity"): "regurgitation_severity",
    ("tricuspid_valve", "Tricuspid regurgitation: acuity of finding"): "regurgitation_acuity",
    ("tricuspid_valve", "Right ventricular systolic pressure"): "rvsp",
    ("tricuspid_valve", "Right ventricular systolic pressure: acuity of finding"): "rvsp_acuity",
    ("prosthetic_or_repaired_valves", "Prosthetic or repaired valve: does this parameter need to be in the report?"): "in_report",
    ("prosthetic_or_repaired_valves", "Prosthetic valve motion"): "motion",
    ("prosthetic_or_repaired_valves", "Prosthetic or repaired valve regurgitation severity"): "regurgitation_severity",
    ("prosthetic_or_repaired_valves", "Prosthetic or repaired valve: acuity of finding"): "acuity",
    ("pericardium", "Pericardium"): "structure",
    ("pericardium", "Pericardial abnormality (select all that apply)"): "structural_abnormality",
    ("pericardium", "Pericardial abnormality: describe 'Other'"): "structural_abnormality_other_description",
    ("pericardium", "Pericardial abnormalities: acuity of finding"): "structure_acuity",
    ("pericardium", "Pericardial effusion: acuity of finding"): "effusion_acuity",
    ("pericardium", "Tamponade physiology or constriction: acuity of finding"): "tamponade_or_constriction_acuity",
    ("pericardium", "Pericardial effusion"): "effusion",
    ("pericardium", "Pericardial effusion size"): "effusion_size",
    ("pericardium", "Pericardial effusion: measurement (cm)"): "effusion_measurement",
    ("pericardium", "Pericardial effusion location"): "effusion_location",
    ("pericardium", "Pericardial effusion content or appearance"): "effusion_content",
    ("pericardium", "Tamponade physiology or constriction"): "tamponade_or_constriction",
    ("pericardium", "Supporting findings (select all that apply)"): "tamponade_or_constriction_supporting_findings",
    ("aorta", "Aortic size"): "size",
    ("aorta", "Aortic size severity"): "size_severity",
    ("pulmonary_artery", "Pulmonary artery size: does this parameter need to be in the report?"): "size_in_report",
    ("pulmonary_artery", "Pulmonary artery other abnormalities: does this parameter need to be in the report?"): "abnormality_in_report",
    ("pulmonary_artery", "Pulmonary artery other abnormalities: acuity of finding"): "abnormality_acuity",
    ("inferior_vena_cava", "Inferior vena cava size"): "size",
    ("inferior_vena_cava", "Inferior vena cava respiratory change"): "respiratory_change",
    ("inferior_vena_cava", "Estimated right atrial pressure"): "estimated_ra_pressure",
    ("inferior_vena_cava", "Inferior vena cava size and right atrial pressure: acuity of finding"): "size_and_ra_pressure_acuity",
    ("inferior_vena_cava", "Inferior vena cava masses or devices: does this parameter need to be in the report?"): "mass_or_device_in_report",
    ("inferior_vena_cava", "Inferior vena cava masses or devices: acuity of finding"): "mass_or_device_acuity",
    ("extracardiac", "Extracardiac abnormalities: does this parameter need to be in the report?"): "abnormality_in_report",
    ("extracardiac", "Extracardiac abnormalities: acuity of finding"): "abnormality_acuity",
}

# Dropdowns whose title says "(select all that apply)" are multi-select for the agent.
MULTI_DROPDOWNS = {"Aorta: abnormality location (select all that apply)",
                   "Pulmonary artery: abnormality location (select all that apply)"}


def slug(text: str) -> str:
    s = text.lower().replace("&", "and").replace("−", "minus ").replace("–", "-").replace(">", "over ")
    s = s.replace("%", " pct ").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def option_slug(label: str) -> str:
    if label in OPTION_OVERRIDES:
        return OPTION_OVERRIDES[label]
    label = re.sub(r"\s*\(e\.g\..*?\)", "", label)  # drop "(e.g. ...)" example lists
    return slug(label)


def field_key(section: str, title: str) -> str:
    if (section, title) in FIELD_OVERRIDES:
        return FIELD_OVERRIDES[(section, title)]
    t = title.replace("(select all that apply)", "").strip()
    t = t.replace(": does this parameter need to be in the report?", " in report")
    t = t.replace(": acuity of finding", " acuity").replace("describe 'Other'", "other description")
    k = slug(t)
    for p in PREFIXES:
        p = slug(p)
        if k.startswith(p + "_") and len(k) > len(p) + 1:
            k = k[len(p) + 1:]
            break
    return k


def labels_differ(label: str, s: str) -> bool:
    return label not in STANDARD and slug(label) != s


def build(form_path: Path, subs_path: Path):
    ledger = json.loads(form_path.read_text())["context"]["ledger"]
    questions = [q for q in parse_questions(ledger) if q["section"]]
    rules = parse_logic(ledger)
    by_uuid = {q["uuid"]: q for q in questions}

    # Assign section/field keys and option slugs.
    for q in questions:
        q["skey"] = SECTIONS[q["section"]]
        q["key"] = field_key(q["skey"], q["title"])
        q["slugs"] = [option_slug(o) for o in q["options"]]
        if len(set(q["slugs"])) != len(q["slugs"]):
            raise ValueError(f"duplicate option slugs in {q['title']}: {q['slugs']}")
        if q["kind"] == "checkboxes" or q["title"] in MULTI_DROPDOWNS:
            q["type"] = "multi"
        elif q["kind"] in ("dropdown", "multiple_choice"):
            q["type"] = "single"
        elif q["kind"] == "text":
            q["type"] = "text"
        else:
            raise ValueError(f"unhandled kind {q['kind']} for {q['title']}")
    unused = set(FIELD_OVERRIDES) - {(q["skey"], q["title"]) for q in questions}
    if unused:
        raise ValueError(f"FIELD_OVERRIDES entries match no question: {sorted(unused)}")
    seen = {}
    for q in questions:
        k = (q["skey"], q["key"])
        if k in seen:
            raise ValueError(f"duplicate field key {k}: {seen[k]!r} / {q['title']!r}")
        seen[k] = q["title"]

    # Visibility conditions from SHOW rules (a question may be shown by several rules -> OR of rules).
    cond = {}
    for r in rules:
        clauses = []
        for q_uuid, _op, opt_uuids in r["when"]:
            src = by_uuid[q_uuid]
            vals = [src["slugs"][src["option_uuids"].index(o)] for o in opt_uuids]
            clauses.append((src, vals))
        for target in r["show"]:
            t = by_uuid[target]
            for src, _ in clauses:
                if src["skey"] != t["skey"]:
                    raise ValueError(f"cross-section dependency: {src['title']} -> {t['title']}")
            cond.setdefault(target, []).append((r["join"], clauses))
    for q in questions:
        if q["hidden"] and q["uuid"] not in cond:
            raise ValueError(f"hidden question with no SHOW rule: {q['title']}")
        if not q["hidden"] and q["uuid"] in cond:
            raise ValueError(f"visible question targeted by SHOW rule: {q['title']}")

    def only_if(q):
        """Template representation of the visibility condition."""
        rs = cond.get(q["uuid"])
        if not rs:
            return {}
        if len(rs) != 1:
            raise ValueError(f"multiple SHOW rules for {q['title']}")
        join, clauses = rs[0]
        render = lambda vals: vals[0] if len(vals) == 1 else vals  # noqa: E731
        if join == "AND" or len(clauses) == 1:
            return {"only_if": {src["key"]: render(v) for src, v in clauses}}
        return {"only_if_any": [{src["key"]: render(v)} for src, v in clauses]}

    def visible(q, ans):
        rs = cond.get(q["uuid"])
        if not rs:
            return True
        for join, clauses in rs:
            hits = []
            for src, vals in clauses:
                a = ans.get(src["uuid"])
                a = a if isinstance(a, list) else ([a] if a else [])
                a = [src["slugs"][src["options"].index(x)] for x in a if x in src["options"]]
                hits.append(visible(src, ans) and any(v in a for v in vals))
            if (any(hits) if join == "OR" else all(hits)):
                return True
        return False

    # Templates.
    templates = {}
    for q in questions:
        sec = templates.setdefault(q["skey"], {"section": q["skey"], "title": q["section"],
                                               "instructions": INSTRUCTIONS, "fields": {}})
        f = {"question": q["title"].replace(" (select all that apply)", "")
             + (" (select all that apply)" if q["type"] == "multi" else ""),
             "type": q["type"]}
        if q["subsection"]:
            f["subsection"] = q["subsection"]
        if q["help"] and not q["help"].lower().startswith("optional"):
            f["help"] = q["help"]
        if q["optional"]:
            f["optional"] = True
        if q["type"] != "text":
            f["options"] = q["slugs"]
            extra = {s: o for s, o in zip(q["slugs"], q["options"]) if labels_differ(o, s)}
            if extra:
                f["option_labels"] = extra
        f.update(only_if(q))
        f["answer"] = [] if q["type"] == "multi" else None
        sec["fields"][q["key"]] = f

    # Expert answers.
    subs = json.loads(subs_path.read_text())["data"]
    all_q = parse_questions(ledger)
    if [sq["label"].strip() for sq in subs["questions"]] != [q["title"] for q in all_q]:
        raise ValueError("submission questions do not line up with form questions")
    qid_to_uuid = {sq["id"]: q["uuid"] for sq, q in zip(subs["questions"], all_q)}
    ordered = sorted(subs["submissions"], key=lambda s: s["submittedAt"])
    experts, answers = {}, {k: {"section": k, "experts": [], "fields": {}} for k in templates}
    for i, sub in enumerate(ordered, 1):
        eid = f"expert_{i}"
        experts[eid] = {"submission_id": sub["id"], "submitted_at": sub["submittedAt"],
                        "completed": sub["isCompleted"]}
        raw = {}
        for r in sub["responses"]:
            a = r["answer"]
            a = [x.strip() for x in a] if isinstance(a, list) else (a.strip() if isinstance(a, str) else a)
            raw[qid_to_uuid[r["questionId"]]] = a
        for sec in answers.values():
            sec["experts"].append(eid)
        for q in questions:
            a = raw.get(q["uuid"])
            shown = visible(q, raw)
            if a not in (None, "", []) and not shown:
                raise ValueError(f"{eid}: answer to hidden question {q['title']}")
            if not shown:
                val = None
            elif q["type"] == "text":
                val = a or ""
            else:
                vals = a if isinstance(a, list) else ([a] if a else [])
                for v in vals:
                    if v not in q["options"]:
                        raise ValueError(f"{eid}: unknown option {v!r} for {q['title']}")
                val = [q["slugs"][q["options"].index(v)] for v in vals]
            fa = answers[q["skey"]]["fields"].setdefault(q["key"], {"type": q["type"], "answers": {}})
            fa["answers"][eid] = val
    return templates, answers, experts


def condition_met(field, filled, skipped):
    """Evaluate a template field's only_if / only_if_any against already-filled answers."""
    def clause(cond):
        for key, want in cond.items():
            if key in skipped:
                return False
            want = want if isinstance(want, list) else [want]
            got = filled.get(key)
            got = got if isinstance(got, list) else ([got] if got else [])
            if not any(w in got for w in want):
                return False
        return True
    if "only_if" in field:
        return clause(field["only_if"])
    if "only_if_any" in field:
        return any(clause(c) for c in field["only_if_any"])
    return True


def consensus_report(template, answer_key):
    """Oracle report: per field, the option accepted by the most experts (ties -> form order); for multi
    fields, options picked by at least half of the experts shown the field. Only used to smoke-test the task."""
    out = json.loads(json.dumps(template))
    filled, skipped = {}, set()
    for key, f in out["fields"].items():
        if not condition_met(f, filled, skipped):
            f["answer"] = None
            skipped.add(key)
            continue
        votes = [v for v in answer_key["fields"][key]["answers"].values() if v is not None]
        if f["type"] == "text":
            f["answer"] = next((v for v in votes if v), None)
        elif f["type"] == "single":
            counts = {o: sum(o in v for v in votes) for o in f["options"]}
            best = max(f["options"], key=lambda o: (counts[o], -f["options"].index(o)))
            f["answer"] = best if counts[best] else (None if f.get("optional") else
                                                     ("cannot_evaluate" if "cannot_evaluate" in f["options"] else f["options"][0]))
        else:
            f["answer"] = [o for o in f["options"] if votes and sum(o in v for v in votes) * 2 >= len(votes)]
        filled[key] = f["answer"]
    return out


ANSWER_NOTE = (
    "Expert answers per field. For 'single' fields each expert lists every option they would accept as "
    "correct (an accepted range). For 'multi' fields each expert lists the set they selected. "
    "null = field not shown to that expert (its only_if condition was not met); [] or \"\" = shown but left blank "
    "(only possible for optional questions)."
)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--form", required=True, type=Path)
    ap.add_argument("--submissions", required=True, type=Path)
    ap.add_argument("--templates-dir", required=True, type=Path)
    ap.add_argument("--answers-dir", required=True, type=Path)
    ap.add_argument("--solution-dir", type=Path, help="also write an expert-consensus oracle report here")
    args = ap.parse_args()

    templates, answers, experts = build(args.form, args.submissions)
    args.templates_dir.mkdir(parents=True, exist_ok=True)
    args.answers_dir.mkdir(parents=True, exist_ok=True)
    for k, t in templates.items():
        (args.templates_dir / f"{k}.json").write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n")
        a = {"section": k, "note": ANSWER_NOTE, **{x: y for x, y in answers[k].items() if x != "section"}}
        (args.answers_dir / f"{k}.json").write_text(json.dumps(a, indent=2, ensure_ascii=False) + "\n")
    if args.solution_dir:
        args.solution_dir.mkdir(parents=True, exist_ok=True)
        for k, t in templates.items():
            key = {"fields": answers[k]["fields"]}
            (args.solution_dir / f"{k}.json").write_text(
                json.dumps(consensus_report(t, key), indent=2, ensure_ascii=False) + "\n")
    (args.answers_dir / "experts.json").write_text(json.dumps(experts, indent=2) + "\n")
    print(f"wrote {len(templates)} sections, {sum(len(t['fields']) for t in templates.values())} fields, "
          f"{len(experts)} experts")


if __name__ == "__main__":
    main()
