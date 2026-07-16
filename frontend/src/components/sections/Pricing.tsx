import { Check, Minus } from 'lucide-react'
import Button from '../ui/Button'
import Divider from '../ui/Divider'

const FREE_FEATURES = [
  { text: '5 precificações por dia',          included: true },
  { text: 'Estimativa de preço de mercado',   included: true },
  { text: 'Anúncios similares (top 3)',        included: true },
  { text: 'Histórico de preços',              included: false },
  { text: 'Relatório em PDF',                 included: false },
  { text: 'Acesso à API',                     included: false },
]

const PRO_FEATURES = [
  { text: 'Precificações ilimitadas',          included: true },
  { text: 'Estimativa de preço de mercado',   included: true },
  { text: 'Anúncios similares (top 20)',       included: true },
  { text: 'Histórico de preços (6 meses)',     included: true },
  { text: 'Relatório em PDF',                 included: true },
  { text: 'Acesso à API (100 req/dia)',        included: true },
]

function FeatureList({ features }: { features: any[] }) {
  return (
    <ul className="flex flex-col gap-2.5 mt-5">
      {features.map(({ text, included }) => (
        <li key={text} className="flex items-center gap-2.5">
          {included
            ? <Check size={14} className="text-text-primary shrink-0" strokeWidth={2.5} />
            : <Minus size={14} className="text-text-muted shrink-0" />
          }
          <span className={`text-sm ${included ? 'text-text-secondary' : 'text-text-muted'}`}>
            {text}
          </span>
        </li>
      ))}
    </ul>
  )
}

export default function Pricing() {
  return (
    <section id="planos" className="bg-bg py-20 px-6">
      <div className="max-w-5xl mx-auto">

        <div className="text-center mb-12">
          <h2 className="text-[28px] font-bold text-text-primary">Planos</h2>
          <p className="text-[16px] text-text-secondary mt-2">
            Comece grátis. Sem cartão de crédito.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 max-w-[560px] mx-auto">

          {/* Free */}
          <div className="border border-border rounded-none p-8 bg-surface">
            <span className="text-[10px] font-serif italic uppercase text-text-secondary bg-white border border-border px-2 py-0.5">
              GRATUITO
            </span>
            <div className="flex items-end gap-1 mt-4">
              <span className="text-[36px] font-mono font-bold text-text-primary leading-none">R$ 0</span>
              <span className="text-sm font-mono text-text-muted mb-1">/mês</span>
            </div>
            <Divider className="my-5" />
            <FeatureList features={FREE_FEATURES} />
            <Button variant="ghost" size="md" className="w-full mt-6 bg-white">
              Criar conta grátis
            </Button>
          </div>

          {/* Pro */}
          <div className="border border-border rounded-none p-8 bg-bg shadow-[4px_4px_0_0_rgba(20,20,20,1)]">
            <span className="text-[10px] font-serif italic uppercase text-white bg-black px-2 py-0.5">
              PRO
            </span>
            <div className="flex items-end gap-1 mt-4">
              <span className="text-[36px] font-mono font-bold text-text-primary leading-none">R$ 29</span>
              <span className="text-sm font-mono text-text-muted mb-1">/mês</span>
            </div>
            <p className="text-[13px] font-mono text-text-muted mt-1">ou R$ 249/ano</p>
            <Divider className="my-5" />
            <FeatureList features={PRO_FEATURES} />
            <Button size="lg" className="mt-6">
              Assinar Pro →
            </Button>
            <p className="text-[12px] text-text-muted text-center mt-3">
              Cancele quando quiser.
            </p>
          </div>

        </div>
      </div>
    </section>
  )
}
