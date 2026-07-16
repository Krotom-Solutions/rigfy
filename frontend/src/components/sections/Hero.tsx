export default function Hero() {
  const scrollToCalculator = () => {
    document.getElementById('calculadora')?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <section className="bg-bg py-24 px-6">
      <div className="max-w-2xl mx-auto text-center">

        <p className="text-[10px] font-serif italic text-text-muted uppercase tracking-widest mb-4">
          Precificação de Hardware Usado
        </p>

        <h1 className="text-[48px] md:text-[48px] text-[32px] font-bold text-text-primary leading-[1.15] mb-5 uppercase tracking-tight">
          Descubra o preço justo<br />do seu hardware.
        </h1>

        <p className="text-[17px] text-text-secondary leading-[1.7] max-w-[520px] mx-auto mb-8">
          O Rigfy analisa milhares de anúncios reais da OLX e usa machine
          learning para calcular o valor de mercado do seu notebook ou
          desktop — sem achismo, sem subjetividade.
        </p>

        <button
          onClick={scrollToCalculator}
          className="bg-black text-white text-[11px] font-bold uppercase tracking-widest px-7 h-12 border border-border hover:opacity-90 transition-colors cursor-pointer"
        >
          Calcular preço agora →
        </button>

        <p className="text-[13px] text-text-muted mt-5">
          ★ 4.8/5 de satisfação · +2.400 precificações este mês · Dados atualizados diariamente
        </p>

      </div>
    </section>
  )
}
