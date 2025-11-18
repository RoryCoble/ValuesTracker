FROM python:latest AS base
# Create integration testing environment
RUN apt-get update
ARG HOST
ENV HOST=${HOST}
ARG PORT
ENV PORT=${PORT}
COPY packages/__init__.py packages/__init__.py
COPY packages/databases.py packages/databases.py
COPY packages/user_database.py packages/user_database.py
COPY tests/__init__.py tests/__init__.py
COPY tests/test_dataseeder.py tests/test_dataseeder.py
COPY tests/test_entities_values.py tests/test_entities_values.py
COPY tests/setup_functions.py tests/setup_functions.py
COPY dataseeder_localtest.txt .
COPY dataseeder.py .
RUN pip install -r dataseeder_localtest.txt
RUN pytest -v tests/

FROM base AS release
RUN apt-get update
COPY packages/__init__.py packages/__init__.py
COPY packages/databases.py packages/databases.py
COPY dataseeder_release.txt .
COPY dataseeder.py .
RUN pip install -r dataseeder_release.txt
CMD ["python","dataseeder.py"]