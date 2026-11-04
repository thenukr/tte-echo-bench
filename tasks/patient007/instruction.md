You are reading a transthoracic echocardiogram (TTE) and writing up the structured findings.

The study is in `/app/study/`. Review all of it before you report:

- `Patient_007_clinical_context_and_study_data.pdf`: the clinical context, the signed measurement
  table, and the measurements transcribed from the ultrasound system's own display.
- `Images/`: the imaging, with 27 MP4 cine clips and 39 JPEG stills named `Patient_007_<n>`.
  `Images/Thumbnails/` has a small preview frame for each of the 66 items.

`pdftotext`/`pdftoppm` (poppler), `ffmpeg`/`ffprobe` and Pillow are installed.

The report form is in `/app/report/`, with one JSON file per cardiac structure (left ventricle, right
ventricle, left atrium, right atrium, valves, pericardium, aorta and the rest). Each file has a
`fields` object. Fill in the `answer` of every field in place, following the `instructions` string at
the top of each file:

- `single` fields take exactly one option from `options`, written as a string.
- `multi` fields take a list of every option that applies.
- `text` fields take a short free-text description. They only come up when you pick `other`.
- A field with `only_if` / `only_if_any` is answered only when that condition holds. Otherwise its
  answer stays `null`. A field is also skipped when the field it depends on was skipped.
- Fields marked `optional` may be left `null` (or `[]`) even when their condition holds.
- `option_labels`, where present, gives the full wording behind an option key.
- Use `cannot_evaluate` when a finding cannot be assessed from the imaging provided.

Questions ending in "does this parameter need to be in the report?" ask whether the finding should
appear in the report at all. Answer `yes` only when it is present or clinically relevant to mention.

**Acuity of finding:** no prior study is provided, so grade the acuity of every finding as if it is
being seen for the first time. Any finding graded `significant`, `urgent` or `critical` goes into the
summary headline.

Do not rename, add or remove files or fields, and do not change anything except the `answer` values.
The report is graded on the files in `/app/report/` when you finish.
