## String de Conexão

DATABASE_URL=postgresql+asyncpg://postgressRailForge:12345@postgress:5432/postgress

| Parte | Valor | De onde vem |
|---|---|---|
| usuário | postgressRailForge | POSTGRES_USER |
| senha | 12345 | POSTGRES_PASSWORD |
| host | postgress | container_name do banco — como o FastAPI está em um `docker-compose.yml` separado, ele não resolve mais pelo nome do serviço (`db`), e sim pelo `container_name`, através da rede externa compartilhada |
| porta | 5432 | porta interna do Postgres dentro da rede Docker (não precisa ser a mesma exposta no host) |
| database | postgress | POSTGRES_DB |

## Rede compartilhada entre os compose files

Como o banco e a API vivem em `docker-compose.yml` separados, eles não compartilham rede por padrão — cada `docker compose up` cria sua própria rede isolada. Pra resolver isso, criamos uma rede Docker **externa**, manualmente, e os dois arquivos se conectam a ela.

Criação (só uma vez, antes de subir qualquer um dos dois):

```bash
docker network create meuapp_network
```

Depois disso, os dois `docker-compose.yml` (db e api) declaram essa rede como `external: true` — ou seja, "não crie essa rede, apenas use a que já existe".

Conferir se os containers estão realmente na mesma rede:

```bash
docker network inspect meuapp_network
```

## Docker Compose — explicação linha a linha

```yaml
services:
  db:                                    # nome do serviço dentro deste compose (não é mais usado como hostname pela API, já que está em outro arquivo)
    image: postgres:18                   # imagem oficial do Postgres, versão 18 (mesma major version usada no Neon em produção)
    container_name: postgress            # nome fixo do container — é ESTE nome que a API usa como host na DATABASE_URL
    restart: unless-stopped              # reinicia o container automaticamente se cair, exceto se você parar manualmente

    environment:
      POSTGRES_USER: postgressRailForge  # cria esse usuário como superuser do banco na primeira inicialização
      POSTGRES_PASSWORD: 12345           # senha do usuário acima (⚠️ só serve pra dev local — nunca use senha fraca assim em produção)
      POSTGRES_DB: postgress             # cria esse banco de dados automaticamente na primeira inicialização

    ports:
      - "5432:5432"                      # <porta do host>:<porta do container>
                                          # expõe o Postgres também pra fora do Docker (ex: DBeaver, psql no seu terminal)
                                          # não é necessário para o FastAPI acessar via `postgress:5432`, mas ajuda a inspecionar o banco manualmente

    volumes:
      - pgdata:/var/lib/postgresql/data  # persiste os dados do banco fora do ciclo de vida do container
                                          # sem isso, cada `docker compose down` apagaria todos os dados
                                          # pgdata é um "named volume" — gerenciado pelo Docker, não uma pasta visível no projeto

    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgressRailForge -d postgress"]
                                          # verifica se o Postgres já está pronto pra aceitar conexões
      interval: 5s                       # checa a cada 5 segundos
      timeout: 5s                        # espera até 5s por uma resposta antes de considerar falha
      retries: 5                         # tenta 5 vezes antes de marcar o container como "unhealthy"
                                          # como db e api estão em compose files diferentes, o `depends_on` do compose da API
                                          # não consegue enxergar esse healthcheck automaticamente — pode ser necessário
                                          # um retry/wait manual na conexão do FastAPI, ou um script de espera no entrypoint

    networks:
      - meuapp_network                   # conecta este container à rede externa compartilhada com a API

volumes:
  pgdata:                                # declara o volume nomeado usado acima

networks:
  meuapp_network:
    external: true                       # não cria uma rede nova — usa a que foi criada manualmente com `docker network create`
```