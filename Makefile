.PHONY: convert
convert:
	docker compose -f docker-compose-convert.yml up --build

.PHONY: build
build:
	docker compose build

.PHONY: run
run:
	docker compose up
