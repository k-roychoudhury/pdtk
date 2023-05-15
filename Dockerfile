FROM python:3.11-alpine AS base

# start the install process
WORKDIR /pdtk
COPY ./dist /pdtk/dist

RUN pip install /pdtk/dist/pdtk-*.whl

CMD ["python3", "-c", "import py_familizer; py_familizer.get_patent_families(['US-9145048-B2'])"]
