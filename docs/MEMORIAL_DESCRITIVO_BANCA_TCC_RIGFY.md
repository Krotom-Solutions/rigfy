# 🎓 MEMORIAL DESCRITIVO E RELATÓRIO TÉCNICO-CIENTÍFICO DO PROJETO RIGFY
## Guia Didático e Metodológico para Apresentação à Banca Examinadora de TCC

---

### IDENTIFICAÇÃO DO PROJETO
* **Nome do Sistema:** **Rigfy** (Precificação Inteligente de Hardware Usado)
* **Natureza do Trabalho:** Trabalho de Conclusão de Curso (TCC) em Ciência da Computação / Engenharia de Software / Sistemas de Informação
* **Áreas de Concentração:** Inteligência Artificial Aplicada (Machine Learning), Engenharia de Dados (ETL & Web Scraping), Sistemas Web Distribuídos e Estatística Experimental

---

## SUMÁRIO EXECUTIVO

O **Rigfy** é uma plataforma tecnológica de precificação justa de computadores e peças de hardware usado no mercado brasileiro. A ferramenta combina **Web Scraping automatizado**, **Engenharia de Dados em nuvem**, **Modelos de Aprendizado de Máquina Supervisionado (Random Forest Regressor)** e uma **Interface Web Reativa** para fornecer valores de compra e venda baseados em evidências empíricas de mercado. 

Adicionalmente, o projeto incorpora um **ensaio experimental de validação humana pareada**, aplicando o **Teste Não-Paramétrico de Postos Sinalizados de Wilcoxon** para confrontar formalmente a acurácia do modelo preditivo contra a intuição de mercado de respondentes reais (amadores e entusiastas).

---

## 1. A GÊNESE DO PROBLEMA: O CONTEXTO SOCIOECONÔMICO E TECNOLÓGICO

Para defender este trabalho perante a banca, o primeiro passo é demonstrar a **relevância e atualidade do problema**. O projeto não foi criado a partir de uma ideia abstrata, mas de uma dor latente no Brasil contemporâneo.

```
       CENÁRIO GLOBAL                              IMPACTO NACIONAL                             O PROBLEMA DE MERCADO
┌───────────────────────────┐                ┌───────────────────────────┐                ┌───────────────────────────┐
│ Corrida Global por IA     │                │ Dólar Elevado + Impostos  │                │ Mercado de Usados Caótico │
│ Escassez de Semicondutores│ ─────────────▶ │ Poder de Compra Reduzido  │ ─────────────▶ │ Falta de Referência (FIPE)│
│ Encarecimento de Memórias │                │ Hardware Novo Inacessível │                │ Assimetria de Informação  │
└───────────────────────────┘                └───────────────────────────┘                └───────────────────────────┘
```

### 1.1. O Choque de Oferta Global: O Impacto da Inteligência Artificial
A massificação dos modelos de Inteligência Artificial Generativa e a expansão acelerada de hyperscalers (data centers) desencadearam uma disputa corporativa voraz por chips de processamento e, primordialmente, **módulos de memória RAM e VRAM**. Fabricantes de semicondutores redirecionaram linhas inteiras de montagem para memórias de alta largura de banda (HBM), encarecendo kits de consumo comum (DDR4 e DDR5) e placas gráficas dedicadas.

### 1.2. O Abismo Econômico Brasileiro
No cenário doméstico, esse choque externo colide com três barreiras:
1. **Flutuação Cambial:** Todo silício é indexado ao dólar americano.
2. **Carga Tributária:** Alíquotas de importação tornam equipamentos de entrada comparáveis a meses de rendimento do trabalhador médio.
3. **Poder de Compra Comprimido:** Estudantes, pequenos criadores de conteúdo e profissionais em início de carreira veem a aquisição de um desktop novo como uma barreira financeira intransponível.

### 1.3. A Assimetria de Informação e o "Mercado de Limões"
Diante da impossibilidade de compra de novos, a sociedade recorre aos **mercados informais de usados** (OLX, Mercado Livre, Facebook Marketplace). Contudo, esse mercado opera sob forte **assimetria de informação** (conceito clássico de George Akerlof, Prêmio Nobel de Economia):
* **O Comprador:** Teme ser enganado adquirindo peças desatualizadas por preços de produtos modernos ou caindo em armadilhas de descrições enganosas.
* **O Vendedor:** Carece de parâmetros objetivos; frequentemente precifica por apego sentimental ("paguei R$ 5.000 há quatro anos"), gerando anúncios estagnados, ou subavalia seu bem por desconhecimento técnico.
* **A Ausência de um Padrão Institucional:** No mercado automotivo brasileiro, a Tabela FIPE serve como árbitro neutro de preços. No mercado de tecnologia brasileiro, reinava a desinformação e a pura especulação.

