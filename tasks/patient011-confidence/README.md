# patient011-confidence

Variant of `tasks/patient011` with a confidence column for every finding.

- `findings_form.csv` has 610 columns: each of the 269 non-acuity questions is followed by a `<question> confidence` column (same `answer_only_if` as its question). Acuity questions have no confidence column.
- Confidence options are `Supported by evidence`, `Usable, partially supported`, then the question's own abstention option(s) (e.g. `Cannot evaluate`, `Not estimable`), which were moved out of the finding's dropdown. Questions with no abstention option get `Cannot evaluate`. `Indeterminate` stays in the mass "suspected etiology" questions because later conditions depend on it.
- `instruction.md` is the original patient011 prompt plus one sentence asking for a best guess on every finding, with the confidence column used to flag weak evidence.

The imaging is not in the repo. Copy it in exactly as described in `tasks/patient011/README.md` (into `Exam_DICOM/` and `Exam_VendorNeutral/` here).

```
harbor run -p tasks/patient011-confidence -a codex -m gpt-6-astra --ak reasoning_effort=xhigh -o jobs -k 1 -n 1
```

The verifier only checks for one answer row with all 610 columns. To score against the expert, drop the `confidence` columns and grade the remaining 341 as for patient011.
