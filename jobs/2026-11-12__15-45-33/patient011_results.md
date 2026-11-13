# patient011: 10 Codex rollouts (gpt-6-astra, xhigh)

Job `2026-11-12__15-45-33`, 10 rollouts. Reward 1 means the form has a complete 341-column answer row; it is **not** scored against expert answers.

## Runs

| Rollout | Reward | Agent time | Cost (USD) | Input tokens | Output tokens | Answered fields |
|---|---|---|---|---|---|---|
| 6g3k6Vo | 1 | 0:07:06 | $4.85 | 2,191,284 | 11,841 | 131 |
| 7pcgsZy | 1 | 0:08:17 | $5.82 | 2,864,369 | 14,053 | 131 |
| 8ody48c | 1 | 0:07:49 | $5.50 | 2,763,913 | 13,864 | 131 |
| bieHtnH | 1 | 0:06:35 | $4.48 | 2,009,549 | 11,132 | 131 |
| DGpgyMP | 1 | 0:05:56 | $4.43 | 2,020,545 | 11,403 | 131 |
| F956WBx | 1 | 0:06:08 | $4.13 | 1,810,170 | 10,983 | 131 |
| fQXmcKb | 1 | 0:07:45 | $4.34 | 1,916,399 | 13,402 | 129 |
| kPPprtq | 1 | 0:09:06 | $5.72 | 2,660,443 | 15,984 | 131 |
| tRWcREA | 1 | 0:07:18 | $4.50 | 2,040,181 | 13,281 | 131 |
| vah4DWT | 1 | 0:07:06 | $4.79 | 2,321,831 | 11,912 | 131 |
| **Total** | | | **$48.56** | 22,598,684 | 127,855 | |

## Agreement across runs

- Fields answered in at least one run: **131** of 341
- All 10 runs gave the identical answer: **100**
- Runs disagreed: **31**
- Left blank in every run (condition not met): **210**

### Most split fields (lowest top-answer share)

| Field | Section | Top answer | Share | Distinct answers |
|---|---|---|---|---|
| Mitral regurgitation severity | Mitral Valve | Trivial | 6/10 | 2 |
| Inferior vena cava respiratory change | Inferior Vena Cava | Not assessable | 6/10 | 2 |
| Estimated right atrial pressure | Inferior Vena Cava | Not estimable | 6/10 | 2 |
| Wall thickness (2) | Right Ventricle | Cannot evaluate from present data | 7/10 | 2 |
| Right ventricle wall thickness: acuity of finding | Right Ventricle | Not applicable (finding absent or not evaluable) | 7/10 | 2 |
| Left ventricular mass: acuity of finding | Left Ventricle | Routine — no special prioritization | 8/10 | 2 |
| Interatrial septum structural abnormalities: acuity of finding | Interatrial Septum | Not applicable (finding absent or not evaluable) | 8/10 | 2 |
| Pulmonic regurgitation | Pulmonic Valve | Present | 8/10 | 2 |
| Pulmonic regurgitation severity | Pulmonic Valve | Trivial | 8/10 | 2 |
| Pulmonic regurgitation: acuity of finding | Pulmonic Valve | Routine — no special prioritization | 8/10 | 2 |
| Inferior vena cava size and right atrial pressure: acuity of finding | Inferior Vena Cava | Routine — no special prioritization | 8/10 | 2 |
| Left ventricle size: acuity of finding | Left Ventricle | Routine — no special prioritization | 9/10 | 2 |
| Left ventricular mass | Left Ventricle | Normal | 9/10 | 2 |
| Left ventricular mass severity | Left Ventricle | Not applicable | 9/10 | 2 |
| Left ventricle global systolic function: acuity of finding | Left Ventricle | Routine — no special prioritization | 9/10 | 2 |
| Ejection fraction value | Left Ventricle | 60-65% | 9/10 | 2 |
| Ejection fraction: acuity of finding | Left Ventricle | Routine — no special prioritization | 9/10 | 2 |
| Diastolic function or LV relaxation | Left Ventricle | Abnormal (impaired) | 9/10 | 2 |
| Diastolic function or LV relaxation: acuity of finding | Left Ventricle | Routine — no special prioritization | 9/10 | 2 |
| Grade of LV diastolic dysfunction | Left Ventricle | Cannot evaluate from present data | 9/10 | 2 |
| Grade of LV diastolic dysfunction: acuity of finding | Left Ventricle | Not applicable (finding absent or not evaluable) | 9/10 | 2 |
| Right ventricle size: acuity of finding | Right Ventricle | Routine — no special prioritization | 9/10 | 2 |
| Right ventricle global systolic function: acuity of finding | Right Ventricle | Routine — no special prioritization | 9/10 | 2 |
| Left atrium size: acuity of finding | Left Atrium | Routine — no special prioritization | 9/10 | 2 |
| Right atrium size: acuity of finding | Right Atrium | Routine — no special prioritization | 9/10 | 2 |

