DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .dev.env
APP = docker_compose/app.yaml
DB = docker_compose/pg.yaml

.PHONY: app
app:
	${DC} -f ${APP} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP} ${ENV} down

.PHONY: pg
pg:
	${DC} -f ${DB} ${ENV} up --build -d

.PHONY: pg-down
pg-down:
	${DC} -f ${DB} ${ENV} down
