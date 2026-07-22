import { useEffect, useRef, useState } from 'react'
import { DOT1X_STEPS, finalVlan, isAccessAccepted, isPortAuthorized, type Dot1xRole } from '@/widgets/nac/dot1x'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

// Horizontale Position (in %) der drei Rollen entlang der Nachrichten-Spur.
// Bewusst nicht 0/50/100, damit der Marker (zentriert via translateX(-50%))
// nirgends über den Rand der Spur hinausragt.
const ROLE_X: Record<Dot1xRole, number> = { supplicant: 12, authenticator: 50, server: 88 }
const PLAY_DELAY_MS = 1700
const PLAY_DELAY_REDUCED_MS = 900

// Liest prefers-reduced-motion reaktiv aus (statt nur einmal beim Mount), da
// sich die OS-Einstellung während einer laufenden Sitzung ändern kann.
function useReducedMotion(): boolean {
  const [reduced, setReduced] = useState(
    () => typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches,
  )
  useEffect(() => {
    if (typeof window === 'undefined' || !window.matchMedia) return
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)')
    const handler = () => setReduced(mq.matches)
    mq.addEventListener('change', handler)
    return () => mq.removeEventListener('change', handler)
  }, [])
  return reduced
}

const STR = {
  de: {
    title: '802.1X-Handshake — Supplicant, Authenticator, Authentication Server',
    subtitle: 'Verfolge den Nachrichtenfluss der 802.1X-Authentifizierung: EAPOL zwischen Client und '
      + 'Switch, RADIUS zwischen Switch und Authentication Server.',
    supplicant: 'Supplicant', supplicantSub: 'Client / Laptop',
    authenticator: 'Authenticator', authenticatorSub: 'Switch / Access Point',
    server: 'Authentication Server', serverSub: 'RADIUS',
    play: 'Abspielen', pause: 'Pause',
    prev: 'Zurück', next: 'Nächster Schritt', reset: 'Von vorn',
    step: 'Schritt', of: 'von',
    eapol: 'EAPOL', radius: 'RADIUS',
    portUnauthorized: 'Port: unauthorized',
    portAuthorized: 'Port: authorized',
    vlanAssigned: 'zugewiesenes VLAN',
    challenge: 'Spiele den Ablauf einmal komplett ab oder klicke dich bis zum RADIUS Access-Accept durch.',
    reducedMotionNote: 'Bewegungsreduzierte Darstellung aktiv: Schritte erscheinen ohne Gleitbewegung.',
  },
  en: {
    title: '802.1X handshake — Supplicant, Authenticator, Authentication Server',
    subtitle: 'Follow the message flow of 802.1X authentication: EAPOL between client and switch, '
      + 'RADIUS between switch and authentication server.',
    supplicant: 'Supplicant', supplicantSub: 'Client / laptop',
    authenticator: 'Authenticator', authenticatorSub: 'Switch / access point',
    server: 'Authentication Server', serverSub: 'RADIUS',
    play: 'Play', pause: 'Pause',
    prev: 'Back', next: 'Next step', reset: 'Restart',
    step: 'Step', of: 'of',
    eapol: 'EAPOL', radius: 'RADIUS',
    portUnauthorized: 'Port: unauthorized',
    portAuthorized: 'Port: authorized',
    vlanAssigned: 'assigned VLAN',
    challenge: 'Play through the whole flow once, or click through it up to the RADIUS Access-Accept.',
    reducedMotionNote: 'Reduced-motion display active: steps appear without a gliding animation.',
  },
} as const