## Answer histograms by field

Each bar is out of 10 runs. `(blank)` = left empty. For select-all-that-apply fields, the per-option counts (how many runs included that option) follow the whole-answer counts.

### Left Ventricle

**Size**
```
Normal  ██████████ 10
```

**Size Severity**
```
Not applicable  ██████████ 10
```

**Left ventricle size: acuity of finding**
```
Routine — no special prioritization               █████████░ 9
Not applicable (finding absent or not evaluable)  █░░░░░░░░░ 1
```

**Wall thickness**
```
Increased  ██████████ 10
```

**Wall thickness severity**
```
Mild  ██████████ 10
```

**Left ventricle wall thickness: acuity of finding**
```
Routine — no special prioritization  ██████████ 10
```

**Left ventricular mass**
```
Normal                             █████████░ 9
Cannot evaluate from present data  █░░░░░░░░░ 1
```

**Left ventricular mass severity**
```
Not applicable                     █████████░ 9
Cannot evaluate from present data  █░░░░░░░░░ 1
```

**Left ventricular mass: acuity of finding**
```
Routine — no special prioritization               ████████░░ 8
Not applicable (finding absent or not evaluable)  ██░░░░░░░░ 2
```

**Intracavitary or myocardial masses: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Left ventricular upper septal morphology: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Aneurysm, pseudoaneurysm or diverticulum: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Global systolic function**
```
Normal  ██████████ 10
```

**Global systolic function severity**
```
Not applicable  ██████████ 10
```

**Left ventricle global systolic function: acuity of finding**
```
Routine — no special prioritization               █████████░ 9
Not applicable (finding absent or not evaluable)  █░░░░░░░░░ 1
```

**Ejection fraction**
```
Normal  ██████████ 10
```

**Ejection fraction value**
```
60-65%  █████████░ 9
55-60%  █░░░░░░░░░ 1
```

**Ejection fraction method (select all that apply)** _(select all)_
```
Visual  ██████████ 10
-- per option --
Visual  ██████████ 10
```

**Ejection fraction: acuity of finding**
```
Routine — no special prioritization               █████████░ 9
Not applicable (finding absent or not evaluable)  █░░░░░░░░░ 1
```

**Regional wall motion abnormalities**
```
Absent  ██████████ 10
```

**Regional wall motion abnormalities: acuity of finding**
```
Not applicable (finding absent or not evaluable)  ██████████ 10
```

**Obstructive lesions (dynamic or structural): does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Myocardial strain: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Diastolic function or LV relaxation**
```
Abnormal (impaired)  █████████░ 9
Indeterminate        █░░░░░░░░░ 1
```

**Diastolic function or LV relaxation: acuity of finding**
```
Routine — no special prioritization               █████████░ 9
Not applicable (finding absent or not evaluable)  █░░░░░░░░░ 1
```

**Filling pressures**
```
Indeterminate  ██████████ 10
```

**Filling pressures refer to**
```
Left atrial pressure  ██████████ 10
```

**Filling pressures: acuity of finding**
```
Not applicable (finding absent or not evaluable)  ██████████ 10
```

