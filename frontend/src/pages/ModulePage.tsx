import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import Markdown from 'react-markdown'
import { Link, useParams } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { Blocks } from '@/components/Blocks'
import { BlockComments } from '@/components/BlockComments'
import { Quiz } from '@/components/Quiz'
import { t, type Lang } from '@/lib/i18n'

export function ModulePage() {
  const { key = '' } = useParams()
  const qc = useQueryClient()
  const me = useQuery({ queryKey: ['me'], queryFn: () => learnApi.me().then((r) => r.data) })
  const lang: Lang = me.data?.language ?? 'de'
  const mod = useQuery({ queryKey: ['module', key, lang], queryFn: () => learnApi.getModule(key).then((r) => r.data) })
  const features = useQuery({ queryKey: ['features'], queryFn: () => learnApi.features().then((r) => r.data) })
  const setLang = useMutation({
    mutationFn: (l: Lang) => learnApi.setLanguage(l),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['me'] })
      qc.invalidateQueries({ queryKey: ['module'] })
    },
  })

  if (mod.isLoading || !mod.data) return <div className="p-10">{t(lang, 'loading')}</div>

  const commentsOn = features.data?.comments ?? false

  return (
    <div className="min-h-screen bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center justify-between mb-2">
          <Link to="/lernen" className="text-sm text-slate-400 hover:text-slate-600">← {t(lang, 'modules')}</Link>
          <div className="flex gap-1 text-xs font-medium">
            <button onClick={() => setLang.mutate('de')}
              className={`rounded px-2 py-1 border ${lang === 'de' ? 'bg-teal-600 text-white border-teal-600' : 'text-slate-500 border-slate-200 hover:bg-slate-50'}`}>
              DE
            </button>
            <button onClick={() => setLang.mutate('en')}
              className={`rounded px-2 py-1 border ${lang === 'en' ? 'bg-teal-600 text-white border-teal-600' : 'text-slate-500 border-slate-200 hover:bg-slate-50'}`}>
              EN
            </button>
          </div>
        </div>
        <h1 className="text-2xl font-bold text-slate-900 mt-2 mb-4">{mod.data.title}</h1>
        {mod.data.scenario && (
          <div className="rounded-xl border-l-4 border-teal-400 bg-teal-50 px-4 py-3 mb-6 text-sm text-slate-700">
            <Markdown>{mod.data.scenario}</Markdown>
          </div>
        )}
        <Blocks
          blocks={mod.data.blocks}
          lang={lang}
          footer={
            commentsOn
              ? (b, i) => (b.type === 'text' ? <BlockComments moduleKey={key} blockIndex={i} lang={lang} /> : null)
              : undefined
          }
        />
        <Quiz moduleKey={key} questions={mod.data.quiz.questions} lang={lang} />
      </div>
    </div>
  )
}