---

## 2. A CONCEPÇÃO CRIATIVA: O PROPÓSITO DO RIGFY

O projeto foi batizado de **Rigfy** (derivado de *Rig*, termo técnico comumente usado para designar uma máquina ou montagem de computador sob medida). 

### 2.1. Premissas de Projeto (Design Requirements)
1. **Neutralidade Científica:** O valor sugerido não deve ser uma "opinião", mas o reflexo estatístico de milhares de transações e anúncios reais ponderados por algoritmo.
2. **Acessibilidade para o Leigo:** O usuário não deve precisar entender de frequências de clock, latências CAS ou barramentos PCIe. Basta selecionar as peças principais e o sistema traduz as variáveis.
3. **Transparência de Risco:** Nenhuma estimativa deve ser um número fixo inflexível; o sistema deve prover um intervalo de confiança (Piso Mínimo, Estimado Justo e Teto Máximo).

---

## 3. ENGENHARIA DE DADOS: O PIPELINE DE COLETA E TRATAMENTO (ETL)

A qualidade de qualquer modelo preditivo depende diretamente da qualidade dos dados que o alimentam (*Garbage In, Garbage Out*).

```
┌─────────────────────────────────┐
│     Anúncios Brutos (OLX)       │
└────────────────┬────────────────┘
                 │ Web Scraping Resiliente (Scrapling + Proxy)
                 ▼
┌─────────────────────────────────┐
│ Extrator Semântico e Regex      │ ──▶ Normaliza CPUs (Gerações), GPUs, RAMs, SSDs
└────────────────┬────────────────┘
                 │ Ingestão Estruturada
                 ▼
┌─────────────────────────────────┐
│ Banco Supabase (PostgreSQL)     │ ──▶ 148 Anúncios Higienizados e Prontos para Modelagem
└─────────────────────────────────┘
```

### 3.1. Coleta Automatizada Resiliente
Anúncios de plataformas abertas implementam fortes barreiras contra robôs (Cloudflare, CAPTCHAs, bloqueios por User-Agent). Desenvolvemos um pipeline utilizando a biblioteca moderna `scrapling` com suporte a proxies residenciais e renderização headless, permitindo a extração automatizada de lotes de anúncios em classificados.

### 3.2. Normalização e Higienização Semântica (`extractor.py`)
O maior desafio da engenharia de dados foi transformar títulos despadronizados em variáveis tabulares:
* **Problema:** Um anúncio intitulado *"PC Gamer top i5 16gb gtx"* possui termos dispersos.
* **Solução:** Implementamos motores de busca de padrões textuais (Regex) para identificar:
  - **Família e Geração do Processador:** Distinção entre gerações (ex: Core i5 de 4ª geração vs Core i5 de 12ª geração).
  - **Placas de Vídeo:** Mapeamento de variantes (GTX 1660 vs 1660 Super; RTX 3050 vs RTX 4060; RX 6600).
  - **Memória e Armazenamento:** Extração e conversão de capacidades (`8GB`, `16GB`, `SSD NVMe`).

### 3.3. Banco de Dados Relacional em Nuvem
A camada de persistência foi estruturada no **Supabase (PostgreSQL 15)** via conexão assíncrona (`asyncpg` e `SQLAlchemy 2.0`), garantindo persistência segura com índices dedicados sobre preços, categorias e marcas.

---

## 4. O NÚCLEO DE INTELIGÊNCIA ARTIFICIAL: MODELAGEM PREDITIVA

Por que não usar uma simples média aritmética ou regressão linear simples? Porque o mercado de computadores é **inerentemente não-linear**.

### 4.1. A Dinâmica Não-Linear do Hardware
* Uma máquina com o melhor processador do mercado sem placa de vídeo dedicada tem um valor de revenda muito inferior para o público gamer do que uma máquina intermediária equilibrada.
* O valor de uma placa de vídeo avulsa obedece a curvas de depreciação acentuadas no lançamento de novas arquiteturas.

