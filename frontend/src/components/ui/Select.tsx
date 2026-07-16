import { ChevronDown } from 'lucide-react'

export default function Select({ label, id, children, value, onChange, required = false }: any) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label htmlFor={id} className="text-[10px] font-serif italic uppercase opacity-60">
          {label}
          {required && <span className="ml-0.5">*</span>}
        </label>
      )}
      <div className="relative">
        <select
          id={id}
          value={value}
          onChange={onChange}
          required={required}
          className="
            w-full h-10 pl-3 pr-8 bg-surface border border-border rounded-none
            text-[14px] text-text-primary appearance-none cursor-pointer
            hover:bg-white focus:bg-white focus:outline-none
            transition-colors
          "
        >
          {children}
        </select>
        <ChevronDown
          size={14}
          className="absolute right-2.5 top-1/2 -translate-y-1/2 text-text-muted pointer-events-none"
        />
      </div>
    </div>
  )
}
