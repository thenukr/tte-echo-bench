This is a research benchmark that evaluates how well models write echocardiography report summaries.
The patient data is de-identified, and nothing you write will be used for patient care.

A transthoracic echocardiogram (TTE) has been read, and the structured findings are complete. Write the
summary of the report from those findings.

## Inputs

- `/app/findings/`: the completed structured findings, one JSON file per cardiac structure (left ventricle,
  valves, atria, pericardium, aorta and the rest). In each file, the `answer` of every field holds the
  reader's finding. `options` lists the choices that were available and `option_labels` spells out
  abbreviated options. `answer: null` means the field did not apply (its `only_if` condition was not met)
  or was left blank. `cannot_evaluate` means the reader could not assess it from the study.
- `/app/study/Patient_007_clinical_context_and_study_data.pdf`: the clinical context (age, sex, reason for
  study, history) and the study's measurement tables. `pdftotext` and `pdftoppm` are installed.

Each finding has an acuity grade: `routine`, `significant`, `urgent`, `critical` or `not_applicable`.
No prior study is available, so acuity was graded as if each finding were seen for the first time.

## Output

Write the summary to `/app/output/summary.md` (Markdown):

1. **Summary headline:** the first line. It must name every finding graded `significant`, `urgent` or
   `critical`, most acute first. If none are graded that high, say the study shows no significant findings.
2. **Impression:** the remaining clinically relevant findings, as a concise numbered list in order of
   importance. Do not repeat every normal or non-evaluable field.

Base the summary on the structured findings. Do not contradict them or add findings they do not support.
Do not edit anything in `/app/findings/`.
