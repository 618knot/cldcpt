build:
	docker compose build
up:
	docker compose up -d
uplog:
	docker compose up
down:
	docker compose down
bash:
	docker compose exec fastapi_app bash
