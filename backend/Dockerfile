ARG MANGLER_ROOT
FROM python:3.11

ARG HOST="0.0.0.0"
ARG PORT=5000

ARG MANGLER_ROOT
ENV ROOT=${MANGLER_ROOT}
WORKDIR ${ROOT}

ENV HOST=${HOST}
ENV PORT=${PORT}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]