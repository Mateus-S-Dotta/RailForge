CMD
docker run --rm -it -v "%cd%":/app -w /app node:24.14.0-slim npx shadcn@latest add input

docker logs -f <nome_ou_id_do_container>