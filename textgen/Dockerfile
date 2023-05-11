ARG MANGLER_ROOT
FROM python:3.11

ARG MANGLER_ROOT

ARG HOST="0.0.0.0"
ARG PORT=5000

WORKDIR ${MANGLER_ROOT}

COPY textgen/requirements/textgen.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ARG COMMON_PATH=${MANGLER_ROOT}/common/
COPY common/python/ ${COMMON_PATH}
WORKDIR ${COMMON_PATH}
RUN pip install --no-cache-dir .
WORKDIR ${MANGLER_ROOT}

COPY textgen/ .


ENV HOST=${HOST}
ENV PORT=${PORT}

EXPOSE ${PORT}

CMD ["python", "app.py"]