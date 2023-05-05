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

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]