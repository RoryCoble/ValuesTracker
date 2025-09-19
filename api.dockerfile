FROM python:latest AS base
# Create integration testing environment
RUN apt-get update
COPY packages/ packages/
COPY tests/__init__.py tests/__init__.py
COPY tests/test_UserDatabase.py tests/test_UserDatabase.py
COPY tests/test_Api.py tests/test_Api.py
COPY api_localtest.txt .
COPY Api.py .
RUN pip install -r api_localtest.txt
RUN pytest -v tests/

FROM base AS release
RUN apt-get update
COPY packages/ packages/
COPY api_release.txt .
COPY Api.py .
RUN pip install -r api_release.txt
CMD ["python","Api.py"]