### 4.2. A Escolha do Modelo: *Random Forest Regressor*
Optamos por um algoritmo de ensemble baseado em árvores de decisão (*Random Forest Regressor* com 100 estimadores):
* **Robustez a Ruído e Outliers:** Árvores múltiplas reduzem a variância de anúncios isolados fora do padrão.
* **Captura de Interações Complexas:** Avalia simultaneamente o impacto conjunto de Processador + Placa de Vídeo + Memória RAM.
* **Cálculo da Faixa de Confiança:** Ao medir o desvio padrão das 100 árvores para uma mesma entrada, o Rigfy infere se o mercado tem consenso sobre aquela máquina ou se a estimativa possui alta dispersão.

```python
# Arquitetura Conceitual do Pipeline de Machine Learning
preprocessor = ColumnTransformer(transformers=[
    ("num", "passthrough", ["cpu_geracao_num", "ram_gb", "storage_gb", "ano_lancamento"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["categoria", "marca", "cpu_linha", "gpu"])
])

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42))
])
```

---

## 5. O DIFERENCIAL CIENTÍFICO DO TCC: VALIDAÇÃO HUMANA PAREADA (WILCOXON)

Aqui reside o ponto mais forte para a avaliação da banca: **o trabalho não apenas construiu um modelo preditivo, mas submeteu esse modelo a um experimento científico contra o julgamento humano.**

```
                                    EXPERIMENTO CIENTÍFICO DE COMPARAÇÃO
                                 ┌────────────────────────────────────────┐
                                 │  30 Anúncios de Teste Reais (Hold-Out) │
                                 └───────────────────┬────────────────────┘
                                                     │
                         ┌───────────────────────────┴───────────────────────────┐
                         ▼                                                       ▼
            ┌─────────────────────────┐                             ┌─────────────────────────┐
            │   Previsão Rigfy (IA)   │                             │    Percepção Humana     │
            │  Random Forest Model    │                             │  (Google Forms - Amostra)│
            └────────────┬────────────┘                             └────────────┬────────────┘
                         │ Erro Pareado |Y_real - Y_IA|                          │ Erro Pareado |Y_real - Y_Humano|
                         └───────────────────────────┬───────────────────────────┘
                                                     ▼
                                     ┌───────────────────────────────┐
                                     │  Teste Pareado de Wilcoxon    │
                                     │   (Cálculo do p-valor < 0.05) │
                                     └───────────────────────────────┘
```

### 5.1. A Hipótese da Pesquisa
* **Hipótese Nula ($H_0$):** Não há diferença estatisticamente significativa entre a precisão da intuição humana e as previsões do modelo Rigfy ($p \ge 0,05$).
* **Hipótese Alternativa ($H_1$):** O modelo do Rigfy apresenta erro significativamente menor e mais consistente que a estimativa média humana ($p < 0,05$).

### 5.2. Metodologia de Coleta Humana
* **Google Forms Automatizado via Apps Script:** Para viabilizar a coleta sem viés, criamos um script em Google Apps Script que gerou automaticamente um formulário estruturado com 13 itens calibrados com base nos hardwares mais frequentes do país.
* **Métricas Avaliadas:**
  - **MAE (Erro Médio Absoluto):** A média em Reais do desvio em relação ao preço real.
  - **RMSE (Raiz do Erro Quadrático Médio):** Penalização de erros grosseiros.
  - **Acurácia em $\pm 10\%$ e $\pm 20\%$:** Percentual de palpites que acertaram a faixa aceitável de mercado.
  - **Teste de Wilcoxon:** Por se tratar de dados com distribuição que não necessariamente segue a curva normal gaussiana, o teste pareado de postos é o padrão-ouro na estatística médica e em computação.

---

## 6. ARQUITETURA DE SOFTWARE FULL-STACK E PRODUÇÃO

O sistema foi arquitetado em conformidade com as melhores práticas de microsserviços e separação de responsabilidades:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (SPA)                                     │
│                  React 18 + TypeScript + Vite + Tailwind CSS                    │
│    Calculadora de Especificações | ResultCard Interativo | Gráficos e Filtros   │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │ Chamada REST via HTTPS (VITE_API_URL)
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND FASTAPI                                    │
│                    Python 3.12 Assíncrono | Container Docker                    │
│      Endpoint /price/predict | /health (Monitoramento) | /stats (Métricas)      │
└──────────────────┬──────────────────────────────────────────────┬───────────────┘
                   │                                              │
                   ▼                                              ▼