**Grade of LV diastolic dysfunction** _(conditional)_
```
Cannot evaluate from present data  █████████░ 9
(blank)                            █░░░░░░░░░ 1
```

**Grade of LV diastolic dysfunction: acuity of finding** _(conditional)_
```
Not applicable (finding absent or not evaluable)  █████████░ 9
(blank)                                           █░░░░░░░░░ 1
```

### Interventricular Septum

**Ventricular septal defect: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Abnormal septal motion: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Ventricular septal shunt: does this parameter need to be in the report?**
```
No  ██████████ 10
```

### Right Ventricle

**Size (2)**
```
Normal  ██████████ 10
```

**Size severity**
```
Not applicable  ██████████ 10
```

**Right ventricle size: acuity of finding**
```
Routine — no special prioritization               █████████░ 9
Not applicable (finding absent or not evaluable)  █░░░░░░░░░ 1
```

**Wall thickness (2)**
```
Cannot evaluate from present data  ███████░░░ 7
Normal                             ███░░░░░░░ 3
```

**Right ventricle wall thickness: acuity of finding**
```
Not applicable (finding absent or not evaluable)  ███████░░░ 7
Routine — no special prioritization               ███░░░░░░░ 3
```

**Intracavitary or myocardial masses: does this parameter need to be in the report? (2)**
```
No  ██████████ 10
```

**Catheters or device leads: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Global systolic function (2)**
```
Normal  ██████████ 10
```

**Global systolic function severity (2)**
```
Not applicable  ██████████ 10
```

**Right ventricle global systolic function: acuity of finding**
```
Routine — no special prioritization               █████████░ 9
Not applicable (finding absent or not evaluable)  █░░░░░░░░░ 1
```

**Right ventricular regional wall motion abnormalities: does this parameter need to be in the report?**
```
No  ██████████ 10
```

### Left Atrium

**Size (3)**
```
Normal  ██████████ 10
```

**Size severity (2)**
```
Not applicable  ██████████ 10
```

**Left atrium size: acuity of finding**
```
Routine — no special prioritization               █████████░ 9
Not applicable (finding absent or not evaluable)  █░░░░░░░░░ 1
```

**Intracavitary masses: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Left atrial appendage: intracavitary masses: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Left atrial appendage: spontaneous echo contrast: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Left atrial appendage: devices: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Pulmonary vein flow pattern: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Left atrial strain: does this parameter need to be in the report?**
```
No  ██████████ 10
```

### Right Atrium

**Size (4)**
```
Normal  ██████████ 10
```

**Size severity (3)**
```
Not applicable  ██████████ 10
```

**Right atrium size: acuity of finding**
```
Routine — no special prioritization               █████████░ 9
Not applicable (finding absent or not evaluable)  █░░░░░░░░░ 1
```

**Intracavitary masses: does this parameter need to be in the report? (2)**
```
No  ██████████ 10
```

**Spontaneous echo contrast: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Catheters or device leads: does this parameter need to be in the report? (2)**
```
No  ██████████ 10
```

### Interatrial Septum

**Structural abnormalities**
```
Normal (intact)                    █████████░ 9
Cannot evaluate from present data  █░░░░░░░░░ 1
```

**Interatrial septum structural abnormalities: acuity of finding**
```
Not applicable (finding absent or not evaluable)  ████████░░ 8
Routine — no special prioritization               ██░░░░░░░░ 2
```

**Interatrial septal communications: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Interatrial septal devices: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Interatrial shunt: does this parameter need to be in the report?**
```
No  ██████████ 10
```

### Aortic Valve

**Aortic valve structure**
```
Structurally normal  ██████████ 10
```

**Aortic valve: number of leaflets**
```
Trileaflet  ██████████ 10
```

**Aortic valve structure: acuity of finding**
```
Routine — no special prioritization               █████████░ 9
Not applicable (finding absent or not evaluable)  █░░░░░░░░░ 1
```

**Aortic valve structural abnormalities: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Aortic valve abnormal motion: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Aortic stenosis: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Aortic regurgitation**
```
Absent  ██████████ 10
```

