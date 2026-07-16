import { useState } from 'react'
import Select from '../ui/Select'
import Button from '../ui/Button'
import Divider from '../ui/Divider'

const ESTADOS = [
  { value: 'novo', label: 'Novo na caixa' },
  { value: 'seminovo', label: 'Seminovo' },
  { value: 'bom', label: 'Bom estado' },
  { value: 'desgaste', label: 'Com desgaste' },
  { value: 'defeito', label: 'Com defeito' },
]

export default function Calculator({ onCalculate, loading }: any) {
  const [form, setForm] = useState<any>({
    categoria: '', marca: '', cpu_linha: '',
    ram_gb: '', storage_tipo: '',
    ano: '', estado: '',
    notaFiscal: false, garantia: false, acessorios: false,
  })

  const [errors, setErrors] = useState<any>({})

  const set = (key: string) => (e: any) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value
    setForm((prev: any) => ({ ...prev, [key]: value }))
    if (errors[key]) setErrors((prev: any) => ({ ...prev, [key]: false }))
  }

  const validate = () => {
    const required = ['categoria', 'cpu_linha', 'ram_gb', 'storage_tipo', 'estado']
    const newErrors: any = {}
    required.forEach((k) => { if (!form[k]) newErrors[k] = true })
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: any) => {
    e.preventDefault()
    if (validate()) onCalculate(form)
  }

  const fieldClass = (key: string) =>
    errors[key] ? 'ring-1 ring-border-strong' : ''

  return (
    <section id="calculadora" className="bg-bg-subtle py-20 px-6">
      <div className="max-w-[620px] mx-auto">
        <div className="bg-bg border border-border rounded-none p-10">

          {/* Header */}
          <div className="mb-6">
            <h2 className="text-[14px] font-bold uppercase tracking-widest text-text-primary">
              Especificações do equipamento
            </h2>
            <p className="text-[10px] font-mono text-text-muted mt-1 uppercase">
              Preencha os campos para obter a estimativa.
            </p>
          </div>
          <Divider className="mb-7" />

          <form onSubmit={handleSubmit} noValidate>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">

              <div className={fieldClass('categoria')}>
                <Select label="Categoria" id="categoria" value={form.categoria} onChange={set('categoria')} required>
                  <option value="">Selecione...</option>
                  <option value="notebook">Notebook</option>
                  <option value="desktop">Desktop</option>
                </Select>
              </div>
              <Select label="Marca" id="marca" value={form.marca} onChange={set('marca')}>
                <option value="">Selecione...</option>
                {['Acer','Apple','Asus','Dell','HP','Lenovo','Samsung','Positivo','Outra'].map(m => (
                  <option key={m} value={m}>{m}</option>
                ))}
              </Select>

              <div className={fieldClass('cpu_linha')}>
                <Select label="Processador" id="cpu_linha" value={form.cpu_linha} onChange={set('cpu_linha')} required>
                  <option value="">Selecione...</option>
                  <optgroup label="Intel">
                    {['Core i3','Core i5','Core i7','Core i9'].map(p => <option key={p} value={p}>{p}</option>)}
                  </optgroup>
                  <optgroup label="AMD">
                    {['Ryzen 3','Ryzen 5','Ryzen 7','Ryzen 9'].map(p => <option key={p} value={p}>{p}</option>)}
                  </optgroup>
                </Select>
              </div>
              
              <div className={fieldClass('ram_gb')}>
                <Select label="Memória RAM" id="ram_gb" value={form.ram_gb} onChange={set('ram_gb')} required>
                  <option value="">Selecione...</option>
                  {[4, 8, 16, 32, 64].map(r => <option key={r} value={r}>{r} GB</option>)}
                </Select>
              </div>

              <div className={fieldClass('storage_tipo')}>
                <Select label="Tipo de Armazenamento" id="storage_tipo" value={form.storage_tipo} onChange={set('storage_tipo')} required>
                  <option value="">Selecione...</option>
                  <option value="HDD">HDD</option>
                  <option value="SSD">SSD</option>
                  <option value="SSD NVMe">SSD NVMe</option>
                </Select>
              </div>

              <Select label="Ano de fabricação" id="ano" value={form.ano} onChange={set('ano')}>
                <option value="">Selecione...</option>
                {Array.from({ length: 10 }, (_, i) => 2024 - i).map(y => (
                  <option key={y} value={y}>{y}</option>
                ))}
              </Select>

            </div>

            {/* Estado de conservação */}
            <div className="mt-6">
              <p className="text-[10px] font-mono uppercase text-text-muted mb-2.5">
                Estado de conservação <span className="ml-0.5">*</span>
              </p>
              <div className="flex flex-wrap gap-2">
                {ESTADOS.map(({ value, label }) => (
                  <button
                    key={value}
                    type="button"
                    onClick={() => setForm((p: any) => ({ ...p, estado: value }))}
                    className={`
                      text-[12px] font-mono px-3.5 py-2 border transition-colors cursor-pointer
                      ${form.estado === value
                        ? 'bg-black text-white border-black'
                        : 'bg-transparent border-black text-black hover:bg-black/5'
                      }
                    `}
                  >
                    {label}
                  </button>
                ))}
              </div>
              {errors.estado && (
                <p className="text-[12px] text-text-muted mt-1.5">Selecione o estado do equipamento.</p>
              )}
            </div>

            {/* Checkboxes */}
            <div className="mt-5 flex flex-wrap gap-5">
              {[
                { key: 'notaFiscal', label: 'Acompanha nota fiscal' },
                { key: 'garantia',   label: 'Possui garantia' },
                { key: 'acessorios', label: 'Acessórios originais' },
              ].map(({ key, label }) => (
                <label key={key} className="flex items-center gap-2 text-[12px] font-mono text-text-secondary cursor-pointer select-none">
                  <input
                    type="checkbox"
                    checked={form[key]}
                    onChange={set(key)}
                    className="w-4 h-4 rounded-none border-black accent-black cursor-pointer"
                  />
                  {label}
                </label>
              ))}
            </div>

            <Divider className="my-7" />

            <Button type="submit" size="lg" disabled={loading}>
              {loading ? 'Calculando...' : 'Calcular preço de mercado →'}
            </Button>

          </form>
        </div>
      </div>
    </section>
  )
}
