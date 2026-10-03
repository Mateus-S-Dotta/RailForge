# RailForge — documentação do projeto

Documentação atualizada em 03/10/2026 a partir do código da pasta de trabalho. O escopo de cadastros e mapa está concluído: o backend fornece a rede por `GET /map`, e o frontend desenha as linhas e estações em SVG. Este documento descreve a implementação atual, substituindo o plano anterior. O manual de uso está em [README.md](README.md).

## Objetivo e tecnologias

O sistema cadastra estações, linhas ferroviárias e conexões que determinam a participação e a ordem das estações em cada linha. O mapa é esquemático, baseado em coordenadas inteiras X/Y. Não há modelos de trens, horários, viagens ou cálculo de rotas de passageiros.

| Camada | Tecnologias | Fonte |
| --- | --- | --- |
| Backend | Python 3.12, FastAPI, Uvicorn, SQLAlchemy síncrono, Pydantic e driver PostgreSQL `psycopg[binary]`. `python-dotenv` é dependência declarada. | [api/Dockerfile](api/Dockerfile), [requirements.txt](api/requirements.txt), [schemas.py](api/app/schemas.py) |
| Banco | PostgreSQL 18, volume persistente, healthcheck. | [bd/docker-compose.yml](bd/docker-compose.yml) |
| Frontend | Next.js 16.3.0, React/React DOM 19.2.8, TypeScript 5, Tailwind CSS 4, Base UI, shadcn e utilitários de classes. | [package.json](frontend/package.json) |
| Execução | Docker Compose por camada, rede compartilhada `railForge_network`, imagens frontend com Node 24.14.0. | Compose e Dockerfiles de cada pasta |
| Mapa | SVG nativo com `line` e `circle`, sem biblioteca de mapas adicional. | [RailMap](frontend/components/railMap/index.tsx) |

As dependências Python não têm versões fixadas em `requirements.txt`; o frontend possui `package-lock.json`.

## Estrutura e responsabilidades

| Arquivo/pasta | Responsabilidade |
| --- | --- |
| [api/main.py](api/main.py) | Aplicação FastAPI, lifespan, CORS, rotas, injeção de sessão e respostas HTTP. |
| [api/app/database.py](api/app/database.py) | Engine síncrono, `Base`, `SessionLocal` e sessão por requisição, fechada em `finally`. Lê `DATABASE_URL` do ambiente. |
| [api/app/models.py](api/app/models.py) | Tabelas `station`, `line`, `conection`, chaves estrangeiras e restrições. |
| [api/app/schemas.py](api/app/schemas.py) | Schemas Pydantic de entrada, saída e resposta composta do mapa. |
| [api/app/crud.py](api/app/crud.py) | Persistência e consultas. `get_map` agrega estações e linhas com estações ordenadas. |
| [api/app/get_stations.py](api/app/get_stations.py) | Helper assíncrono de consulta por posição, sem uso nas rotas atuais; a rota ativa usa o CRUD síncrono. |
| [frontend/app/page.tsx](frontend/app/page.tsx) | Página cliente, menu lateral, estados dos formulários, carregamento de `/map` e integração com `RailMap`. |
| [frontend/app/constrants.ts](frontend/app/constrants.ts) | URL `http://localhost:8000/` e tipos `LineStation` e `MapLine` usados pelo mapa. |
| [frontend/components/railMap/index.tsx](frontend/components/railMap/index.tsx) | Renderização SVG a partir da propriedade `lines`. |
| [frontend/app/createEntities/forms.ts](frontend/app/createEntities/forms.ts) | Campos e endpoints dos três formulários. |
| [frontend/app/createEntities/createEntities.tsx](frontend/app/createEntities/createEntities.tsx) | `ElementForm`, inputs controlados e POST JSON. |
| [frontend/components/ui](frontend/components/ui), [frontend/lib/utils.ts](frontend/lib/utils.ts) | Button/Input sobre Base UI e composição de classes. |
| [frontend/app/layout.tsx](frontend/app/layout.tsx), [globals.css](frontend/app/globals.css) | Layout, fontes Geist e tema escuro/Tailwind. |
| [frontend/next.config.ts](frontend/next.config.ts) | Build `standalone`; não define proxy da API. |
| [bd/mock.sql](bd/mock.sql), [bd/MOCK.md](bd/MOCK.md) | Carga de dados fictícios e instruções de execução no banco Docker. |
| [setup.ps1](setup.ps1), [setup.ps1.md](setup.ps1.md) | Inicialização local e comando para executar o projeto. |