**Aortic regurgitation severity**
```
Not applicable  ██████████ 10
```

**Aortic regurgitation: acuity of finding**
```
Not applicable (finding absent or not evaluable)  ██████████ 10
```

### Mitral Valve

**Mitral valve structure**
```
Structurally normal  ██████████ 10
```

**Mitral valve structure: acuity of finding**
```
Routine — no special prioritization               █████████░ 9
Not applicable (finding absent or not evaluable)  █░░░░░░░░░ 1
```

**Mitral valve structural abnormalities: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Mitral valve abnormal motion: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Mitral stenosis: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Mitral regurgitation**
```
Present  ██████████ 10
```

**Mitral regurgitation severity**
```
Trivial  ██████░░░░ 6
Mild     ████░░░░░░ 4
```

**Mitral regurgitation: mechanism** _(conditional)_
```
Cannot evaluate from present data  ██████████ 10
```

**Mitral regurgitation: acuity of finding**
```
Routine — no special prioritization  ██████████ 10
```

### Pulmonic Valve

**Pulmonic valve structure**
```
Not well visualized  ██████████ 10
```

**Pulmonic valve structure: acuity of finding**
```
Not applicable (finding absent or not evaluable)  ██████████ 10
```

**Pulmonic valve structural abnormalities: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Pulmonic valve abnormal motion: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Pulmonic stenosis**
```
Absent  ██████████ 10
```

**Pulmonic stenosis severity**
```
Not applicable  ██████████ 10
```

**Pulmonic stenosis: acuity of finding**
```
Not applicable (finding absent or not evaluable)  ██████████ 10
```

**Pulmonic regurgitation**
```
Present  ████████░░ 8
Absent   ██░░░░░░░░ 2
```

**Pulmonic regurgitation severity**
```
Trivial         ████████░░ 8
Not applicable  ██░░░░░░░░ 2
```

**Pulmonic regurgitation: acuity of finding**
```
Routine — no special prioritization               ████████░░ 8
Not applicable (finding absent or not evaluable)  ██░░░░░░░░ 2
```

### Tricuspid Valve

**Tricuspid valve structure**
```
Structurally normal  ██████████ 10
```

**Tricuspid valve: number of leaflets**
```
Not determined  ██████████ 10
```

**Tricuspid valve structure: acuity of finding**
```
Routine — no special prioritization               █████████░ 9
Not applicable (finding absent or not evaluable)  █░░░░░░░░░ 1
```

**Tricuspid valve structural abnormalities: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Tricuspid valve abnormal motion: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Tricuspid stenosis**
```
Absent  ██████████ 10
```

**Tricuspid stenosis: acuity of finding**
```
Not applicable (finding absent or not evaluable)  ██████████ 10
```

**Tricuspid regurgitation**
```
Present  ██████████ 10
```

**Tricuspid regurgitation severity**
```
Trivial  ██████████ 10
```

**Tricuspid regurgitation: acuity of finding**
```
Routine — no special prioritization  ██████████ 10
```

**Right ventricular systolic pressure**
```
Not estimable  ██████████ 10
```

**Right ventricular systolic pressure: acuity of finding**
```
Not applicable (finding absent or not evaluable)  ██████████ 10
```

### Prosthetic Valves or Repaired Valves

**Prosthetic or repaired valve: does this parameter need to be in the report?**
```
No  ██████████ 10
```

### Pericardium

**Pericardium**
```
Normal  ██████████ 10
```

**Pericardial abnormalities: acuity of finding**
```
Not applicable (finding absent or not evaluable)  █████████░ 9
Routine — no special prioritization               █░░░░░░░░░ 1
```

**Pericardial effusion**
```
Absent  ██████████ 10
```

**Pericardial effusion size**
```
Not applicable  ██████████ 10
```

**Pericardial effusion location**
```
Not applicable  ██████████ 10
```

**Pericardial effusion content or appearance**
```
Not applicable  ██████████ 10
```

**Pericardial effusion: acuity of finding**
```
Not applicable (finding absent or not evaluable)  ██████████ 10
```

