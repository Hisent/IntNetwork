import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { authApi, errMsg } from '@/lib/api'
import { trainerApi } from '@/lib/trainerApi'
import { isPasskeySupported, isPasskeyCancelled, loginWithPasskey } from '@/lib/passkey'
import { BrandLogo } from '@/components/BrandLogo'
import { TrainerLangToggle } from '@/components/TrainerLangToggle'
import { useTr } from '@/store/lang'
import { Field } from './shared'

// --- Login --------------------------------------------------------------------

export function TrainerLogin({ onLogin }: { onLogin: (t: string) => void }) {
  const { tr } = useTr()
  const [email, setEmail] = useState('')
  const [pw, setPw] = useState('')
  const [err, setErr] = useState('')
  const [busy, setBusy] = useState(false)
  const [passkeyBusy, setPasskeyBusy] = useState(false)
  // isPasskeySupported() ist eine reine Browser-/Kontext-Prüfung (kein
  // Request) — einmal pro Render reicht, kein State/Effekt nötig.
  const passkeySupported = isPasskeySupported()
  const passkeyStatus = useQuery({
    queryKey: ['passkey-status'],
    queryFn: () => trainerApi.passkeyStatus().then((r) => r.data),
    enabled: passkeySupported,
  })
  async function submit(e: React.FormEvent) {
    e.preventDefault()
    if (busy) return
    setErr(''); setBusy(true)
    try { onLogin((await authApi.trainerLogin(email, pw)).data.access_token) }
    catch { setErr(tr('trLoginFailed')) }
    finally { setBusy(false) }
  }
  // Abbruch des Systemdialogs (NotAllowedError) ist ein normaler Rückzug,
  // kein Anwendungsfehler — dafür bleibt der Fehlerkasten still (siehe
  // isPasskeyCancelled in lib/passkey.ts).
  async function submitPasskey() {
    if (passkeyBusy) return
    setErr(''); setPasskeyBusy(true)
    try { onLogin((await loginWithPasskey()).access_token) }
    catch (e) { if (!isPasskeyCancelled(e)) setErr(errMsg(e, tr('trPasskeyLoginFailed'))) }
    finally { setPasskeyBusy(false) }
  }
  const showPasskeyButton = passkeySupported && passkeyStatus.data?.enabled === true
  return (
    <div className="workbench flex min-h-dvh items-center justify-center p-4">
      <form onSubmit={submit} className="wb-surface flex w-full max-w-sm flex-col gap-3 p-8 shadow">
        <div className="mb-3 flex items-center justify-between gap-2">
          <Link to="/"><BrandLogo className="h-9 text-lg" showName /></Link>
          <TrainerLangToggle />
        </div>
        <h1 className="text-xl font-bold text-[var(--wb-ink)]">{tr('trLoginTitle')}</h1>
        <Field label={tr('trEmail')} type="email" autoComplete="username" placeholder={tr('trEmailPlaceholder')} value={email} onChange={(e) => setEmail(e.target.value)} />
        <Field label={tr('trPassword')} type="password" autoComplete="current-password" placeholder="••••••••" value={pw} onChange={(e) => setPw(e.target.value)} />
        {err && <p aria-live="polite" className="text-sm text-rose-600">{err}</p>}
        <button disabled={busy || passkeyBusy} className="wb-control mt-1 rounded-lg bg-[var(--wb-accent)] py-2 font-medium text-white hover:bg-[var(--wb-accent-hover)] disabled:opacity-50 disabled:cursor-not-allowed">{busy ? tr('trSigningIn') : tr('trSignIn')}</button>
        {showPasskeyButton && (
          <button type="button" onClick={submitPasskey} disabled={busy || passkeyBusy}
            className="wb-control rounded-lg border border-[var(--wb-border)] py-2 font-medium text-[var(--wb-ink)] hover:bg-[var(--wb-subtle)] disabled:opacity-50 disabled:cursor-not-allowed">
            {passkeyBusy ? tr('trSigningIn') : tr('trSignInPasskey')}
          </button>
        )}
      </form>
    </div>
  )
}