O backend persiste os cadastros e fornece a ordem dos vínculos. O frontend consome os dados e define a geometria visual, sem alterar coordenadas persistidas.

## Inicialização, configuração e banco

Na raiz do projeto:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

O script inicia Docker Desktop, aguarda sua disponibilidade, sobe o banco, espera seu healthcheck, sobe a API, instala dependências frontend com uma imagem Node e executa `docker compose watch frontend-dev`. O terminal permanece ocupado pelo acompanhamento do frontend.

Os Compose usam a rede `railForge_network`. O banco se chama `postgress`; a API, `railforge_api`; o frontend de desenvolvimento, `railforge_frontend_dev`. As portas locais são 5432, 8000 e 3000 respectivamente. O banco utiliza volume nomeado `pgdata`.

Os Compose referenciam `api/.env` e `frontend/.env`. A API exige `DATABASE_URL`; `database.py` não chama `load_dotenv`. Para a conexão local síncrona, usar o driver `postgresql+psycopg` e host `postgress`. O CORS permite todas as origens, métodos e headers quando `ENVIRONMENT=dev` (padrão), sem credenciais.

Não há migrações Alembic no repositório. O lifespan executa `Base.metadata.create_all(bind=engine)`, criando tabelas ausentes; isso não altera tabelas já existentes. Restrições descritas nos modelos dependem de terem sido criadas no banco utilizado.

[frontend/AGENTS.md](frontend/AGENTS.md), referenciado por `CLAUDE.md`, exige consultar os guias locais de Next.js em `node_modules/next/dist/docs/` antes de escrever código frontend. [bd/README.md](bd/README.md) contém exemplos históricos com outra rede e driver assíncrono; os Compose atuais e o código síncrono são a referência de execução.

## Cadastros e relacionamentos

A definição persistente está em [models.py](api/app/models.py), os contratos em [schemas.py](api/app/schemas.py), e os campos da tela em [forms.ts](frontend/app/createEntities/forms.ts).

### Estação (`station`)

| Campo | Contrato e persistência |
| --- | --- |
| `id` | Inteiro, chave primária gerada pelo banco. |
| `name` | String obrigatória; coluna de até 255 caracteres. |
| `description` | String opcional/nula; coluna de até 1000 caracteres. |
| `position_x`, `position_y` | Inteiros obrigatórios nos schemas de criação/saída. Colunas permitem nulo; o par tem restrição de unicidade no modelo. |
| `created_at` | Data/hora com timezone, preenchida por `now()` no banco e retornada pela API. |

A tela exige nome e X/Y; descrição é opcional. Não há latitude/longitude nem validação de faixa de coordenadas. PATCH permite alterar parcialmente os campos enviados; o CRUD usa `exclude_unset=True`.

### Linha (`line`)

- `id`: inteiro, chave primária gerada pelo banco.
- `name`: obrigatório; coluna de até 255 caracteres e formulário obrigatório.
- `color`: opcional/nula; coluna de até 20 caracteres. O formulário sugere hexadecimal, mas não valida uma cor CSS.
- Não há unicidade de nome. PATCH permite atualização parcial de nome/cor.

### Conexão (`conection`)

- `id_station`: inteiro obrigatório, FK para `station.id`.
- `id_line`: inteiro obrigatório, FK para `line.id`.
- `sequence`: inteiro obrigatório e não nulo, usado para ordenar as estações na linha.
- Chave primária composta `(id_station, id_line)`: uma estação pode pertencer a várias linhas; não pode se repetir na mesma linha.
- Unicidade `(id_line, sequence)`: a ordem não pode se repetir dentro da linha. Não há exigência de sequência positiva, contínua ou iniciada em 1.
- O formulário exige `id_line`; `id_station` e `sequence` são inputs de texto sem `required`, mas os três campos são obrigatórios na API.

A grafia `Conection`/`conection`/`conections` é a utilizada pelo projeto. Não há PATCH de conexão, entidade de trecho, geometria intermediária ou configuração de exclusão em cascata. FKs podem impedir excluir estação/linha ainda vinculada.

### Fluxo e validações

Em `page.tsx`, o usuário escolhe Criar Estação, Criar Linha ou Criar Conexão; Cancelar volta ao menu. Os campos ficam em `form.result`. `ElementForm` envia POST JSON e limpa os campos depois que o `fetch` resolve. Os inputs armazenam strings; Pydantic converte valores compatíveis para os inteiros declarados.

