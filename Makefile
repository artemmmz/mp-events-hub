DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .dev.env
APP = docker_compose/app.yaml
DB = docker_compose/pg.yaml
RMQ = docker_compose/rmq.yaml
REDIS = docker_compose/redis.yaml

.PHONY: app
app:
	${DC} -f ${APP} ${ENV} up --build -d
	# docker compose -f docker_compose/app.yaml --env-file .dev.env up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP} ${ENV} down
	# docker compose -f docker_compose/app.yaml --env-file .dev.env down

.PHONY: pg
pg:
	${DC} -f ${DB} ${ENV} up --build -d
	# docker compose -f docker_compose/pg.yaml --env-file .dev.env up --build -d

.PHONY: pg-down
pg-down:
	${DC} -f ${DB} ${ENV} down
	# docker compose -f docker_compose/pg.yaml --env-file .dev.env down

.PHONY: rmq
rmq:
	${DC} -f ${RMQ} ${ENV} up --build -d

.PHONY: rmq-down
rmq-down:
	${DC} -f ${RMQ} ${ENV} down


.PHONY: redis
redis:
	${DC} -f ${REDIS} ${ENV} up --build -d

.PHONY: redis-down
redis-down:
	${DC} -f ${REDIS} ${ENV} down