# Dados mock do RailForge

[mock.sql](mock.sql) cadastra **20 estações, 4 linhas e 20 conexões**, usando as tabelas de [models.py](../api/app/models.py). Cada linha recebe cinco estações com `sequence` de 1 a 5. As cores são azul, verde, vermelha e amarela.

As coordenadas formam quatro trajetos horizontais: X varia de 100 a 500 e Y é 100, 200, 300 ou 400 conforme a linha. Todas as posições são distintas. Os dados são fictícios, sem estações compartilhadas entre linhas.

## Pré-requisitos

- Docker Desktop em execução.
- Banco do projeto iniciado e saudável.
- API iniciada ao menos uma vez contra esse banco para criar `station`, `line` e `conection`. O SQL não cria tabelas. Em banco antigo, confira se `conection.sequence` existe: `create_all` não atualiza tabelas existentes.

## Executar pelo PowerShell

Na raiz do projeto (`RailForge`), inicie o banco, se necessário:

```powershell
docker compose -f .\bd\docker-compose.yml up -d
docker compose -f .\bd\docker-compose.yml ps
```

Depois de confirmar o banco saudável e as tabelas criadas, copie o SQL para o container e execute:

```powershell
docker cp .\bd\mock.sql postgress:/tmp/railforge-mock.sql
docker exec postgress psql -U postgressRailForge -d postgress -v ON_ERROR_STOP=1 -f /tmp/railforge-mock.sql
```

Os nomes de container, usuário e banco correspondem a [docker-compose.yml](docker-compose.yml). `ON_ERROR_STOP=1` interrompe a execução em caso de erro. A transação garante que a carga seja aplicada por inteiro ou revertida por inteiro.

## Conferir os registros

```powershell
docker exec postgress psql -U postgressRailForge -d postgress -c "SELECT l.name AS linha, l.color, c.sequence, s.name AS estacao, s.position_x, s.position_y FROM line l JOIN conection c ON c.id_line = l.id JOIN station s ON s.id = c.id_station WHERE s.description = 'RailForge mock: 20 estacoes / 4 linhas' ORDER BY l.id, c.sequence;"
```

A consulta deve retornar 20 linhas: cinco estações por linha ferroviária, em sequência. Os IDs são gerados pelo banco e podem variar; o SQL usa `RETURNING id` para criar os vínculos corretamente, sem assumir IDs fixos.

## Reexecução e dados existentes

O script preserva os cadastros existentes e não executa exclusões. Uma nova execução é recusada se os nomes das linhas mock ou a descrição identificadora já estiverem presentes; não duplica a carga nem completa uma carga modificada manualmente.

Se uma posição X/Y já estiver ocupada e a restrição de unicidade do modelo estiver instalada no banco, a carga falhará e será revertida. Nesse caso, escolha posições livres no SQL antes de executar novamente. Não remova dados existentes para abrir espaço. Não é necessário reiniciar o banco após a carga.

Este script fornece dados para o mapa; ele não corrige a rota `/map` nem implementa sua renderização. Os comandos acima são instruções de execução e não foram executados durante a criação destes arquivos.
