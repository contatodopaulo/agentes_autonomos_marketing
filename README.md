# Sistema de Agentes Autônomos de Marketing

Sistema automatizado com 4 agentes de IA conectados à API da OpenAI para criação de conteúdo de marketing digital.

## Estrutura do Sistema

O sistema é composto por 4 agentes que trabalham em sequência:

1. **Agente Escritor** - Gera blog posts baseados em títulos
2. **Agente Editor** - Revisa e fornece feedback estruturado
3. **Agente Revisor** - Aplica as sugestões do editor
4. **Agente LinkedIn** - Gera posts para LinkedIn baseados nos blog posts finais

## Instalação

1. Clone o repositório ou navegue até o diretório do projeto

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure a API Key da OpenAI:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione: `OPENAI_API_KEY=your_api_key_here`
   - Ou configure como variável de ambiente

## Uso

1. Prepare o arquivo `ideias.csv` com uma coluna chamada `titulo`:
```csv
titulo
Como criar conteúdo de marketing que converte
Inteligência Artificial no Marketing Digital
```

2. Execute o orquestrador:
```bash
python orquestrador.py
```

3. O sistema processará cada linha do CSV sequencialmente, gerando:
   - Rascunhos em `intermediarios/drafts/`
   - Feedbacks em `intermediarios/feedbacks/`
   - Revisões em `intermediarios/revisoes/`
   - Blog posts finais em `blog_posts_finais/`
   - Posts do LinkedIn em `linkedin_posts/`

## Estrutura de Pastas

```
agentes_autonomos_marketing/
├── agente_escritor/          # Agente que gera blog posts
├── agente_editor/            # Agente que revisa conteúdo
├── agente_revisor/           # Agente que aplica revisões
├── agente_linkedin/          # Agente que gera posts LinkedIn
├── intermediarios/           # Arquivos intermediários
│   ├── drafts/              # Rascunhos originais
│   ├── feedbacks/           # Feedbacks do editor
│   └── revisoes/            # Versões revisadas
├── blog_posts_finais/       # Blog posts finais
├── linkedin_posts/           # Posts do LinkedIn
├── orquestrador.py          # Arquivo principal
├── ideias.csv               # CSV com títulos
└── requirements.txt         # Dependências Python
```

## Configuração dos Agentes

Cada agente possui um arquivo `config.py` com os prompts utilizados. Você pode editar esses arquivos para ajustar o comportamento de cada agente:

- `agente_escritor/config.py` - Prompt para geração de blog posts
- `agente_editor/config.py` - Prompt para revisão editorial
- `agente_revisor/config.py` - Prompt para aplicação de revisões
- `agente_linkedin/config.py` - Prompt para posts do LinkedIn

## Características

- ✅ Processamento sequencial linha por linha do CSV
- ✅ Saída verbosa no terminal para cada etapa
- ✅ Salvamento de arquivos intermediários
- ✅ Formato markdown para todos os arquivos gerados
- ✅ Tratamento de erros com mensagens claras
- ✅ Sanitização automática de títulos para nomes de arquivo

## Requisitos

- Python 3.8+
- API Key da OpenAI
- Bibliotecas Python: `openai`, `pandas`, `python-dotenv`

