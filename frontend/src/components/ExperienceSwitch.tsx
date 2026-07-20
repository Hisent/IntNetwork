import { useUiModeStore, type UiMode } from '@/store/uiMode'
import { mayChangeExperience } from '@/components/experienceSwitchLogic'

export function ExperienceSwitch({ lang = 'de', confirmBeforeChange = false, confirmMessage }: {
  lang?: 'de' | 'en'
  confirmBeforeChange?: boolean
  confirmMessage?: string
}) {
  const { mode, setMode } = useUiModeStore()
  const label = lang === 'de' ? 'Ansicht' : 'View'
  const options: { value: UiMode; label: string }[] = [
    { value: 'classic', label: 'Classic' },
    { value: 'workbench', label: 'Workbench' },
  ]

  return (
    <fieldset className="flex items-center gap-1 text-xs">
      <legend className="sr-only">{label}</legend>
      {options.map((option) => (
        <button key={option.value} type="button" onClick={() => {
          if (option.value === mode) return
          const message = confirmMessage ?? (lang === 'de'
            ? 'Laufende Eingaben werden beim Wechsel zurückgesetzt. Ansicht trotzdem wechseln?'
            : 'Current inputs will be reset when switching. Change view anyway?')
          if (mayChangeExperience(confirmBeforeChange, message, (value) => window.confirm(value))) setMode(option.value)
        }}
          aria-pressed={mode === option.value}
          className={`rounded px-2 py-1 border ${mode === option.value
            ? 'border-[var(--workshop-accent)] bg-[var(--workshop-accent)] text-white'
            : 'border-slate-200 text-slate-500 hover:bg-slate-50'}`}>
          {option.label}
        </button>
      ))}
    </fieldset>
  )
}
