import { useState } from 'react'
import { flipBit, toBase64, bytesToHex } from '@/widgets/pki/aead'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const DEFAULT_PLAINTEXT = 'Gehaltsanpassung: 4200 EUR ab 01.09.'
const DEFAULT_PASSWORD = 'Sommer2026!'

const PBKDF2_ITERATIONS = 150_000

const STR = {
  de: {
    title: 'AEAD — Verschlüsselung, die Manipulation erkennt',
    subtitle: 'AES-GCM ist ein AEAD-Verfahren (Authenticated Encryption with Associated Data): es verschlüsselt '
      + 'nicht nur, sondern hängt ein Authentifizierungs-Tag an. PBKDF2 leitet aus dem Passwort einen 256-Bit-Schlüssel ab.',
    plaintextLabel: 'Klartext',
    passwordLabel: 'Passwort',
    encrypt: 'Verschlüsseln',
    decrypt: 'Entschlüsseln',
    flipBit: 'Ein Bit im Geheimtext kippen',
    nonceLabel: 'Nonce / IV (12 Byte, hex)',
    ciphertextHexLabel: 'Geheimtext (Hex)',
    ciphertextB64Label: 'Geheimtext (Base64)',
    recoveredLabel: 'Wiederhergestellter Klartext',
    tamperedNote: 'Geheimtext wurde manipuliert (1 Bit gekippt).',
    authFailed: 'Entschlüsselung fehlgeschlagen: Die Authentifizierung hat nicht gestimmt (Tag ungültig). '
      + 'Das ist beabsichtigt — AEAD liefert entweder den vollständigen, unveränderten Klartext oder gar nichts. '
      + 'Es gibt keinen „halb entschlüsselten“ Zwischenzustand, weder bei einem manipulierten Geheimtext noch bei einem falschen Passwort.',
    nonceHint: 'Die Nonce/IV wird pro Nachricht neu zufällig erzeugt und niemals wiederverwendet. Wird derselbe '
      + 'Nonce mit demselben Schlüssel zweimal verwendet, bricht das bei AES-GCM sowohl die Vertraulichkeit als auch die Authentizität.',
    challenge: 'Verschlüssle, kippe ein Bit im Geheimtext (oder ändere das Passwort) und entschlüssle erneut — beobachte den kontrollierten Fehlschlag.',
    notEncryptedYet: 'Noch nicht verschlüsselt.',
  },
  en: {
    title: 'AEAD — encryption that detects tampering',
    subtitle: 'AES-GCM is an AEAD scheme (Authenticated Encryption with Associated Data): it not only encrypts, '
      + 'it also attaches an authentication tag. PBKDF2 derives a 256-bit key from the password.',
    plaintextLabel: 'Plaintext',
    passwordLabel: 'Password',
    encrypt: 'Encrypt',
    decrypt: 'Decrypt',
    flipBit: 'Flip one bit in the ciphertext',
    nonceLabel: 'Nonce / IV (12 bytes, hex)',
    ciphertextHexLabel: 'Ciphertext (hex)',
    ciphertextB64Label: 'Ciphertext (Base64)',
    recoveredLabel: 'Recovered plaintext',
    tamperedNote: 'Ciphertext has been tampered with (1 bit flipped).',
    authFailed: 'Decryption failed: authentication did not check out (invalid tag). This is by design — AEAD '
      + 'delivers either the complete, unmodified plaintext or nothing at all. There is no "half-decrypted" '
      + 'in-between state, whether the ciphertext was tampered with or the password was wrong.',
    nonceHint: 'The nonce/IV is freshly randomized for every message and never reused. Reusing the same nonce '
      + 'with the same key twice breaks both confidentiality and authenticity under AES-GCM.',
    challenge: 'Encrypt, flip a bit in the ciphertext (or change the password) and decrypt again — observe the controlled failure.',
    notEncryptedYet: 'Not encrypted yet.',
  },
} as const

interface Encrypted {
  salt: Uint8Array<ArrayBuffer>
  iv: Uint8Array<ArrayBuffer>
  ciphertext: Uint8Array<ArrayBuffer>
}

async function deriveKey(password: string, salt: Uint8Array<ArrayBuffer>, usage: KeyUsage[]): Promise<CryptoKey> {
  const material = await crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveKey'])
  return crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations: PBKDF2_ITERATIONS, hash: 'SHA-256' },
    material,
    { name: 'AES-GCM', length: 256 },
    false,
    usage,
  )
}

