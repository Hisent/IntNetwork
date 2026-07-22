// WebAuthn für den Trainer-Login/-Verwaltung — bewusst ohne Bibliothek
// (@simplewebauthn/browser o.ä.): der Browser liefert/erwartet ArrayBuffer,
// das Backend spricht ausschließlich Base64url (RFC 4648 §5, kein Padding).
// Die Umwandlung zwischen beiden Welten ist praktisch der gesamte Aufwand
// dieser Datei — der Rest ist ein dünner Aufruf von
// navigator.credentials.create()/.get().
import { trainerApi, type PasskeySummary, type PasskeyCreationOptionsJSON, type PasskeyRequestOptionsJSON } from '@/lib/trainerApi'

// --- Base64url ⇄ ArrayBuffer ---------------------------------------------------

/** Base64url (RFC 4648 §5: '-'/'_' statt '+'/'/', kein Padding) -> ArrayBuffer. */
export function base64UrlToBuffer(value: string): ArrayBuffer {
  const base64 = value.replace(/-/g, '+').replace(/_/g, '/')
  const padLength = (4 - (base64.length % 4)) % 4
  const padded = base64 + '='.repeat(padLength)
  const binary = atob(padded)
  const bytes = new Uint8Array(binary.length)
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i)
  return bytes.buffer
}

/** ArrayBuffer -> Base64url (ohne Padding), wie es das Backend erwartet. */
export function bufferToBase64Url(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer)
  let binary = ''
  for (const byte of bytes) binary += String.fromCharCode(byte)
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')
}

// --- Unterstützungs-Check -------------------------------------------------------

/**
 * WebAuthn gibt es nur unter HTTPS oder auf localhost. Auf einer nackten
 * HTTP-Instanz (z.B. internes Testsystem ohne Zertifikat) existiert
 * navigator.credentials zwar evtl. noch, ruft aber nie erfolgreich auf — der
 * Passkey-Knopf soll dort erst gar nicht erscheinen statt einen Fehler zu werfen.
 */
export function isPasskeySupported(): boolean {
  return typeof window !== 'undefined' && !!window.PublicKeyCredential && window.isSecureContext
}

/**
 * Bricht der Mensch den Systemdialog ab (oder es gibt keinen passenden
 * Authenticator), wirft der Browser NotAllowedError. Das ist eine normale
 * Rückzugsmöglichkeit, kein Anwendungsfehler — Aufrufer sollen dafür still in
 * den Ausgangszustand zurückkehren statt eine Fehlermeldung zu zeigen.
 */
export function isPasskeyCancelled(err: unknown): boolean {
  return err instanceof DOMException ? err.name === 'NotAllowedError' : (err as { name?: string })?.name === 'NotAllowedError'
}

// --- JSON-Optionen (vom Backend, siehe trainerApi.ts) -> WebAuthn-Optionen (ArrayBuffer) ---

function decodeCreationOptions(json: PasskeyCreationOptionsJSON): PublicKeyCredentialCreationOptions {
  return {
    ...json,
    challenge: base64UrlToBuffer(json.challenge),
    user: { ...json.user, id: base64UrlToBuffer(json.user.id) },
    excludeCredentials: json.excludeCredentials?.map((c) => ({ ...c, id: base64UrlToBuffer(c.id) })),
  }
}

function decodeRequestOptions(json: PasskeyRequestOptionsJSON): PublicKeyCredentialRequestOptions {
  return {
    ...json,
    challenge: base64UrlToBuffer(json.challenge),
    allowCredentials: json.allowCredentials?.map((c) => ({ ...c, id: base64UrlToBuffer(c.id) })),
  }
}

// --- WebAuthn-Antwort (ArrayBuffer) -> JSON (Base64url), fürs Backend --------

function encodeAttestationCredential(credential: PublicKeyCredential) {
  const response = credential.response as AuthenticatorAttestationResponse
  return {
    id: credential.id,
    rawId: bufferToBase64Url(credential.rawId),
    type: credential.type,
    response: {
      clientDataJSON: bufferToBase64Url(response.clientDataJSON),
      attestationObject: bufferToBase64Url(response.attestationObject),
      transports: response.getTransports?.(),
    },
    clientExtensionResults: credential.getClientExtensionResults(),
  }
}

function encodeAssertionCredential(credential: PublicKeyCredential) {
  const response = credential.response as AuthenticatorAssertionResponse
  return {
    id: credential.id,
    rawId: bufferToBase64Url(credential.rawId),
    type: credential.type,
    response: {
      clientDataJSON: bufferToBase64Url(response.clientDataJSON),
      authenticatorData: bufferToBase64Url(response.authenticatorData),
      signature: bufferToBase64Url(response.signature),
      userHandle: response.userHandle ? bufferToBase64Url(response.userHandle) : null,
    },
    clientExtensionResults: credential.getClientExtensionResults(),
  }
}

// --- Die beiden Ceremony-Funktionen --------------------------------------------

/** Registriert einen neuen Passkey für den eingeloggten Trainer. */
export async function registerPasskey(label: string): Promise<PasskeySummary> {
  const { data } = await trainerApi.passkeyRegisterOptions()
  const publicKey = decodeCreationOptions(data.publicKey)
  const credential = (await navigator.credentials.create({ publicKey })) as PublicKeyCredential
  const payload = encodeAttestationCredential(credential)
  const result = await trainerApi.passkeyRegisterVerify(payload, label)
  return result.data
}

/** Meldet den Trainer per Passkey an — liefert dasselbe wie der Passwort-Login. */
export async function loginWithPasskey(): Promise<{ access_token: string }> {
  const { data } = await trainerApi.passkeyLoginOptions()
  const publicKey = decodeRequestOptions(data.publicKey)
  const credential = (await navigator.credentials.get({ publicKey })) as PublicKeyCredential
  const payload = encodeAssertionCredential(credential)
  const result = await trainerApi.passkeyLoginVerify(payload)
  return result.data
}
