ARG MANGLER_ROOT
ARG PORT
FROM python:3.11

ARG MANGLER_ROOT
ARG HOST="0.0.0.0"
ARG PORT

ENV ROOT=${MANGLER_ROOT}
WORKDIR ${ROOT}

ENV HOST=${HOST}
ENV PORT=${PORT}

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG COMMON_PATH=${MANGLER_ROOT}/common/
COPY common/python/ ${COMMON_PATH}
WORKDIR ${COMMON_PATH}
RUN pip install --no-cache-dir .
WORKDIR ${MANGLER_ROOT}

COPY backend/ .


CMD ["python", "app.py"]