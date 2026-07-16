import { useState } from 'react'
import { Menu, X } from 'lucide-react'

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false)

  const scrollTo = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
    setMobileOpen(false)
  }

  return (
    <header className="sticky top-0 z-50 bg-bg border-b border-border">
      <div className="max-w-5xl mx-auto px-6 h-14 flex items-center justify-between">

        {/* Logo */}
        <div className="flex items-center gap-2">
          <span className="font-bold text-[18px] text-text-primary tracking-tight">
            Rigfy
          </span>
          <span className="text-[10px] font-serif italic uppercase text-text-secondary bg-surface border border-border px-2 py-0.5">
            BETA
          </span>
        </div>

        {/* Nav desktop */}
        <nav className="hidden md:flex items-center gap-6">
          <button
            onClick={() => scrollTo('como-funciona')}
            className="text-sm text-text-secondary hover:text-text-primary transition-colors cursor-pointer"
          >
            Como funciona
          </button>
          <button
            onClick={() => scrollTo('planos')}
            className="text-sm text-text-secondary hover:text-text-primary transition-colors cursor-pointer"
          >
            Planos
          </button>
        </nav>

        {/* Actions desktop */}
        <div className="hidden md:flex items-center gap-3">
          <button className="text-[11px] font-bold uppercase tracking-widest text-text-secondary hover:text-text-primary transition-colors px-3 py-1.5 cursor-pointer">
            Entrar
          </button>
          <button className="text-[11px] font-bold uppercase tracking-widest bg-black text-white px-4 py-1.5 hover:opacity-90 transition-colors cursor-pointer border border-border">
            Criar conta
          </button>
        </div>

        {/* Hamburger mobile */}
        <button
          className="md:hidden p-1 text-text-secondary cursor-pointer"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="Menu"
        >
          {mobileOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Menu mobile */}
      {mobileOpen && (
        <div className="md:hidden border-t border-border bg-bg">
          <div className="max-w-5xl mx-auto px-6 py-3 flex flex-col gap-1">
            <button
              onClick={() => scrollTo('como-funciona')}
              className="text-sm text-text-secondary hover:text-text-primary py-2 text-left border-b border-border cursor-pointer"
            >
              Como funciona
            </button>
            <button
              onClick={() => scrollTo('planos')}
              className="text-sm text-text-secondary hover:text-text-primary py-2 text-left border-b border-border cursor-pointer"
            >
              Planos
            </button>
            <button className="text-[11px] font-bold uppercase tracking-widest text-text-secondary hover:text-text-primary py-2 text-left border-b border-border cursor-pointer">
              Entrar
            </button>
            <button className="mt-2 text-[11px] font-bold uppercase tracking-widest bg-black text-white px-4 py-2 hover:opacity-90 transition-colors text-center cursor-pointer border border-border">
              Criar conta
            </button>
          </div>
        </div>
      )}
    </header>
  )
}
