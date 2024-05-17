FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DOCKER_BUILDKIT=1
WORKDIR /app
COPY requirements requirements
RUN python -m pip install --upgrade pip && \
    pip install -r requirements/test.requirements.txt --no-cache-dir
COPY . .