A API valida campos/tipos e responde 422 para entradas inválidas. Comprimentos, FKs e unicidade dependem do banco; não há tratamento explícito de `IntegrityError` no CRUD, nem validação de nome não vazio ou cor. O formulário não verifica `response.ok` nem mostra confirmação/erro de cadastro.

Não há listagem, edição ou exclusão pela tela principal. Para obter IDs e conferir registros, usar as listagens da API ou `/docs`. `frontend/app/action.ts` e `components/loginTemplate/index.tsx` são estruturas remanescentes de login, sem autenticação ou cadastro de usuários implementado no backend.

## Endpoints e uso pelo frontend

Rotas em [api/main.py](api/main.py), sem prefixo `/api`; operações em [crud.py](api/app/crud.py).

| Método e rota | Resposta/comportamento | Uso pela tela |
| --- | --- | --- |
| `GET /` | Mensagem de API em execução. | Nenhum. |
| `GET /health/db` | Status/versão PostgreSQL; 500 em erro de conexão tratado. | Nenhum. |
| `POST /stations` | `StationCreate` → `StationOut`, 201. | Formulário de estação. |
| `GET /stations` | Array `StationOut`; `skip=0`, `limit=100`. | Consulta manual de IDs. |
| `GET /stations/by-position` | Faixas inclusivas `x_min`, `x_max`, `y_min`, `y_max` → estações. | Nenhum. |
| `GET /stations/{station_id}` | Estação ou 404. | Nenhum. |
| `PATCH /stations/{station_id}` | Atualização parcial ou 404. | Nenhum. |
| `DELETE /stations/{station_id}` | 204 sem corpo ou 404; sujeito às FKs. | Nenhum. |
| `POST /lines` | `LineCreate` → `LineOut`, 201. | Formulário de linha. |
| `GET /lines` | Array `LineOut`; `skip=0`, `limit=100`. | Consulta manual de IDs. |
| `GET /lines/{line_id}` | Linha ou 404. | Nenhum. |
| `PATCH /lines/{line_id}` | Atualização parcial ou 404. | Nenhum. |
| `DELETE /lines/{line_id}` | 204 sem corpo ou 404; sujeito às FKs. | Nenhum. |
| `POST /conections` | `ConectionCreate` → `ConectionOut`, 201. | Formulário de conexão. |
| `GET /conections` | Array de conexões; `skip=0`, `limit=100`. | Nenhum. |
| `GET /conections/{id_station}/{id_line}` | Conexão ou 404. | Nenhum. |
| `DELETE /conections/{id_station}/{id_line}` | 204 sem corpo ou 404. | Nenhum. |
| `GET /map` | `MapResponse` com todas as estações e linhas com estações ordenadas. | Carregado ao montar a página. |

Listagens não têm ordenação explícita nem validação de faixa para paginação. A consulta por posição não valida mínimo menor que máximo e é registrada antes da rota dinâmica de estação.

## Contrato do mapa — implementado

```http
GET http://localhost:8000/map
Accept: application/json
```

Exemplo ilustrativo de resposta HTTP 200, com IDs e data/hora fictícios:

```json
{
  "stations": [
    {"name":"Central","position_y":100,"position_x":100,"description":null,"id":1,"created_at":"2026-10-03T12:00:00Z"},
    {"name":"Mercado","position_y":100,"position_x":200,"description":null,"id":2,"created_at":"2026-10-03T12:01:00Z"}
  ],
  "lines": [
    {
      "name":"Linha Azul",
      "color":"#2563eb",
      "id":1,
      "stations":[
        {"station_id":1,"name":"Central","position_x":100,"position_y":100,"sequence":1},
        {"station_id":2,"name":"Mercado","position_x":200,"position_y":100,"sequence":2}
      ]
    }
  ]
}
```

[schemas.py](api/app/schemas.py) define `StationOut`, `LineStationOut`, `LineMapOut` e `MapResponse`. `get_map` executa três consultas: estações, linhas e conexões com JOIN de estação ordenadas por `id_line` e `sequence`. Agrupa as conexões por linha, instancia `LineMapOut` e retorna `MapResponse`. A construção anterior com `LineOut`, que perdia `stations`, foi corrigida.

- A lista mestra `stations` inclui estações sem vínculo e não repete estações.
- `lines` inclui linhas vazias com `stations: []`; estações compartilhadas aparecem nas listas das respectivas linhas com o mesmo `station_id`.
- As listas internas estão em ordem crescente de `sequence`; lacunas na numeração não interrompem o trajeto.
- `/map` não aplica o limite padrão de 100 das listagens. A ordem externa de linhas/estações não é garantida.
- `description` e `color` permitem `null`; X/Y e `sequence` são inteiros; `created_at` é serializado como string de data/hora.
- Banco vazio retorna `{"stations":[],"lines":[]}`. Não há campo separado de segmentos/geometria.

