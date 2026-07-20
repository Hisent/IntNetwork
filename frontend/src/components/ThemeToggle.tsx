import { useThemeStore } from '@/store/theme'
import { Icon } from '@/components/Icon'
import type { Lang } from '@/lib/i18n'

export function ThemeToggle({ lang = 'de', className = '' }: { lang?: Lang; className?: string }) {
  const { theme, toggle } = useThemeStore()
  const dark = theme === 'dark'
  const label = dark
    ? (lang === 'de' ? 'Helles Design' : 'Light theme')
    : (lang === 'de' ? 'Dunkles Design' : 'Dark theme')
  return (
    <button
      type="button"
      onClick={toggle}
      aria-label={label}
      title={label}
      className={`grid h-9 w-9 place-items-center rounded-lg text-current opacity-70 transition-opacity hover:opacity-100 ${className}`}>
      <Icon name={dark ? 'sun' : 'moon'} className="h-5 w-5" />
    </button>
  )
}
