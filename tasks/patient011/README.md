# patient011

Harbor task: read an adult TTE and fill out `findings_form.csv` (341 columns; answer options in `findings_form_options.json`).

The imaging is not in the repo. Before building the task, copy the study from the shared Drive folder into:

- `environment/workspace/Exam_DICOM/JOSHUA_DEBEAR_11-09-2026_23598818/` (the 44 `.dcm` files) and `environment/workspace/Exam_DICOM/dicom_viewing_instructions.txt`
- `environment/workspace/Exam_VendorNeutral/JOSHUA_DEBEAR_11-09-2026_23598818/` (`Images/` with the annotated still and `Thumbnails/`, and `Exam_Data/` with `study.json` and `annotated_images_manifest.json`)

Run with, for example:

```
harbor run -p tasks/patient011 -a codex -m gpt-6-astra --ak reasoning_effort=xhigh -o jobs -k 1 -n 1
```

The verifier only checks that the form has one answer row with all 341 columns; scoring against the expert's answers is done separately.
