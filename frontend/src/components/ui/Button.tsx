export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  type = 'button',
  className = '',
}: any) {
  const base = 'inline-flex items-center justify-center font-bold uppercase tracking-widest transition-colors focus:outline-none disabled:cursor-not-allowed cursor-pointer border border-border rounded-none'

  const variants: any = {
    primary: 'bg-black text-white hover:opacity-90 disabled:opacity-50',
    ghost:   'bg-transparent text-text-primary hover:bg-white',
    link:    'bg-transparent border-transparent text-text-secondary hover:opacity-80 underline-offset-2 hover:underline',
  }

  const sizes: any = {
    sm: 'text-[10px] px-3 py-1.5 h-8',
    md: 'text-[11px] px-6 py-2 h-10',
    lg: 'text-xs px-6 h-12 w-full',
  }

  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      className={`${base} ${variants[variant]} ${sizes[size]} ${className}`}
    >
      {children}
    </button>
  )
}
