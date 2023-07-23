db:
		docker run --name webtronics-db -p 5432:5432 -e POSTGRES_USER=anton -e POSTGRES_PASSWORD=password -e POSTGRES_DB=webtronics -d postgres:14

dev-start:
		poetry run uvicorn src.main:app --reload
