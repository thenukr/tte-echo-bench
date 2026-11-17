FROM python:3.12-slim

# Tools for reading the study: DICOM (pydicom + JPEG codecs), cine export (ffmpeg), the clinical docx
# (python-docx), stills (Pillow), plus jq.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg poppler-utils jq \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir pydicom numpy pillow python-docx pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg

WORKDIR /app
COPY workspace/ /app/