export function AeadLab({ lang }: { lang: Lang }) {
  const [plaintext, setPlaintext] = useState(DEFAULT_PLAINTEXT)
  const [password, setPassword] = useState(DEFAULT_PASSWORD)
  const [enc, setEnc] = useState<Encrypted | null>(null)
  const [tampered, setTampered] = useState(false)
  const [recovered, setRecovered] = useState<string | null>(null)
  const [authError, setAuthError] = useState(false)
  const s = STR[lang]

  const handleEncrypt = async () => {
    const salt = crypto.getRandomValues(new Uint8Array(16))
    const iv = crypto.getRandomValues(new Uint8Array(12))
    const key = await deriveKey(password, salt, ['encrypt'])
    const buffer = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, new TextEncoder().encode(plaintext))
    setEnc({ salt, iv, ciphertext: new Uint8Array(buffer) })
    setTampered(false)
    setRecovered(null)
    setAuthError(false)
  }

  const handleFlipBit = () => {
    if (!enc) return
    const index = Math.floor(Math.random() * enc.ciphertext.length * 8)
    setEnc({ ...enc, ciphertext: flipBit(enc.ciphertext, index) as Uint8Array<ArrayBuffer> })
    setTampered(true)
    setRecovered(null)
    setAuthError(false)
  }

  const handleDecrypt = async () => {
    if (!enc) return
    try {
      const key = await deriveKey(password, enc.salt, ['decrypt'])
      const buffer = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: enc.iv }, key, enc.ciphertext)
      setRecovered(new TextDecoder().decode(buffer))
      setAuthError(false)
    } catch {
      setRecovered(null)
      setAuthError(true)
    }
  }

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-4">{s.subtitle}</p>

      <label htmlFor="aead-plaintext" className="mb-1 block text-xs font-semibold text-slate-500">{s.plaintextLabel}</label>
      <input
        id="aead-plaintext"
        value={plaintext}
        onChange={(e) => setPlaintext(e.target.value)}
        className="mb-3 w-full rounded-lg border border-slate-300 px-3 py-1.5 text-sm outline-none focus:border-teal-500"
      />

      <label htmlFor="aead-password" className="mb-1 block text-xs font-semibold text-slate-500">{s.passwordLabel}</label>
      <input
        id="aead-password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="mb-3 w-full rounded-lg border border-slate-300 px-3 py-1.5 text-sm outline-none focus:border-teal-500"
      />

      <div className="mb-4 flex flex-wrap gap-2">
        <button
          onClick={handleEncrypt}
          className="rounded-lg bg-teal-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-teal-700"
        >
          {s.encrypt}
        </button>
        <button
          onClick={handleFlipBit}
          disabled={!enc}
          className="rounded-lg border border-amber-300 px-3 py-1.5 text-sm font-medium text-amber-800 hover:bg-amber-50 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {s.flipBit}
        </button>
        <button
          onClick={handleDecrypt}
          disabled={!enc}
          className="rounded-lg border border-teal-300 px-3 py-1.5 text-sm font-medium text-teal-700 hover:bg-teal-50 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {s.decrypt}
        </button>
      </div>

      <div className="rounded-lg border border-slate-200 bg-slate-50 p-3" aria-live="polite">
        {enc ? (
          <>
            <p className="mb-1 text-xs font-semibold text-slate-500">{s.nonceLabel}</p>
            <p className="mb-2 break-all font-mono text-xs text-slate-800">{bytesToHex(enc.iv)}</p>
            <p className="mb-1 text-xs font-semibold text-slate-500">{s.ciphertextHexLabel}</p>
            <p className="mb-2 break-all font-mono text-xs text-slate-800">{bytesToHex(enc.ciphertext)}</p>
            <p className="mb-1 text-xs font-semibold text-slate-500">{s.ciphertextB64Label}</p>
            <p className="break-all font-mono text-xs text-slate-800">{toBase64(enc.ciphertext)}</p>
            {tampered && (
              <p className="mt-2 text-xs font-medium text-amber-800">{s.tamperedNote}</p>
            )}
          </>
        ) : (
          <p className="text-xs text-slate-400">{s.notEncryptedYet}</p>
        )}
      </div>

      {recovered !== null && (
        <div className="mt-3 rounded-lg border border-green-200 bg-green-50 p-3" aria-live="polite">
          <p className="mb-1 text-xs font-semibold text-green-700">{s.recoveredLabel}</p>
          <p className="break-all font-mono text-xs text-green-900">{recovered}</p>
        </div>
      )}

      {authError && (
        <div className="mt-3 rounded-lg border border-rose-300 bg-rose-50 p-3 text-xs text-rose-900" aria-live="polite">
          {s.authFailed}
        </div>
      )}

      <p className="mt-4 text-xs text-slate-500">{s.nonceHint}</p>

      <ChallengeBox lang={lang} task={s.challenge} done={authError} />
    </div>
  )
}
