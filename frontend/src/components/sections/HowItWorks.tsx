import Divider from '../ui/Divider'

const ETAPAS = [
  {
    num: 'ETAPA 01',
    titulo: 'Coleta em tempo real',
    texto: 'Nosso robô varre a OLX diariamente e coleta centenas de anúncios de hardware, extraindo preço, especificações e condição de cada equipamento.',
  },
  {
    num: 'ETAPA 02',
    titulo: 'Análise com machine learning',
    texto: 'Um modelo de Random Forest treinado com milhares de transações reais identifica os padrões que determinam o preço justo para cada configuração.',
  },
  {
    num: 'ETAPA 03',
    titulo: 'Estimativa fundamentada',
    texto: 'Você recebe o preço médio de mercado, a faixa de negociação e os anúncios reais usados como base — total transparência na metodologia.',
  },
]

export default function HowItWorks() {
  return (
    <section id="como-funciona" className="bg-bg-subtle py-20 px-6">
      <div className="max-w-5xl mx-auto">

        <h2 className="text-[28px] font-bold text-text-primary text-center mb-12">
          Como o Rigfy calcula o preço?
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
          {ETAPAS.map(({ num, titulo, texto }) => (
            <div key={num}>
              <p className="text-[10px] font-serif italic text-text-muted uppercase tracking-widest opacity-60">{num}</p>
              <p className="text-[12px] font-bold uppercase tracking-widest text-text-primary mt-2">{titulo}</p>
              <p className="text-[14px] text-text-secondary leading-[1.7] mt-2">{texto}</p>
            </div>
          ))}
        </div>

        <Divider className="my-10" />

        <p className="text-[13px] text-text-muted text-center">
          Metodologia baseada em Design Science Research (Hevner et al., 2004) — desenvolvido como pesquisa acadêmica na UFMT.
        </p>

      </div>
    </section>
  )
}
