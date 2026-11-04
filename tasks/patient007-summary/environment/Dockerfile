FROM python:3.12-slim

# poppler-utils (pdftotext/pdftoppm) for the clinical context PDF, jq for reading the findings JSONs.
RUN apt-get update \
    && apt-get install -y --no-install-recommends poppler-utils jq \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Completed structured findings (patient007, filled from expert alex.ryzhikov's Tally submission).
COPY findings/ /app/findings/
# Clinical context and measurement tables.
COPY study/ /app/study/

# The agent writes its summary here.
RUN mkdir -p /app/output
