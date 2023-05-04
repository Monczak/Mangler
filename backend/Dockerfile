ARG MANGLER_ROOT
FROM python:3.11

ARG MANGLER_ROOT
ENV ROOT=${MANGLER_ROOT}
WORKDIR ${ROOT}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]