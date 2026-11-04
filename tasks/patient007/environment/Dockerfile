FROM python:3.12-slim

# Tools for reading the study: poppler-utils (pdftotext/pdftoppm) for the clinical context PDF,
# ffmpeg/ffprobe for the MP4 clips, Pillow for the stills.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg poppler-utils \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir pillow==11.0.0

WORKDIR /app

# Study data: clinical context PDF + Images/ (27 MP4 clips, 39 JPEG stills, Thumbnails/).
COPY study/ /app/study/

# Blank structured report, one JSON per cardiac structure. The agent fills in the "answer" values in place.
COPY report_template/ /app/report/
