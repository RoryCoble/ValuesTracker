FROM python:latest AS base
# Create integration testing environment
RUN apt-get update
COPY packages/__init__.py packages/__init__.py
COPY packages/databases.py packages/databases.py
COPY packages/user_database.py packages/user_database.py
COPY tests/__init__.py tests/__init__.py
COPY tests/test_user_database.py tests/test_user_database.py
COPY tests/test_api.py tests/test_api.py
COPY api_localtest.txt .
COPY api.py .
RUN pip install -r api_localtest.txt
RUN pytest -v tests/

FROM base AS release
RUN apt-get update
COPY packages/__init__.py packages/__init__.py
COPY packages/databases.py packages/databases.py
COPY packages/user_database.py packages/user_database.py
COPY api_release.txt .
COPY api.py .
RUN pip install -r api_release.txt
CMD ["python","api.py"]