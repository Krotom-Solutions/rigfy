/**
 * Script do Google Apps Script para criar automaticamente o formulário do TCC (Rigfy)
 * 
 * COMO USAR:
 * 1. Acesse: https://script.google.com/
 * 2. Clique em "Novo projeto" (ou "+ Novo script")
 * 3. Cole todo o código deste arquivo no editor
 * 4. Clique no ícone de disquete (Salvar) e depois em "Executar" (Run)
 * 5. Se o Google pedir autorização de acesso ao Google Drive / Forms, conceda
 * 6. Na aba "Registro de execução" (Logs), você verá o link para editar e o link público!
 */

function criarFormularioRigfyTCC() {
  const tituloForm = "Pesquisa de Percepção de Valor de Hardware Usado - Rigfy (TCC)";
  const descricaoForm = "Olá! Esta pesquisa faz parte de um Trabalho de Conclusão de Curso (TCC) sobre precificação de hardware usado no Brasil e inteligência artificial.\n\n" +
    "Objetivo: Entender a percepção humana sobre o valor de revenda de diferentes componentes e computadores usados no mercado nacional.\n\n" +
    "Instruções: Para cada item abaixo, informe apenas o valor numérico em Reais (R$) que você considera justo para compra/venda daquele item usado em bom estado de funcionamento.\n" +
    "Tempo estimado: 3 a 5 minutos.";

  // Cria o formulário no Google Drive
  const form = FormApp.create(tituloForm);
  form.setDescription(descricaoForm);
  form.setIsQuiz(false);
  form.setAllowResponseEdits(false);
  form.setProgressBar(true);

  // 1. Pergunta de Perfil / Nível de Conhecimento
  const itemPerfil = form.addMultipleChoiceItem();
  itemPerfil.setTitle("Qual é o seu nível de familiaridade com peças, computadores e preços de hardware?")
    .setChoiceValues([
      "Iniciante (uso o computador apenas para tarefas básicas do dia a dia)",
      "Intermediário (já pesquisei peças, comprei ou montei meu próprio computador)",
      "Avançado / Entusiasta (acompanho lançamentos, benchmarks e o mercado de usados frequentemente)"
    ])
    .setRequired(true);

  // 2. Lista de Hardwares Representativos para o Experimento
  const itens = [
    {
      id: "ITEM_01",
      categoria: "Placa de Vídeo (GPU)",
      titulo: "NVIDIA GeForce GTX 1060 6GB",
      specs: "6GB VRAM GDDR5 | 192-bit | Placa de entrada muito popular para jogos leves/eSports | Usada, funcionando perfeitamente."
    },
    {
      id: "ITEM_02",
      categoria: "Placa de Vídeo (GPU)",
      titulo: "NVIDIA GeForce GTX 1660 Super 6GB",
      specs: "6GB VRAM GDDR6 | 192-bit | Excelente custo-benefício para Full HD | Usada, com caixa original."
    },
    {
      id: "ITEM_03",
      categoria: "Placa de Vídeo (GPU)",
      titulo: "AMD Radeon RX 6600 8GB",
      specs: "8GB VRAM GDDR6 | Arquitetura RDNA 2 | Baixo consumo e ótimo desempenho em 1080p | Usada, 1 ano de uso."
    },
    {
      id: "ITEM_04",
      categoria: "Placa de Vídeo (GPU)",
      titulo: "NVIDIA GeForce RTX 3050 6GB/8GB",
      specs: "Suporte a Ray Tracing e DLSS | Ideal para notebooks e desktops intermediários | Usada."
    },
    {
      id: "ITEM_05",
      categoria: "Placa de Vídeo (GPU)",
      titulo: "NVIDIA GeForce RTX 4060 8GB",
      specs: "Geração atual Ada Lovelace | Suporte a DLSS 3 com Frame Generation | Usada em estado de nova."
    },
    {
      id: "ITEM_06",
      categoria: "Processador (CPU)",
      titulo: "AMD Ryzen 5 5600 (6 Núcleos / 12 Threads)",
      specs: "Socket AM4 | Frequência até 4.4GHz | 32MB Cache L3 | Um dos processadores mais vendidos no Brasil | Usado, sem cooler."
    },
    {
      id: "ITEM_07",
      categoria: "Processador (CPU)",
      titulo: "Intel Core i5 10400F (10ª Geração - 6 Núcleos / 12 Threads)",
      specs: "Socket LGA 1200 | Frequência até 4.3GHz | Processador intermediário Intel | Usado."
    },
    {
      id: "ITEM_08",
      categoria: "Processador (CPU)",
      titulo: "AMD Ryzen 7 5800X (8 Núcleos / 16 Threads)",
      specs: "Socket AM4 | Frequência até 4.7GHz | Focado em alto desempenho e multitarefa | Usado."
    },
    {
      id: "ITEM_09",
      categoria: "Notebook",
      titulo: "Notebook Lenovo / Acer Core i3 com 8GB RAM e SSD 256GB",
      specs: "Tela 15.6\" HD | Intel Core i3 (10ª ou 11ª Ger) | 8GB RAM | SSD 256GB | Bateria durando ~2h | Usado com marcas de uso leves."
    },
    {
      id: "ITEM_10",
      categoria: "Notebook",
      titulo: "Notebook Dell / Lenovo Core i5 com 16GB RAM e SSD 512GB",
      specs: "Tela 15.6\" Full HD | Intel Core i5 11ª/12ª Ger | 16GB RAM DDR4 | SSD 512GB NVMe | Gráficos Intel Iris Xe | Usado, excelente estado."
    },
    {
      id: "ITEM_11",
      categoria: "Computador Completo (Desktop Gamer)",
      titulo: "PC Gamer: Ryzen 5 5500 + GTX 1660 Super + 16GB RAM + SSD 480GB",
      specs: "Configuração completa montada em gabinete com lateral de vidro e fonte 500W 80 Plus. Pronto para uso."
    },
    {
      id: "ITEM_12",
      categoria: "Computador Completo (Desktop Gamer)",
      titulo: "PC Gamer: Ryzen 5 5600 + RTX 3060 12GB + 16GB RAM + SSD 512GB NVMe",
      specs: "Configuração gamer intermediária moderna. Fonte 600W 80 Plus Bronze. Usado por 1 ano."
    },
    {
      id: "ITEM_13",
      categoria: "Memória RAM",
      titulo: "Kit de Memória RAM 16GB (2x8GB) DDR4 3200MHz",
      specs: "Memória para computador de mesa (Desktop) com dissipador de calor | Usada, 100% funcional."
    }
  ];

  // Adiciona cada item com validação numérica (apenas número maior que zero)
  itens.forEach((it, index) => {
    // Adiciona seção a cada 4 ou 5 itens para não cansar o usuário
    if (index === 0) {
      form.addPageBreakItem().setTitle("Seção 1: Placas de Vídeo (GPUs)").setHelpText("Estime o valor de revenda justo para cada placa avulsa usada.");
    } else if (index === 5) {
      form.addPageBreakItem().setTitle("Seção 2: Processadores (CPUs)").setHelpText("Estime o valor de revenda justo para cada processador avulso usado.");
    } else if (index === 8) {
      form.addPageBreakItem().setTitle("Seção 3: Notebooks e Computadores Completos").setHelpText("Estime o valor de revenda justo para as máquinas montadas.");
    } else if (index === 12) {
      form.addPageBreakItem().setTitle("Seção 4: Memória RAM").setHelpText("Estime o valor justo para o kit de memória.");
    }

    const itemText = form.addTextItem();
    itemText.setTitle(`[${it.categoria}] ${it.titulo}`)
      .setHelpText(`Especificações: ${it.specs}\n\n-> Insira abaixo apenas o valor estimado em Reais (ex: 850):`)
      .setRequired(true);

    // Validação para aceitar apenas valores numéricos positivos
    const validacaoNumero = FormApp.createTextValidation()
      .requireNumberGreaterThan(0)
      .setHelpText("Por favor, digite um valor numérico válido maior que zero (ex: 750).")
      .build();
    itemText.setValidation(validacaoNumero);
  });

  // Mensagem final de agradecimento
  form.setConfirmationMessage("Muito obrigado pela sua participação! Suas respostas serão fundamentais para a análise quantitativa do TCC no projeto Rigfy.");

  // Exibe URLs de acesso no Console de Execução
  Logger.log("=================================================");
  Logger.log("✅ FORMULÁRIO CRIADO COM SUCESSO!");
  Logger.log("=================================================");
  Logger.log("🔗 LINK PARA EDITAR E INSERIR AS FOTOS: " + form.getEditUrl());
  Logger.log("🔗 LINK PÚBLICO PARA COMPARTILHAR: " + form.getPublishedUrl());
  Logger.log("=================================================");
}