export function Dot1xFlow({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const reducedMotion = useReducedMotion()
  const [idx, setIdx] = useState(0)
  const [maxReached, setMaxReached] = useState(0)
  const [playing, setPlaying] = useState(false)
  const [markerLeft, setMarkerLeft] = useState(ROLE_X[DOT1X_STEPS[0].from])
  const [transitioning, setTransitioning] = useState(false)
  const rafRef = useRef<number[]>([])

  const step = DOT1X_STEPS[idx]
  const atEnd = idx === DOT1X_STEPS.length - 1
  const authorized = isPortAuthorized(maxReached)
  const done = isAccessAccepted(maxReached)

  useEffect(() => setMaxReached((m) => Math.max(m, idx)), [idx])

  // Marker entlang der Spur bewegen: instant zur Quelle springen, dann (ohne
  // reduced motion) im nächsten Frame per CSS-Transition zum Ziel gleiten.
  useEffect(() => {
    rafRef.current.forEach(cancelAnimationFrame)
    rafRef.current = []
    const fromX = ROLE_X[step.from]
    const toX = ROLE_X[step.to]
    if (reducedMotion) {
      setTransitioning(false)
      setMarkerLeft(toX)
      return
    }
    setTransitioning(false)
    setMarkerLeft(fromX)
    const raf1 = requestAnimationFrame(() => {
      const raf2 = requestAnimationFrame(() => {
        setTransitioning(true)
        setMarkerLeft(toX)
      })
      rafRef.current.push(raf2)
    })
    rafRef.current.push(raf1)
    return () => rafRef.current.forEach(cancelAnimationFrame)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [idx, reducedMotion])

  // Autoplay: schreitet Schritt für Schritt fort, bis der letzte Schritt
  // erreicht ist.
  useEffect(() => {
    if (!playing) return undefined
    if (atEnd) { setPlaying(false); return undefined }
    const delay = reducedMotion ? PLAY_DELAY_REDUCED_MS : PLAY_DELAY_MS
    const timer = setTimeout(() => setIdx((i) => Math.min(i + 1, DOT1X_STEPS.length - 1)), delay)
    return () => clearTimeout(timer)
  }, [playing, idx, atEnd, reducedMotion])

  const goNext = () => { setPlaying(false); setIdx((i) => Math.min(i + 1, DOT1X_STEPS.length - 1)) }
  const goPrev = () => { setPlaying(false); setIdx((i) => Math.max(i - 1, 0)) }
  const restart = () => { setPlaying(false); setIdx(0) }
  const togglePlay = () => { if (atEnd) setIdx(0); setPlaying((p) => !p) }

  const roleLabel = (role: Dot1xRole) =>
    role === 'supplicant' ? s.supplicant : role === 'authenticator' ? s.authenticator : s.server

  const roleActive = (role: Dot1xRole) => step.from === role || step.to === role

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-4">{s.subtitle}</p>

      <div className="grid grid-cols-3 gap-2 mb-1">
        {(['supplicant', 'authenticator', 'server'] as Dot1xRole[]).map((role) => (
          <div
            key={role}
            className={`rounded-lg border-2 px-2 py-2 text-center transition-colors ${
              roleActive(role) ? 'border-teal-600 bg-teal-50/60' : 'border-slate-200 bg-slate-50'
            }`}
          >
            <p className="text-xs font-semibold text-slate-700">{roleLabel(role)}</p>
            <p className="text-[10px] text-slate-500">
              {role === 'supplicant' ? s.supplicantSub : role === 'authenticator' ? s.authenticatorSub : s.serverSub}
            </p>
          </div>
        ))}
      </div>

      <div className="relative h-8 mb-3" aria-hidden="true">
        <div className="absolute left-[12%] right-[12%] top-1/2 h-px bg-slate-200" />
        <div
          className={`absolute top-1/2 -translate-y-1/2 -translate-x-1/2 rounded-full px-2 py-1 text-[10px] font-semibold whitespace-nowrap shadow ${
            step.layer === 'eapol' ? 'bg-teal-600 text-white' : 'bg-slate-700 text-white'
          }`}
          style={{
            left: `${markerLeft}%`,
            transition: transitioning ? 'left 650ms ease-in-out' : 'none',
          }}
        >
          {step.from === step.to ? step.name : (ROLE_X[step.to] > ROLE_X[step.from] ? '→ ' : '← ') + step.name}
        </div>
      </div>

      <p className="text-xs text-slate-500 mb-2">
        {s.step} {idx + 1} {s.of} {DOT1X_STEPS.length}
        <span className={`ml-3 rounded px-2 py-0.5 font-medium ${
          step.layer === 'eapol' ? 'bg-teal-100 text-teal-800' : 'bg-slate-100 text-slate-700'
        }`}>
          {step.layer === 'eapol' ? s.eapol : s.radius}
        </span>
      </p>

      <div className="rounded-lg border-2 border-teal-300 bg-teal-50/60 p-3 mb-3" aria-live="polite">
        <p className="text-xs font-semibold text-slate-600 mb-1">
          {roleLabel(step.from)} → {roleLabel(step.to)}
        </p>
        <p className="font-mono text-sm text-slate-800 mb-1">{step.name}</p>
        <p className="text-xs text-slate-600">{step.detail[lang]}</p>
      </div>

      {reducedMotion && (
        <p className="text-[11px] text-slate-400 mb-3">{s.reducedMotionNote}</p>
      )}

      <div className="flex flex-wrap gap-2 mb-4">
        <button
          onClick={goPrev}
          disabled={idx === 0}
          className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-default"
        >
          {s.prev}
        </button>
        <button
          onClick={togglePlay}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium"
        >
          {playing ? s.pause : s.play}
        </button>
        <button
          onClick={goNext}
          disabled={atEnd}
          className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-default"
        >
          {s.next}
        </button>
        <button
          onClick={restart}
          className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-50"
        >
          {s.reset}
        </button>
      </div>

      <div
        className={`rounded-lg border p-3 mb-1 text-sm font-medium ${
          authorized ? 'border-green-200 bg-green-50 text-green-800' : 'border-slate-200 bg-slate-50 text-slate-500'
        }`}
        aria-live="polite"
      >
        {authorized ? s.portAuthorized : s.portUnauthorized}
        {authorized && <span className="ml-2">· {s.vlanAssigned}: <strong>{finalVlan()}</strong></span>}
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={done} />
    </div>
  )
}
