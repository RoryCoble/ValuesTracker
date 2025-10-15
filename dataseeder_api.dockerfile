FROM python:latest AS base
# Create integration testing environment
RUN apt-get update
COPY packages/__init__.py packages/__init__.py
COPY packages/databases.py packages/databases.py
COPY tests/__init__.py tests/__init__.py
COPY tests/test_dataseeder_api.py tests/test_dataseeder_api.py
COPY tests/test_DataSeeder.py tests/test_DataSeeder.py
COPY dataseederapi_localtest.txt .
COPY DataSeeder.py .
COPY dataseeder_api.py .
RUN pip install -r dataseederapi_localtest.txt
RUN pytest -v tests/

FROM base AS release
RUN apt-get update
COPY packages/__init__.py packages/__init__.py
COPY packages/databases.py packages/databases.py
COPY dataseederapi_release.txt .
COPY DataSeeder.py .
COPY dataseeder_api.py .
RUN pip install -r dataseederapi_release.txt
CMD ["python","dataseeder_api.py"]