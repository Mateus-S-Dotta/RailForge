### Próximo passo: conectar o FastAPI a esse banco

Pra o container do FastAPI conseguir resolver `db` como hostname, os dois serviços precisam estar no **mesmo `docker-compose.yml`** (ou na mesma rede Docker, se forem arquivos separados). Exemplo juntando os dois:

\`\`\`yaml
services:
  db:
    # ... (como acima)

  api:
    build: .
    container_name: fastapi_app
    depends_on:
      db:
        condition: service_healthy       # só sobe a API depois que o Postgres estiver pronto
    environment:
      DATABASE_URL: postgresql+asyncpg://postgressRailForge:12345@db:5432/postgress
    ports:
      - "8000:8000"
\`\`\`

docker run --rm -it -v "${PWD}:/app" -w /app node:24.14.0-slim npx create-next-app@latest .

Adicionando algo ao final para testar
