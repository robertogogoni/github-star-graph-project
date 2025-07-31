# GitHub Star Graph

Este projeto oferece um roteiro completo para transformar a lista de repositórios que você marcou com estrela em **visualizações interativas** e **insights acionáveis**. A proposta é começar pequeno—extraindo e classificando seus repositórios favoritos—e evoluir gradualmente para uma solução avançada que inclua enriquecimento com IA, grafos de similaridade, integração com repositórios em alta e atualizações automatizadas. Tudo é documentado para que você acompanhe o raciocínio, as escolhas e os resultados ao longo do caminho.

## Objetivos

O repositório tem como metas principais:

* **Centralizar scripts e ferramentas** para coletar, enriquecer e classificar seus repositórios estrelados e também consultar projetos em alta.
* **Registrar o processo de tinkering**: cada passo, hipótese e ajuste é descrito em `docs/PROCESS.md` para que outras pessoas (e você no futuro) possam entender como as decisões foram tomadas.
* **Permitir evolução incremental**: você pode adicionar novas funcionalidades (por exemplo, coleta de tópicos, clustering semântico, modelagem de grafos) sem perder contexto, pois o projeto está organizado em módulos e etapas bem definidas.
* **Promover boas práticas**: o README segue convenções recomendadas, explica claramente como usar os scripts e alerta para cuidados de segurança como o uso de tokens.

## Versão Mínima Viável (MVP)

O ponto de partida consiste em obter os dados básicos dos repositórios que você marcou com estrela e classificá‑los por linguagem, domínio e tipo. Isso fornece uma visão panorâmica do seu perfil técnico e ajuda a planejar a visualização posterior. Nesta fase você precisará apenas de um token de acesso com permissão de leitura pública (`public_repo`).

Os scripts principais são:

1. `scripts/export_github_stars.py` – Exporta todos os repositórios que você marcou com estrela. Lê o token de acesso pessoal (PAT) da variável de ambiente `GITHUB_TOKEN` e grava um arquivo `starred_repos.json` com os detalhes básicos de cada repositório.
2. `scripts/classify_repos.py` – Recebe o JSON exportado e gera um arquivo CSV com as colunas `Área de Domínio`, `Tipo de Projeto`, `Subdomínio`, `Linguagem`, `Repositório`, `Descrição` e `URL`. A classificação utiliza listas estendidas de palavras‑chave para mapear cada repositório a categorias técnicas e de negócio.

### Executando o MVP

1. **Crie um ambiente Python isolado (opcional)**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Instale as dependências** listadas em `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Defina a variável de ambiente `GITHUB_TOKEN`** com seu PAT (no fish shell, por exemplo):

   ```fish
   set -x GITHUB_TOKEN "seu_token"
   ```

4. **Execute o script de exportação** para baixar todos os repositórios que você estrelou:

   ```bash
   python scripts/export_github_stars.py
   ```

5. **Classifique os repositórios** usando listas estendidas de palavras‑chave para identificar domínio, tipo e subdomínio:

   ```bash
   python scripts/classify_repos.py starred_repos.json starred_repos_refined.csv
   ```

6. **Analise os resultados**: abra o CSV gerado em uma planilha (Excel, LibreOffice ou Google Sheets) e explore as colunas `Área de Domínio`, `Tipo de Projeto`, `Subdomínio`, `Linguagem`, etc.

## Evolução Planejada

Com o MVP estabelecido, você poderá avançar em etapas incrementais. Algumas sugestões:

1. **Enriquecer com tópicos** – O script `scripts/fetch_repo_topics.py` consulta a API do GitHub para obter as tags atribuídas pelos mantenedores. Esses metadados ajudam a refinar categorias e identificar relações entre projetos.
2. **Aplicar clustering semântico** – `scripts/cluster_repos.py` utiliza `TF‑IDF` e `KMeans` para agrupar descrições semelhantes. Isso revela padrões ocultos e cria uma base para visualizações por proximidade semântica.
3. **Modelar o grafo** – Converta os repositórios, tópicos e relações de similaridade em um grafo (JSON ou CSV). Essa estrutura pode ser importada para um banco de grafos (Neo4j) ou consumida por bibliotecas de visualização como D3.js ou Cytoscape.js.
4. **Integração com trending** – Adicione um módulo para coletar repositórios em alta (trending) e conectá‑los a seus repositórios estrelados por linguagem, tópicos ou dependências comuns.
5. **Automatizar e publicar** – Configure GitHub Actions para rodar esses scripts diariamente ou semanalmente. Use GitHub Pages ou outro serviço para hospedar a visualização interativa atualizada.
6. **Aplicar IA avançada** – Explore embeddings com `sentence-transformers` ou APIs de IA para calcular similaridade contextual, recomendações e sumarizações automáticas.

## Estrutura do Repositório

- `scripts/` – Contém os scripts Python utilizados nas etapas de coleta, enriquecimento, classificação e clustering.
- `docs/` – Arquivos de documentação, incluindo o processo de tinkering (`PROCESS.md`).
- `requirements.txt` – Lista de dependências Python.
- `.github/workflows/` – (Opcional) Contém configurações de automação via GitHub Actions para atualização contínua.

## Requisitos

* **Python 3.8 ou superior** – Os scripts usam recursos de versões recentes da linguagem.
* **Acesso à internet** – Necessário para chamadas à API do GitHub e, eventualmente, para baixar arquivos trending ou dependências.
* **Personal Access Token (PAT)** – O token deve ter o escopo mínimo de leitura de repositórios públicos (`public_repo`). Nunca o commit sua chave no repositório; mantenha‑o em uma variável de ambiente.

## Contribuindo

Este projeto incentiva uma mentalidade experimental (“tinkering”). Sugestões para colaborar:

* **Branches temáticos** – Crie ramos específicos para cada melhoria (ex.: `feature/clustering`, `feature/trending`, `ci/automacao`). Isso mantém o histórico organizado.
* **Mensagens de commit claras** – Explique o porquê de cada alteração. Isso ajuda a reconstruir a linha de raciocínio.
* **Atualize a documentação** – Sempre que experimentar algo novo, registre no arquivo `docs/PROCESS.md` o que foi feito, o que funcionou e o que pode ser melhorado.
* **Cuide da segurança** – Nunca exponha tokens ou credenciais. Utilize variáveis de ambiente e arquivos `.env` ignorados pelo git.