## Consumo e renderização — implementado

[page.tsx](frontend/app/page.tsx) busca `/map` em `useEffect`, verifica `response.ok`, lê o JSON e guarda somente `data.lines`. Usa `AbortController` no cleanup para evitar atualização após desmontagem. Mensagens de carregamento e falha são passadas ao componente. Os tipos `MapLine` e `LineStation` estão em [constrants.ts](frontend/app/constrants.ts).

[RailMap](frontend/components/railMap/index.tsx) recebe `lines: MapLine[]` e `message?: string`:

1. Reúne as estações contidas nas linhas e remove duplicatas por `station_id` para desenhar um único marcador por estação compartilhada.
2. Calcula os limites pelas coordenadas dessas estações, com margem de 30 unidades em cada lado, e usa `viewBox` e `preserveAspectRatio="xMidYMid meet"`. X cresce à direita e Y para baixo; suporta posições negativas, estações alinhadas e um único ponto.
3. Desenha cada trecho com `<line>` entre elementos consecutivos de `line.stations`, na ordem do array, sem reordenar no frontend ou fechar o trajeto.
4. Aplica stroke de largura 4 e a cor da linha; cor nula/vazia usa `#94a3b8`. Não há validação de cor CSS inválida.
5. Desenha os círculos depois dos trajetos: raio 7, preenchimento branco, borda `#334155`, largura 2.
6. Usa `<title>` nos grupos e círculos para nomes e IDs, visíveis ao passar o mouse; não desenha rótulos permanentes de nomes.
7. Sem estações vinculadas, usa `viewBox="0 0 600 400"` e `<text>` para mensagem de carregamento, erro ou mapa vazio. O SVG tem título e identificação acessível.

Todo o conteúdo do mapa é SVG (`svg`, `g`, `line`, `circle`, `title`, `text`). Não há elementos HTML usados para construir o desenho. Formulários e menu permanecem componentes HTML na página.

**Atualização dos dados:** `/map` é buscado ao montar a página. Cadastros não disparam nova busca automaticamente; é necessário recarregar a página para visualizar alterações. Não há botão de retry: recarregar também permite tentar novamente após falha.

Estações isoladas estão na resposta backend, mas não aparecem no desenho, porque o componente recebe somente `lines`. Uma linha com uma estação gera um círculo sem trecho; com duas ou mais, gera segmentos retos. Trechos sobrepostos podem cobrir uns aos outros.

A interface antiga `stationInterface` ainda existe em `constrants.ts`, com `id_linha` e descrição não anulável, mas não é utilizada pelo mapa; seus tipos ativos são `LineStation`/`MapLine`. Não foi introduzida biblioteca de mapas, estado global, mapa geográfico, zoom, edição por arraste ou roteamento.

## Dados mock

[bd/mock.sql](bd/mock.sql) insere 20 estações, quatro linhas e 20 conexões, em transação. Cada linha possui cinco estações com sequência de 1 a 5, X de 100 a 500 e Y fixo em 100, 200, 300 ou 400. Cores: azul, verde, vermelha e amarela. As linhas não compartilham estações.

IDs são obtidos com `RETURNING`, sem valores fixos. Nomes de linha e descrição identificadora detectam carga anterior e recusam reexecução; o script não apaga dados. Colisão de coordenadas pode impedir a carga pela restrição de unicidade. Requer tabelas já criadas pela API. Comandos de execução e consulta estão em [bd/MOCK.md](bd/MOCK.md) e no manual [README.md](README.md).

## Verificações realizadas e limites

Durante a implementação, `/map` foi consultado no container e retornou HTTP 200 com 20 estações e quatro linhas. Foram conferidos os campos do contrato e a ordenação das estações por `sequence`.

No frontend, lint passou sem erros, com aviso em `tailwind.config.ts`, e `tsc --noEmit --incremental false` passou. A renderização estática do componente confirmou segmentos na ordem do array, estações compartilhadas sem duplicação, mapa vazio, ponto único e uso exclusivo de elementos SVG. Esses checks foram executados durante a implementação; não foram repetidos nesta atualização documental. Não há suíte de testes específica declarada e não foi executado build de produção nessa verificação.

As limitações acima descrevem o produto atual; não constituem um plano de implementação pendente. O escopo solicitado de cadastros e visualização do mapa está entregue.
