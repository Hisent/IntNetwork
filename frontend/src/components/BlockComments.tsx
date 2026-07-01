import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { learnApi } from '@/lib/learnApi'

export function BlockComments({ moduleKey, blockIndex }: { moduleKey: string; blockIndex: number }) {
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
        {open ? '▾' : '▸'} 💬 Kommentare ({items.length})
      </button>
      {open && (
        <div className="mt-2 rounded-lg border bg-slate-50 p-3">
          <div className="flex flex-col gap-2 mb-2">
            {items.length === 0 && <p className="text-xs text-slate-400">Noch keine Kommentare.</p>}
            {items.map((c) => (
              <div key={c.id} className="text-sm">
                <span className="font-medium text-slate-700">{c.author_name}</span>
                <span className="text-xs text-slate-400"> · {c.created_at.slice(0, 16).replace('T', ' ')}</span>
                {c.own && (
                  <button
                    onClick={() => del.mutate(c.id)}
                    className="ml-2 text-xs text-rose-600 hover:text-rose-700"
                  >
                    löschen
                  </button>
                )}
                <p className="text-slate-700">{c.body}</p>
              </div>
            ))}
          </div>
          <div className="flex gap-2">
            <input
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Kommentar…"
              className="flex-1 border rounded-lg px-2 py-1 text-sm"
            />
            <button
              onClick={() => text.trim() && add.mutate()}
              disabled={add.isPending}
              className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 text-sm font-medium disabled:opacity-60"
            >
              Senden
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
