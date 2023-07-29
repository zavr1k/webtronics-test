compose-up:
		docker-compose up -d
compose-down:
		docker-compose down

lint:
	poetry run flake8 src/ tests/

test: compose-test-up compose-test compose-test-down
compose-test-up:
		docker-compose -f docker-compose-test.yaml up --build -d
compose-test:
		docker exec webtronics-app-test poetry run flake8 src/ tests/ || true
		docker exec webtronics-app-test poetry run pytest -s tests/ || true
compose-test-down:
		docker-compose -f docker-compose-test.yaml  down
