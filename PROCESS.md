# Processo de Tinkering

Este documento serve como diário de bordo do projeto, registrando
decisões, tentativas, erros e aprendizados ao longo da evolução da
aplicação de visualização de grafos para repositórios estrelados.

## 1. Exportação dos repositórios estrelados

- **Ferramenta utilizada**: script `export_github_stars.py` em Python.
- **Motivação**: o conector GitHub disponível no ambiente não
  oferecia um endpoint para listar estrelas. Recorremos à API
  pública do GitHub com paginação (`/users/{user}/starred`) e um
  PAT fornecido pelo usuário.
- **Resultado**: obtivemos um JSON com ~4 465 repositórios.

## 2. Classificação inicial

- **Objetivo**: categorizar rapidamente os repositórios por
  linguagem principal, tema e tipo de projeto usando heurísticas.
- **Método**: definimos dicionários de palavras‑chave para mapear
  descrições e nomes para grandes categorias (por exemplo,
  `Android`, `Web`, `DevOps`). Também identificamos se o projeto
  era uma biblioteca, framework, CLI etc.
- **Aprendizado**: essa abordagem ofereceu uma visão geral, mas
  deixou muitos projetos na categoria “Other” e não capturou
  subtemas.

## 3. Refinamento das Categorias

- **Melhorias**: expandimos as listas de palavras‑chave para
  domínios (por exemplo, `Data & AI`, `Security & Crypto`) e tipos
  (biblioteca, template, dataset). Incluímos subdomínios como
  `React`, `Docker`, `Kubernetes`.
- **Resultado**: geramos o arquivo `starred_repos_refined.csv` com
  colunas `Área de Domínio`, `Tipo de Projeto`, `Subdomínio`,
  proporcionando uma visão mais granular.

## 4. Clustering Semântico

- **Objetivo**: descobrir agrupamentos naturais nos dados sem
  depender de listas pré‑definidas de palavras‑chave.
- **Método**: usamos TF‑IDF para vetorização das descrições e
  `KMeans` (20 clusters) para agrupar os projetos. Identificamos
  palavras‑chave dominantes em cada cluster para rotulá‑los.
- **Resultado**: arquivo `starred_repos_clusters.csv` que associa
  cada repositório a um cluster e lista as palavras mais comuns do
  grupo.
- **Observações**: clusters revelaram comunidades interessantes,
  como ferramentas de design, wrappers de APIs, listas “awesome” e
  utilitários de produtividade.

## 5. Enriquecimento com tópicos (a executar localmente)

- **Desafio**: a API para tópicos dos repositórios (`/topics`) não
  é acessível diretamente no ambiente de execução atual. Preparou‑se
  o script `fetch_repo_topics.py` para ser executado localmente,
  adicionando a lista de `topics` a cada registro.
- **Próximos passos**: uma vez enriquecido o JSON, a classificação
  poderá usar esses rótulos para uma categorização ainda mais
  precisa.

## 6. Próximas Evoluções

1. **Grafo de Conexões**: modelar relações entre repositórios
   (compartilham tópicos, dependências ou alta similaridade) e
   construir um grafo no Neo4j ou arquivo JSON para visualização.
2. **Integração com Repositórios Trending**: coletar projetos em
   alta regularmente e integrá‑los ao grafo para identificar
   conexões com suas estrelas atuais.
3. **Automação**: configurar GitHub Actions para rodar os scripts
   periodicamente e manter a visualização sempre atualizada.

Este processo é iterativo; novas ideias e melhorias devem ser
registradas aqui à medida que forem implementadas.