**Tamponade physiology or constriction**
```
Neither  ██████████ 10
```

**Supporting findings (select all that apply)** _(select all)_
```
None  ██████████ 10
-- per option --
None  ██████████ 10
```

**Tamponade physiology or constriction: acuity of finding**
```
Not applicable (finding absent or not evaluable)  ██████████ 10
```

**Epicardial fat: does this parameter need to be in the report?**
```
No  ██████████ 10
```

### Aorta

**Aortic size**
```
Normal  ██████████ 10
```

**Aortic size severity**
```
Not applicable  ██████████ 10
```

**Aorta: segments measured (select all that apply)** _(select all)_
```
Sinuses of Valsalva  ██████████ 10
-- per option --
Sinuses of Valsalva  ██████████ 10
```

**Aortic size: acuity of finding**
```
Routine — no special prioritization               █████████░ 9
Not applicable (finding absent or not evaluable)  █░░░░░░░░░ 1
```

**Aorta: abnormalities**
```
None  ██████████ 10
```

**Aorta abnormalities: acuity of finding**
```
Not applicable (finding absent or not evaluable)  ██████████ 10
```

### Pulmonary Artery

**Pulmonary artery size: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Pulmonary artery other abnormalities: does this parameter need to be in the report?**
```
No  ██████████ 10
```

### Inferior Vena Cava

**Inferior vena cava size**
```
Normal  ██████████ 10
```

**Inferior vena cava respiratory change**
```
Not assessable           ██████░░░░ 6
Collapses more than 50%  ████░░░░░░ 4
```

**Estimated right atrial pressure**
```
Not estimable  ██████░░░░ 6
3 mmHg (0-5)   ████░░░░░░ 4
```

**Inferior vena cava size and right atrial pressure: acuity of finding**
```
Routine — no special prioritization               ████████░░ 8
Not applicable (finding absent or not evaluable)  ██░░░░░░░░ 2
```

**Inferior vena cava masses or devices: does this parameter need to be in the report?**
```
No  ██████████ 10
```

**Hepatic vein flow pattern: does this parameter need to be in the report?**
```
No  ██████████ 10
```

### Extracardiac

**Extracardiac abnormalities: does this parameter need to be in the report?**
```
No  ██████████ 10
```

## Fields left blank in every run

These are all conditional questions whose condition no run met (or optional fields no run filled).


**Left Ventricle:** LV mass: suspected etiology (consistent with); LV mass: location; LV mass: size (largest dimension); LV mass: echogenicity; LV mass: shape and attachment; LV mass: describe 'Other'; LV mass: mobility; Left ventricle intracavitary or myocardial masses: acuity of finding; Upper septal finding; Upper septal morphology: hemodynamic consequence; Left ventricular upper septal morphology: acuity of finding; Aneurysm, pseudoaneurysm or diverticulum: type; Aneurysm, pseudoaneurysm or diverticulum: location; Aneurysm, pseudoaneurysm or diverticulum: size (largest dimension); Aneurysm, pseudoaneurysm or diverticulum: associated thrombus or mass; Aneurysm, pseudoaneurysm or diverticulum: acuity of finding; Regional wall motion: walls involved (select all that apply); Anterior wall: level (select all that apply); Anterior wall: grade (select all that apply); Anteroseptal wall: level (select all that apply); Anteroseptal wall: grade (select all that apply); Inferoseptal wall: level (select all that apply); Inferoseptal wall: grade (select all that apply); Inferior wall: level (select all that apply); Inferior wall: grade (select all that apply); Inferolateral wall: level (select all that apply); Inferolateral wall: grade (select all that apply); Anterolateral wall: level (select all that apply); Anterolateral wall: grade (select all that apply); Apex: grade (select all that apply); Obstructive lesion: type; Obstructive lesion: peak gradient at rest (mmHg); Obstructive lesion: peak gradient with physiologic maneuver (mmHg); Obstructive lesions: acuity of finding; Global longitudinal strain value (GLS, %); Global longitudinal strain; Myocardial strain: acuity of finding; 

