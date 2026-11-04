FROM python:3.12-slim

WORKDIR /app

# Study imaging for this patient. Placeholder until the de-identified TTE clips/stills are added.
COPY study/ /app/study/

# Blank structured report, one JSON per cardiac structure. The agent fills in the "answer" values in place.
COPY report_template/ /app/report/
