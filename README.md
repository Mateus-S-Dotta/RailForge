# RailForge

Sistema para cadastrar estações e linhas ferroviárias e visualizar seus trajetos em um mapa SVG. As conexões indicam a qual linha cada estação pertence e sua ordem no trajeto.

## Rodar o projeto

Com Docker Desktop instalado e o comando `docker` disponível, abra um terminal na raiz do projeto e execute o comando de [setup.ps1.md](setup.ps1.md):

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

O script inicia o Docker Desktop, sobe o PostgreSQL, aguarda o banco ficar saudável, sobe a API e inicia o frontend em desenvolvimento. Mantenha esse terminal aberto: ele acompanha o frontend com `docker compose watch`.

Os Compose usam `api/.env` e `frontend/.env`; esses arquivos devem existir. A API exige `DATABASE_URL` apontando para o banco. Para o banco local deste projeto, a configuração em `api/.env` é:

```dotenv
DATABASE_URL=postgresql+psycopg://postgressRailForge:12345@postgress:5432/postgress
ENVIRONMENT=dev
```

O Compose do frontend exige `frontend/.env`, mesmo que não haja variáveis adicionais a configurar. As portas 3000, 8000 e 5432 precisam estar disponíveis.

Quando os serviços estiverem prontos, acesse:

- Aplicação: [http://localhost:3000](http://localhost:3000).
- Documentação interativa da API: [http://localhost:8000/docs](http://localhost:8000/docs).
- Verificação do banco: [http://localhost:8000/health/db](http://localhost:8000/health/db).

## Montar uma linha no mapa

1. Clique em **Criar Estação**. Informe nome, posição X e posição Y; a descrição é opcional. Por exemplo, cadastre Central em `(100, 100)`.
2. Clique em **Cancelar** para voltar ao menu e depois em **Criar Linha**. Informe um nome e, se desejar, uma cor hexadecimal, como `#2563eb`.
3. Consulte os IDs criados em [GET /stations](http://localhost:8000/stations) e [GET /lines](http://localhost:8000/lines). Use os IDs reais retornados, sem assumir que começam em 1.
4. Em **Criar Conexão**, preencha **Linha Id**, **Estação Id** e **Número na sequencia**. Essa conexão diz que a estação pertence à linha e ocupa, por exemplo, a posição `1`.
5. Cadastre outra estação, por exemplo Mercado em `(200, 100)`, e conecte-a à mesma linha com sequência `2`.
6. **Recarregue a página** para visualizar o mapa atualizado. As duas estações aparecerão como círculos ligados por uma linha reta.

Repita o cadastro de estações e conexões, aumentando a sequência para `3`, `4` e assim por diante. Para uma nova linha, crie outro cadastro de linha e use seu ID nas conexões.

Uma estação vinculada gera um círculo; são necessárias **pelo menos duas estações na mesma linha** para aparecer um trecho. Estações sem conexão não aparecem no mapa. X cresce para a direita e Y para baixo; o mapa se ajusta automaticamente ao espaço disponível.

Não repita o par X/Y entre estações, nem a sequência dentro da mesma linha. Uma estação pode participar de linhas diferentes, mas não pode ser cadastrada duas vezes na mesma linha. Ao passar o mouse sobre círculos ou trajetos, o mapa mostra nomes e IDs.

## Iniciar com dados mock

Como alternativa aos cadastros manuais, [bd/mock.sql](bd/mock.sql) cria **20 estações, 4 linhas e todas as 20 conexões**, com cinco estações ordenadas por linha. Não é preciso cadastrar conexões adicionais para desenhar esses trajetos.

Depois de iniciar o projeto e a API criar as tabelas, abra outro terminal na raiz do projeto:

```powershell
 docker cp .\bd\mock.sql postgress:/tmp/railforge-mock.sql
 docker exec postgress psql -U postgressRailForge -d postgress -v ON_ERROR_STOP=1 -f /tmp/railforge-mock.sql
```

Recarregue a aplicação para ver as quatro linhas. O script preserva os cadastros existentes, executa em uma transação e recusa uma carga repetida. Se alguma coordenada já estiver ocupada, escolha posições livres no SQL. Instruções de conferência estão em [bd/MOCK.md](bd/MOCK.md).

## Se o mapa não aparecer

- Recarregue a página depois de cadastrar dados ou executar o mock: o mapa é carregado ao abrir a página.
- Confira se as estações têm conexões e se a linha tem pelo menos duas estações para desenhar um trecho.
- Consulte [GET /map](http://localhost:8000/map) para conferir os dados e a ordem retornados pelo backend.
- Se aparecer “Não foi possível carregar o mapa”, confira a API e o banco:

```powershell
 docker logs railforge_api --tail 50
 docker compose -f .\bd\docker-compose.yml ps
```

Os formulários atuais não exibem confirmação de sucesso nem erros de cadastro. Para conferir se um registro foi salvo, consulte os endpoints de listagem ou a documentação interativa da API.

A documentação técnica, os modelos e o contrato do mapa estão em [PROJETO.md](PROJETO.md).
