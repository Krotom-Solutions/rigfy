import { useState } from 'react'
import Hero from '../components/sections/Hero'
import Calculator from '../components/sections/Calculator'
import ResultCard from '../components/sections/ResultCard'
import HowItWorks from '../components/sections/HowItWorks'
import Pricing from '../components/sections/Pricing'
import Divider from '../components/ui/Divider'

export default function Home() {
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleCalculate = async (formData: any) => {
    setLoading(true)
    setResult(null)

    try {
      // Filtramos apenas as chaves vazias ou nulas
      const payload: any = {}
      Object.keys(formData).forEach(key => {
        if (formData[key] !== '' && formData[key] !== null) {
          payload[key] = formData[key]
        }
      })

      if (payload.ram_gb) {
        payload.ram_gb = parseInt(payload.ram_gb, 10)
      }

      const response = await fetch('http://localhost:8000/price/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })

      if (!response.ok) throw new Error('Falha na conexão')
      const data = await response.json()
      setResult(data)
    } catch (err) {
      console.error(err)
      alert('Erro ao calcular preço.')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setResult(null)
  }

  return (
    <>
      <Hero />
      <Divider />
      <Calculator onCalculate={handleCalculate} loading={loading} />
      {(loading || result) && (
        <ResultCard result={result} loading={loading} onReset={handleReset} />
      )}
      <HowItWorks />
      <Pricing />
    </>
  )
}
