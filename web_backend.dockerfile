FROM python:latest AS base
# Create integration testing environment
RUN apt-get update
COPY packages/__init__.py packages/__init__.py
COPY packages/ApiRequests.py packages/ApiRequests.py
COPY packages/Databases.py packages/Databases.py
COPY packages/UserDatabase.py packages/UserDatabase.py
COPY tests/__init__.py tests/__init__.py
COPY tests/test_ApiRequests.py tests/test_ApiRequests.py
COPY ui_localtest.txt .
RUN pip install -r ui_localtest.txt
RUN pytest -v tests/

FROM base AS release
ENV REDIS_URL=redis://redis PYTHONUNBUFFERED=1
ENV CUSTOM_API_URL=http://api:5000
WORKDIR /app
COPY packages/__init__.py packages/__init__.py
COPY packages/ApiRequests.py packages/ApiRequests.py
COPY packages/UiSettings.py packages/UiSettings.py
COPY ui_release.txt .
COPY assets/ assets/
COPY pages/ pages/
COPY ValueTracker/ ValueTracker/
COPY rxconfig.py .

RUN pip install -r ui_release.txt
ENTRYPOINT ["reflex", "run", "--env", "prod", "--backend-only", "--loglevel", "debug"]