**Interventricular Septum:** Ventricular septal defect: type; Ventricular septal defect: size; Ventricular septal defect: number; Ventricular septal defect: acuity of finding; Abnormal septal motion: type (select all that apply); Abnormal septal motion: reason or explanation; Abnormal septal motion: reason or explanation: describe 'Other'; Abnormal septal motion: acuity of finding; Ventricular septal shunt: direction; Ventricular septal shunt: detection technique (select all that apply); Ventricular septal shunt: peak gradient across the defect (mmHg); Ventricular septal shunt: acuity of finding; 

**Right Ventricle:** RV mass: suspected etiology (consistent with); RV mass: location; RV mass: size (largest dimension); RV mass: echogenicity; RV mass: shape and attachment; RV mass: describe 'Other'; RV mass: mobility; Right ventricle intracavitary or myocardial masses: acuity of finding; Catheter or device lead: type; Catheter or device lead: type: describe 'Other'; Catheter or device lead: location; Catheter or device lead: location: describe 'Other'; Catheter or device lead: associated masses; Right ventricle catheters or device leads: acuity of finding; RV regional wall motion: walls involved (select all that apply); RV free wall: level (select all that apply); RV free wall: grade (select all that apply); RV apex: grade (select all that apply); Right ventricular regional wall motion abnormalities: acuity of finding; 

**Left Atrium:** LA mass: suspected etiology (consistent with); LA mass: location; LA mass: size (largest dimension); LA mass: echogenicity; LA mass: shape and attachment; LA mass: describe 'Other'; LA mass: mobility; Left atrium intracavitary masses: acuity of finding; Left atrial appendage mass: suspected etiology (consistent with); Left atrial appendage mass: location; Left atrial appendage mass: size (largest dimension); Left atrial appendage mass: echogenicity; Left atrial appendage mass: shape and attachment; Left atrial appendage mass: mobility; Left atrial appendage mass: describe 'Other'; Left atrial appendage intracavitary masses: acuity of finding; Left atrial appendage: spontaneous echo contrast grade; Left atrial appendage spontaneous echo contrast: acuity of finding; Left atrial appendage device: type; Left atrial appendage device: size (mm); Left atrial appendage device: type: describe 'Other'; Left atrial appendage device: pathologic findings (select all that apply); Left atrial appendage devices: acuity of finding; Pulmonary vein flow pattern; Pulmonary vein flow pattern: acuity of finding; Left atrial strain; Left atrial reservoir strain value (%); Left atrial strain: acuity of finding; 

**Right Atrium:** RA mass: suspected etiology (consistent with); RA mass: location; RA mass: size (largest dimension); RA mass: echogenicity; RA mass: shape and attachment; RA mass: describe 'Other'; RA mass: mobility; Right atrium intracavitary masses: acuity of finding; Right atrial spontaneous echo contrast grade; Right atrium spontaneous echo contrast: acuity of finding; Right atrial catheter or device lead: type; Right atrial catheter or device lead: type: describe 'Other'; Right atrial catheter or device lead: location; Right atrial catheter or device lead: location: describe 'Other'; Right atrial catheter or device lead: associated masses; Right atrium catheters or device leads: acuity of finding; 

**Interatrial Septum:** Interatrial septum: abnormality (select all that apply); Interatrial septum: bowing direction; Atrial septal defect: type; Interatrial septal communication; Interatrial septal communication: type; Interatrial septal communication: size (largest dimension); Interatrial septal communication: type: describe 'Other'; Interatrial septal communications: acuity of finding; Atrial septal device: type; Atrial septal device: size (mm); Atrial septal device: type: describe 'Other'; Atrial septal device: pathologic findings (select all that apply); Interatrial septal devices: acuity of finding; Interatrial shunt: direction; Interatrial shunt: location; Interatrial shunt: detection technique (select all that apply); Interatrial shunt: Qp:Qs; Interatrial shunt: acuity of finding; 

