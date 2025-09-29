FROM cypress/base:latest

WORKDIR /tests
ENV CYPRESS_BASE_URL=http://host.docker.internal:3000
ENV cypress_database=host.docker.internal
ENV cypress_database_port=5431
ENV cypress_api=http://host.docker.internal:5001
ENV cypress_dataseeder_api=http://host.docker.internal:5002

COPY ./package.json .
COPY ./cypress.config.js .
COPY ./cypress ./cypress

RUN npm i

ENTRYPOINT ["npx", "cypress", "run"]