import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { trainerApi } from '@/lib/trainerApi'
import { groupByModuleBlock, blockSnippet, type TrainerComment } from '@/components/commentGroups'

export function TrainerFeedback({ courseId }: { courseId: number }) {
  const comments = useQuery({
    queryKey: ['course-comments', courseId],
    queryFn: () => trainerApi.courseComments(courseId).then((r) => r.data),
  })

  if (!comments.data) return null
  if (comments.data.length === 0)
    return <p className="text-sm text-slate-400">Noch kein Feedback in diesem Kurs.</p>

  const byModule = new Map<string, TrainerComment[]>()
  for (const c of comments.data) {
    const list = byModule.get(c.module_key) ?? []
    list.push(c)
    byModule.set(c.module_key, list)
  }

  return (
    <div className="flex flex-col gap-4">
      {[...byModule.keys()].map((key) => (
        <FeedbackModule key={key} courseId={courseId} moduleKey={key} comments={byModule.get(key)!} />
      ))}
    </div>
  )
}

function FeedbackModule({
  courseId,
  moduleKey,
  comments,
}: {
  courseId: number
  moduleKey: string
  comments: TrainerComment[]
}) {
  const qc = useQueryClient()
  const mod = useQuery({
    queryKey: ['trainer-module', moduleKey],
    queryFn: () => trainerApi.trainerModule(moduleKey).then((r) => r.data),
  })
  const [drafts, setDrafts] = useState<Record<number, string>>({})

  const add = useMutation({
    mutationFn: (v: { blockIndex: number; body: string }) =>
      trainerApi.addTrainerComment(courseId, moduleKey, v.blockIndex, v.body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['course-comments', courseId] }),
  })
  const del = useMutation({
    mutationFn: (id: number) => trainerApi.deleteTrainerComment(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['course-comments', courseId] }),
  })

  const groups = groupByModuleBlock(comments)

  return (
    <div className="rounded-xl border bg-white p-4">
      <h4 className="text-sm font-semibold text-slate-800 mb-2">{mod.data?.title ?? moduleKey}</h4>
      <div className="flex flex-col gap-3">
        {groups.map((g) => {
          const snippet = blockSnippet(mod.data?.blocks[g.blockIndex])
          return (
            <div key={g.blockIndex} className="border-t pt-2">
              <p className="text-xs text-slate-400">
                Block {g.blockIndex + 1}
                {snippet && <span> · „{snippet}"</span>}
              </p>
              {g.items.map((c) => (
                <div key={c.id} className="text-sm mt-1">
                  <span className="font-medium text-slate-700">{c.author_name}</span>
                  <button
                    onClick={() => del.mutate(c.id)}
                    className="ml-2 text-xs text-rose-600 hover:text-rose-700"
                  >
                    löschen
                  </button>
                  <p className="text-slate-700">{c.body}</p>
                </div>
              ))}
              <div className="flex gap-2 mt-2">
                <input
                  value={drafts[g.blockIndex] ?? ''}
                  onChange={(e) => setDrafts((d) => ({ ...d, [g.blockIndex]: e.target.value }))}
                  placeholder="Antwort…"
                  className="flex-1 border rounded-lg px-2 py-1 text-sm"
                />
                <button
                  onClick={() => {
                    const body = (drafts[g.blockIndex] ?? '').trim()
                    if (body) {
                      add.mutate({ blockIndex: g.blockIndex, body })
                      setDrafts((d) => ({ ...d, [g.blockIndex]: '' }))
                    }
                  }}
                  className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 text-sm font-medium"
                >
                  Antworten
                </button>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
