export default function Footer() {
  return (
    <footer className="bg-bg-subtle border-t border-border py-10">
      <div className="max-w-5xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-8">

        <div>
          <p className="font-bold text-[11px] uppercase tracking-widest text-text-primary">Rigfy</p>
          <p className="text-sm text-text-muted mt-1">A Tabela FIPE do hardware usado.</p>
        </div>

        <div className="flex flex-col gap-1">
          {['Sobre', 'Como funciona', 'API', 'Contato'].map((link) => (
            <a
              key={link}
              href="#"
              className="text-sm text-text-secondary hover:text-text-primary transition-colors leading-loose"
            >
              {link}
            </a>
          ))}
        </div>

        <div>
          <p className="text-sm text-text-muted">
            Pesquisa acadêmica — UFMT, Cuiabá MT.
          </p>
          <p className="text-xs text-text-muted mt-1">
            © 2025 Rigfy. Todos os direitos reservados.
          </p>
        </div>

      </div>
    </footer>
  )
}