**Aortic Valve:** Aortic valve: structural abnormality (select all that apply); Aortic valve: structural abnormality: describe 'Other'; Bicuspid aortic valve: type; Aortic valve: suspected etiology; Aortic valve: suspected etiology: describe 'Other'; Aortic valve structural abnormalities: acuity of finding; Aortic valve: abnormal motion (select all that apply); Aortic valve abnormal motion: acuity of finding; Aortic stenosis severity; Aortic stenosis: mechanism; Aortic stenosis: mechanism: describe 'Other'; Aortic stenosis: acuity of finding; Aortic regurgitation: mechanism; Aortic regurgitation: mechanism: describe 'Other'; 

**Mitral Valve:** Mitral valve: structural abnormality (select all that apply); Mitral valve: structural abnormality: describe 'Other'; Mitral valve: leaflet involved (select all that apply); Mitral valve: suspected etiology; Mitral valve: suspected etiology: describe 'Other'; Mitral valve structural abnormalities: acuity of finding; Mitral valve: abnormal motion (select all that apply); Mitral valve abnormal motion: acuity of finding; Mitral stenosis severity; Mitral stenosis: mechanism; Mitral stenosis: mechanism: describe 'Other'; Mitral stenosis: acuity of finding; Mitral regurgitation: mechanism: describe 'Other'; 

**Pulmonic Valve:** Pulmonic valve: structural abnormality (select all that apply); Pulmonic valve: structural abnormality: describe 'Other'; Pulmonic valve structural abnormalities: acuity of finding; Pulmonic valve: abnormal motion (select all that apply); Pulmonic valve abnormal motion: acuity of finding; 

**Tricuspid Valve:** Tricuspid valve: structural abnormality (select all that apply); Tricuspid valve: structural abnormality: describe 'Other'; Tricuspid valve: suspected etiology; Tricuspid valve: suspected etiology: describe 'Other'; Tricuspid valve structural abnormalities: acuity of finding; Tricuspid valve: abnormal motion (select all that apply); Tricuspid valve abnormal motion: acuity of finding; 

**Prosthetic Valves or Repaired Valves:** Prosthetic or repaired valve: position (select all that apply); Prosthetic or repaired valve: type; Prosthetic or repaired valve: type: describe 'Other'; Prosthetic valve motion; Prosthetic or repaired valve: pathologic findings (select all that apply); Prosthetic or repaired valve: pathologic findings: describe 'Other'; Prosthetic or repaired valve: masses; Prosthetic or repaired valve: stenosis; Prosthetic or repaired valve: regurgitation; Prosthetic or repaired valve regurgitation severity; Prosthetic or repaired valve: regurgitation location; Prosthetic or repaired valve: acuity of finding; 

**Pericardium:** Pericardial abnormality (select all that apply); Pericardial abnormality: describe 'Other'; Pericardial effusion: measurement (cm); Epicardial fat: amount; Epicardial fat: acuity of finding; 

**Aorta:** Aorta: dilated segments (select all that apply); Aorta: abnormality (select all that apply); Aorta: abnormality: describe 'Other'; Aorta: abnormality location (select all that apply); Aorta: abnormality location: describe 'Other'; 

**Pulmonary Artery:** Pulmonary artery size; Pulmonary artery size: acuity of finding; Pulmonary artery: abnormality (select all that apply); Pulmonary artery: abnormality: describe 'Other'; Pulmonary artery: abnormality location (select all that apply); Pulmonary artery: abnormality location: describe 'Other'; Pulmonary artery other abnormalities: acuity of finding; 

**Inferior Vena Cava:** Inferior vena cava: mass or device (select all that apply); Inferior vena cava: mass or device: describe 'Other'; Inferior vena cava: mass or device location; Inferior vena cava: mass or device location: describe 'Other'; Inferior vena cava masses or devices: acuity of finding; Hepatic vein flow pattern; Hepatic vein flow pattern: acuity of finding; 

**Extracardiac:** Extracardiac abnormality (select all that apply); Extracardiac abnormality: describe 'Other'; Extracardiac abnormality: size or severity; Extracardiac abnormality: size or severity: describe 'Other'; Extracardiac abnormalities: acuity of finding; 
