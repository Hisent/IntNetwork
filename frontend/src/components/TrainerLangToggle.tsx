import { LangToggle } from '@/components/workbench/WorkbenchShell'
import { useLangStore } from '@/store/lang'

export function TrainerLangToggle({ className }: { className?: string }) {
  const { lang, setLang } = useLangStore()
  return <LangToggle lang={lang} onChange={setLang} className={className} />
}
