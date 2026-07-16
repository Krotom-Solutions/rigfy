import { useEffect, useRef, useState } from 'react'

export default function ProgressBar({ value = 0, animated = false }: any) {
  const [width, setWidth] = useState(0)
  const rafRef = useRef<any>(null)

  useEffect(() => {
    if (!animated) {
      setWidth(value)
      return
    }

    const duration = 600
    const start = performance.now()

    const animate = (now: number) => {
      const elapsed = now - start
      const progress = Math.min(elapsed / duration, 1)
      // easeOutCubic
      const eased = 1 - Math.pow(1 - progress, 3)
      setWidth(Math.round(eased * value))
      if (progress < 1) rafRef.current = requestAnimationFrame(animate)
    }

    rafRef.current = requestAnimationFrame(animate)
    return () => cancelAnimationFrame(rafRef.current)
  }, [value, animated])

  return (
    <div className="w-full h-1.5 bg-surface-2 rounded-none overflow-hidden border border-border">
      <div
        className="h-full bg-black rounded-none transition-none"
        style={{ width: `${width}%` }}
      />
    </div>
  )
}
