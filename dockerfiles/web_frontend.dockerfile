FROM python:3.13 AS base
# Create integration testing environment
RUN apt-get update
COPY packages/__init__.py packages/__init__.py
COPY packages/api_requests.py packages/api_requests.py
COPY packages/databases.py packages/databases.py
COPY packages/user_database.py packages/user_database.py
COPY tests/__init__.py tests/__init__.py
COPY tests/test_api_requests.py tests/test_api_requests.py
COPY tests/setup_functions.py tests/setup_functions.py
COPY env/ui_localtest.txt .
RUN pip install -r ui_localtest.txt
RUN pytest -v tests/

FROM base AS builder
WORKDIR /app
COPY packages/__init__.py packages/__init__.py
COPY packages/api_requests.py packages/api_requests.py
COPY packages/ui_settings.py packages/ui_settings.py
COPY env/ui_release.txt .
COPY assets/ assets/
COPY pages/ pages/
COPY value_tracker/ value_tracker/
COPY rxconfig.py .
RUN pip install -r ui_release.txt
RUN reflex export --frontend-only --no-zip

FROM nginx

COPY --from=builder /app/.web/build/client /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf