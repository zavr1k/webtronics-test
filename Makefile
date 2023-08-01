compose:
		docker-compose -f docker-compose.yaml up -d --build
compose-down:
		docker-compose down

compose-dev:
		docker-compose up --build

lint:
	poetry run flake8 src/ tests/

test: compose-test-up compose-test compose-test-down
compose-test-up:
		docker-compose -f docker-compose-test.yaml -p webtronics-test up --build -d
compose-test:
		docker exec webtronics-app-test poetry run flake8 src/ tests/ || true
		docker exec webtronics-app-test poetry run pytest -s -vv tests/ || true
compose-test-down:
		docker-compose -f docker-compose-test.yaml -p webtronics-test down
