import { useRef, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { trainerApi } from '@/lib/trainerApi'
import { ConfirmDialog } from '@/components/ConfirmDialog'
import { useTr } from '@/store/lang'
import { groupByModuleBlock, blockSnippet, type TrainerComment } from '@/components/commentGroups'

export function TrainerFeedback({ courseId }: { courseId: number }) {
  const { tr } = useTr()
  const comments = useQuery({
    queryKey: ['course-comments', courseId],
    queryFn: () => trainerApi.courseComments(courseId).then((r) => r.data),
  })

  if (!comments.data) return null
  if (comments.data.length === 0)
    return <p className="text-sm text-slate-500">{tr('trNoFeedback')}</p>

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
  const { tr } = useTr()
  const qc = useQueryClient()
  const mod = useQuery({
    queryKey: ['trainer-module', moduleKey],
    queryFn: () => trainerApi.trainerModule(moduleKey).then((r) => r.data),
  })
  const [drafts, setDrafts] = useState<Record<number, string>>({})
  // Löschen ist unwiderruflich und trifft fremde Beiträge — erst nach Rückfrage.
  const [deleteTarget, setDeleteTarget] = useState<TrainerComment | null>(null)
  const deleteTriggerRef = useRef<HTMLButtonElement | null>(null)
  const rootRef = useRef<HTMLDivElement | null>(null)

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
  const send = (blockIndex: number) => {
    const body = (drafts[blockIndex] ?? '').trim()
    if (!body || add.isPending) return
    // Entwurf erst nach Erfolg leeren — schlägt das Senden fehl,
    // bleibt der Text zum erneuten Versuch stehen.
    add.mutate({ blockIndex, body }, { onSuccess: () => setDrafts((d) => ({ ...d, [blockIndex]: '' })) })
  }

  return (
    <div ref={rootRef} className="rounded-xl border bg-white p-4">
      <h4 className="text-sm font-semibold text-slate-800 mb-2">{mod.data?.title ?? moduleKey}</h4>
      {(add.isError || del.isError) && <p role="alert" className="mb-2 text-xs text-rose-600">{tr('trActionFailed')}</p>}
      <div className="flex flex-col gap-3">
        {groups.map((g) => {
          const snippet = blockSnippet(mod.data?.blocks[g.blockIndex])
          return (
            <div key={g.blockIndex} className="border-t pt-2">
              <p className="text-xs text-slate-500">
                {tr('trBlockN', { n: g.blockIndex + 1 })}
                {snippet && <span> · {tr('trQuoted', { text: snippet })}</span>}
              </p>
              {g.items.map((c) => (
                <div key={c.id} className="text-sm mt-1">
                  <span className="font-medium text-slate-700">{c.author_name}</span>
                  <button
                    onClick={(e) => { deleteTriggerRef.current = e.currentTarget; setDeleteTarget(c) }}
                    aria-label={tr('trDeleteCommentAria', { name: c.author_name })}
                    className="ml-2 text-xs text-rose-600 hover:text-rose-700"
                  >
                    {tr('trDeleteLower')}
                  </button>
                  <p className="text-slate-700">{c.body}</p>
                </div>
              ))}
              <div className="flex gap-2 mt-2">
                {/* Enter sendet, Umschalt+Enter macht eine neue Zeile */}
                <textarea
                  rows={1}
                  value={drafts[g.blockIndex] ?? ''}
                  onChange={(e) => setDrafts((d) => ({ ...d, [g.blockIndex]: e.target.value }))}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) { e.preventDefault(); send(g.blockIndex) }
                  }}
                  aria-label={tr('trReplyToBlockAria', { n: g.blockIndex + 1 })}
                  title={tr('trEnterSends')}
                  placeholder={tr('trReplyPh')}
                  className="flex-1 border rounded-lg px-2 py-1 text-sm"
                />
                <button
                  onClick={() => send(g.blockIndex)}
                  className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 text-sm font-medium"
                >
                  {tr('trReply')}
                </button>
              </div>
            </div>
          )
        })}
      </div>
      <ConfirmDialog
        open={deleteTarget !== null}
        title={tr('trDeleteComment')}
        description={<>{tr('trDeleteCommentDesc', { name: deleteTarget?.author_name ?? '' })}</>}
        confirmLabel={tr('trDelete')}
        triggerRef={deleteTriggerRef}
        container={rootRef.current?.closest('.workbench')}
        onConfirm={() => { if (deleteTarget) del.mutate(deleteTarget.id); setDeleteTarget(null) }}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  )
}
