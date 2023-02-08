FROM python:3.8-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev gcc
RUN apt-get update && apt-get install -y wget

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . .

# HEALTHCHECK --interval=10s --timeout=10s --start-period=55s \
#    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/ || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

