import { useEffect, useState } from 'react'
import Button from '../ui/Button'
import Divider from '../ui/Divider'

function formatPrice(value: number) {
  if (value === undefined || value === null) return ''
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', minimumFractionDigits: 0 })
}

function AnimatedPrice({ target }: { target: number }) {
  const [displayed, setDisplayed] = useState(0)

  useEffect(() => {
    if (!target) return
    const duration = 800
    const start = performance.now()
    const animate = (now: number) => {
      const progress = Math.min((now - start) / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      setDisplayed(Math.round(eased * target))
      if (progress < 1) requestAnimationFrame(animate)
    }
    requestAnimationFrame(animate)
  }, [target])

  return <span>{formatPrice(displayed)}</span>
}

export default function ResultCard({ result, loading, onReset }: any) {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    if (result) {
      requestAnimationFrame(() => setVisible(true))
    } else {
      setVisible(false)
    }
  }, [result])

  if (loading) {
    return (
      <section className="bg-bg-subtle py-6 px-6">
        <div className="max-w-[620px] mx-auto bg-bg border border-border rounded-none p-10">
          <div className="flex items-center gap-3 text-text-muted text-sm">
            <div className="w-4 h-4 border-2 border-border-strong border-t-black rounded-full animate-spin" />
            Analisando mercado...
          </div>
        </div>
      </section>
    )
  }

  if (!result) return null

  const isInsuficiente = result.confianca === 'insuficiente'

  return (
    <section className="bg-bg-subtle py-6 px-6">
      <div
        className="max-w-[620px] mx-auto bg-bg border border-border rounded-none p-10 transition-opacity duration-300"
        style={{ opacity: visible ? 1 : 0 }}
      >
        <p className="text-[10px] font-mono text-text-muted uppercase tracking-widest mb-4">
          Estimativa de Preço de Mercado
        </p>
        <Divider className="mb-5" />

        <p className="font-mono font-bold text-[52px] leading-none text-text-primary mb-1">
          {result.preco_estimado ? <AnimatedPrice target={result.preco_estimado} /> : 'N/A'}
        </p>
        <p className="font-mono text-[13px] text-text-muted mt-2">
          Intervalo: {formatPrice(result.preco_minimo)} — {formatPrice(result.preco_maximo)}
        </p>

        <Divider className="my-6" />

        {isInsuficiente && (
          <div className="mb-6 p-4 border border-black bg-black/5">
            <p className="text-sm font-mono text-text-primary">
              ⚠️ <strong>Atenção:</strong> Há poucos dados no mercado para as especificações exatas dessa máquina. A estimativa pode ser menos precisa.
            </p>
          </div>
        )}

        <p className="text-sm font-mono text-text-muted mb-6">
          Baseado em <strong>{result.total_anuncios_similares || 0}</strong> anúncios similares.
        </p>

        <div className="flex items-center gap-3 mt-6">
          <Button variant="ghost" size="md" className="flex-1" onClick={onReset}>
            Nova precificação
          </Button>
        </div>
      </div>
    </section>
  )
}
