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

## Updates: Python Playwright tests added

With the application running, simply enter the commands below to see the testing output or go to playwright_tests and look them over.
```
pip install -r env/playwright.txt
pytest -v playwright_tests/
```

## Updates: GitHub workflows complete with end to end testing!

Building on the above I added a series of github actions workflows that take any push to main, or PR, and rebuilds the images in dependency order. For example, until the Database workflow is finished the Dataseeder, Dataseeder Api, and Api images will not be built. That way, during the test step for those images the newest version of Database is checked against the new code to ensure that the integration tests still pass for these latest changes. This roles all the way up until the application's images are built and the UI Test workflow runs. There the entire application is spun up, in the pipelines memory, and an entire Playwright test suite is run against the newest full version of the application. Here further workflows could be added to start triggering releases of builds that have been fully vetted. The files for this change be found at [.github/workflows/](.github/workflows/).
