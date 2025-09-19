FROM python:latest AS base
# Create integration testing environment
RUN apt-get update
COPY packages/__init__.py packages/__init__.py
COPY packages/Databases.py packages/Databases.py
COPY tests/__init__.py tests/__init__.py
COPY tests/test_DataSeeder.py tests/test_DataSeeder.py
COPY tests/test_EntitiesValues.py tests/test_EntitiesValues.py
COPY dataseeder_localtest.txt .
COPY DataSeeder.py .
RUN pip install -r dataseeder_localtest.txt
RUN pytest -v tests/

FROM base AS release
RUN apt-get update
COPY packages/__init__.py packages/__init__.py
COPY packages/Databases.py packages/Databases.py
COPY dataseeder_release.txt .
COPY DataSeeder.py .
RUN pip install -r dataseeder_release.txt
CMD ["python","DataSeeder.py"]