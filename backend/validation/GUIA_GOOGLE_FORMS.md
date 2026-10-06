# 📋 Guia de Criação Automática do Formulário (Google Forms - TCC Rigfy)

Este guia permite gerar o formulário completo do Google Forms em menos de 1 minuto usando o **Google Apps Script**.

---

### Passo a Passo

1. **Acesse o Google Apps Script:**
   - Entre em [https://script.google.com/home/start](https://script.google.com/home/start)
   - Clique no botão **"+ Novo projeto"** (canto superior esquerdo).

2. **Cole o Código:**
   - Apague qualquer código existente no editor (`myFunction`).
   - Abra o arquivo [`criar_formulario_google.gs`](file:///d:/Documentos/rigfy/backend/validation/criar_formulario_google.gs), copie todo o conteúdo e cole no editor do Google.

3. **Execute o Script:**
   - Clique no ícone de salvar (💾 ou `Ctrl+S`).
   - Clique no botão **"Executar"** (Run).
   - *Nota de Permissão:* Na primeira vez, o Google solicitará permissão para criar formulários no seu Google Drive:
     - Clique em *Revisar permissões* -> Escolha sua conta -> Clique em *Avançado* -> *Acessar [Nome do Projeto] (não seguro)* -> *Permitir*.

4. **Pegue os Links no Console:**
   - Na parte inferior da tela (no Registro de Execução / Logs), aparecerão dois links:
     - 🔗 **Link de Edição:** Abra para adicionar as fotos de cada hardware.
     - 🔗 **Link Público:** Compartilhe com colegas, amigos e grupos para coletar respostas.

---

### Como Adicionar as Imagens no Google Forms

1. Abra o **Link de Edição** gerado pelo script.
2. Em cada uma das 13 perguntas de hardware, passe o mouse sobre a pergunta e clique no ícone de imagem (🖼️) ao lado do título.
3. Faça o upload da foto do hardware (ou pesquise direto na busca de imagens do Google dentro do próprio Forms).

---

### Como Importar as Respostas para o Rigfy

1. Na aba **Respostas** do Google Forms, clique no ícone verde **"Vincular ao Planilhas"** (Google Sheets).
2. Na planilha que abrir, vá em:
   `Arquivo` -> `Fazer download` -> `Valores separados por vírgula (.csv)`.
3. Salve o arquivo como `backend/validation/formulario_humano.csv`.
4. Execute o script do projeto:
   ```bash
   python backend/scripts/computar_humano.py
   ```
5. O script calculará automaticamente o **MAE, RMSE, MAPE e o Teste de Postos de Wilcoxon (p-valor)** comparando o Rigfy contra os humanos!
