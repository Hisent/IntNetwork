import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { learnApi } from '@/lib/learnApi'
import { errMsg } from '@/lib/api'
import { t, type Lang } from '@/lib/i18n'
import { formatApiTime } from '@/lib/apiTime'

export function BlockComments({ moduleKey, blockIndex, lang }: { moduleKey: string; blockIndex: number; lang: Lang }) {
  const qc = useQueryClient()
  const [open, setOpen] = useState(false)
  const [text, setText] = useState('')

  const comments = useQuery({
    queryKey: ['comments', moduleKey],
    queryFn: () => learnApi.listComments(moduleKey).then((r) => r.data),
  })
  const add = useMutation({
    mutationFn: () => learnApi.addComment(moduleKey, blockIndex, text),
    onSuccess: () => {
      setText('')
      qc.invalidateQueries({ queryKey: ['comments', moduleKey] })
    },
  })
  const del = useMutation({
    mutationFn: (id: number) => learnApi.deleteComment(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['comments', moduleKey] }),
  })

  const items = (comments.data ?? []).filter((c) => c.block_index === blockIndex)

  return (
    <div className="mt-1">
      <button
        onClick={() => setOpen((o) => !o)}
        className="text-xs font-medium text-teal-700 hover:text-teal-800"
      >
        {open ? '▾' : '▸'} 💬 {t(lang, 'comments')} ({items.length})
      </button>
      {open && (
        <div className="mt-2 rounded-lg border bg-slate-50 p-3">
          <div className="flex flex-col gap-2 mb-2">
            {items.length === 0 && <p className="text-xs text-slate-400">{t(lang, 'noComments')}</p>}
            {items.map((c) => (
              <div key={c.id} className="text-sm">
                <span className="font-medium text-slate-700">{c.author_name}</span>
                <span className="text-xs text-slate-400"> · {formatApiTime(c.created_at, lang)}</span>
                {c.own && (
                  <button
                    onClick={() => del.mutate(c.id)}
                    className="ml-2 text-xs text-rose-600 hover:text-rose-700"
                  >
                    {t(lang, 'delete')}
                  </button>
                )}
                <p className="text-slate-700">{c.body}</p>
              </div>
            ))}
          </div>
          <form className="flex gap-2" onSubmit={(e) => { e.preventDefault(); if (text.trim() && !add.isPending) add.mutate() }}>
            <input
              value={text}
              onChange={(e) => setText(e.target.value)}
              aria-label={t(lang, 'comments')}
              placeholder={t(lang, 'commentPlaceholder')}
              className="flex-1 border rounded-lg px-2 py-1 text-sm"
            />
            <button
              disabled={add.isPending}
              className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 text-sm font-medium disabled:opacity-60"
            >
              {t(lang, 'send')}
            </button>
          </form>
          {(add.isError || del.isError) && (
            <p role="alert" className="mt-2 text-xs text-rose-600">
              {errMsg(add.error ?? del.error, lang === 'de' ? 'Das hat nicht geklappt. Bitte erneut versuchen.' : 'That did not work. Please try again.')}
            </p>
          )}
        </div>
      )}
    </div>
  )
}
