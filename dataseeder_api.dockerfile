FROM python:latest AS base
# Create integration testing environment
RUN apt-get update
COPY packages/__init__.py packages/__init__.py
COPY packages/Databases.py packages/Databases.py
COPY tests/__init__.py tests/__init__.py
COPY tests/test_DataSeederApi.py tests/test_DataSeederApi.py
COPY dataseederapi_localtest.txt .
COPY DataSeeder.py .
COPY DataSeederApi.py .
RUN pip install -r dataseederapi_localtest.txt
RUN pytest -v tests/

FROM base AS release
RUN apt-get update
COPY packages/__init__.py packages/__init__.py
COPY packages/Databases.py packages/Databases.py
COPY dataseederapi_release.txt .
COPY DataSeeder.py .
COPY DataSeederApi.py .
RUN pip install -r dataseederapi_release.txt
CMD ["python","DataSeederApi.py"]