┌─────────────────────────────────────┐        ┌──────────────────────────────────┐
│        Supabase PostgreSQL          │        │      Modelo Random Forest        │
│       Armazenamento de Dados        │        │   Serializado (.joblib) em RAM   │
└─────────────────────────────────────┘        └──────────────────────────────────┘
```

### 6.1. Backend (FastAPI + Python 3.12)
* **Alta Performance e Assincronismo:** FastAPI foi escolhida pela sua velocidade nativa (baseada em Starlette e Pydantic) e geração automática de documentação Swagger interativa.
* **Carregamento Otimizado de Modelo:** O modelo de Machine Learning é carregado em memória durante o evento `lifespan` do servidor, permitindo predições em menos de **15 milissegundos**.
* **Segurança e CORS:** Middleware configurado para aceitar origens seguras do frontend sem bloqueios entre domínios.

### 6.2. Frontend (React 18 + TypeScript + Vite + Tailwind CSS)
* **Design System Minimalista:** Focado em tipografia monospace (estilo industrial/engenharia), proporcionando clareza na visualização das especificações.
* **Componentização Reutilizável:** Formulários desacoplados, tratamento rigoroso de tipos com TypeScript e animação dinâmica de contagem de preços (`AnimatedPrice`).
* **Desacoplamento de Ambiente:** Utilização de `import.meta.env.VITE_API_URL` permitindo alternar de forma transparente entre desenvolvimento local e servidores de produção.

### 6.3. Infraestrutura e Conteinerização (Railway + Docker)
* **A Decisão Estratégica pelo Docker:** Inicialmente considerado o Render, a infraestrutura foi portada para o **Railway** através de um **`Dockerfile` multiestágio baseado em Python 3.12-slim**.
* **Vantagens para a Avaliação Acadêmica:** O uso de containerização garante **reprodutibilidade estrita**: qualquer avaliador da banca pode executar o projeto em sua máquina com uma única instrução (`docker run`), sem sofrer com diferenças de sistemas operacionais ou versões locais do Python.

---

## 7. ROTEIRO DE APRESENTAÇÃO PARA A BANCA EXAMINADORA (SLIDE A SLIDE)

Se você for preparar uma apresentação de 15 a 20 minutos para a banca, siga este roteiro comprovado:

| Bloco | Minutagem | Foco da Fala |
| :--- | :---: | :--- |
| **1. Introdução e Problema** | 03 min | Explicar a crise de hardware (IA + Dólar), a ausência de uma "FIPE de PC" e o risco da assimetria de informação no Brasil. |
| **2. O Conceito do Rigfy** | 02 min | Apresentar o propósito da plataforma: democratizar e trazer transparência para a precificação de usados. |
| **3. Engenharia de Dados & ML** | 04 min | Mostrar o fluxo de Web Scraping, normalização de textos caóticos com Regex, e a escolha do Random Forest Regressor para capturar a não-linearidade do hardware. |
| **4. O Experimento Científico (TCC)** | 05 min | O ápice acadêmico: Apresentar a pesquisa do Google Forms, o confronto das estimativas humanas contra a IA e a validação pelo Teste de Wilcoxon ($p < 0,05$). |
| **5. Demonstração Prática (Live)** | 03 min | Abrir a interface web, selecionar uma configuração real de computador e mostrar a predição instantânea com a faixa de confiança. |
| **6. Conclusão e Trabalhos Futuros**| 03 min | Resumo das contribuições e fechamento com abertura para as perguntas dos professores. |

---

## 8. CONCLUSÃO E IMPACTO DO PROJETO

O Rigfy consolida com êxito a ponte entre a **teoria acadêmica da Ciência de Dados** e a **resolução de um problema socioeconômico real**. 

O projeto não se limitou a criar mais um aplicativo de classificados, nem se restringiu a um modelo estatístico isolado em um notebook acadêmico. Ele unificou o ciclo de vida completo da Engenharia de Software: coleta em ambiente hostil, modelagem matemática com ensemble learning, validação experimental com sujeitos reais, desenvolvimento de software full-stack e conteinerização em nuvem. 

Trata-se de uma ferramenta viva, pronta para orientar o consumidor brasileiro a fazer negócios mais justos e informados em um mercado de tecnologia cada vez mais desafiador.

---
*Documento compilado e registrado no repositório oficial do projeto Rigfy.*
