# ValuesTracker
---

[Rory Coble](https://www.linkedin.com/in/rory-coble-572314107/)

---

ValuesTracker is a demo website used to showcase my ability to write a postgres & Python web application with automated testing built into each component. The UI utilizes the Reflex framework and the API relies on Flask. All of it is hosted in cicd-esq docker containers that render shippable software for some form of cloud deployment. Finally the whole application has a set of end to end tests written in Cypress. On it a user can select an Entity represented by some five letter code and watch its value go up and down in realtime.

## Starting the Application

Want to run my demo, and have docker desktop installed? Then execute the follow commands in the root of this repo using whatever shell you have configured.
```
docker compose up -d db 
docker compose up -d api
docker compose up -d dataseeder_api
docker compose up -d web_backend 
docker compose up -d web_frontend
docker compose up -d cypress
-- Once Cypress exits successfully --
docker compose up -d dataseeder
```
Then you can navigate a web browser to http://localhost:3000 and explore the application. Feel free to message me on LinkedIn with any questions or suggestions for improvements.