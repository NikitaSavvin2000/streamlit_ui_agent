FROM python:3.11-buster
USER root
RUN apt-get update
RUN apt-get install -y vim poppler-utils

WORKDIR /app
COPY ./ ./

COPY pyproject.toml pdm.lock README.md ./

RUN pip install -U pip setuptools wheel
RUN pip install zstandard
RUN pip install pdm
RUN pdm install --prod --frozen-lockfile --no-editable
RUN pdm build
RUN pdm install

EXPOSE 8501

ENTRYPOINT ["pdm", "run", "src/server.py"]