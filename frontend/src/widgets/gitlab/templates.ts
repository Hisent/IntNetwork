// Fünf Vorlagen fürs Git-Lab (Modul cc_git_collaboration: Worktrees und
// Zusammenarbeit). Jede Vorlage außer "merge-konflikt-2" ist für sich lauffähig
// in einem frischen Arbeitsverzeichnis. Das Arbeitsverzeichnis ist je Teilnehmer
// EINES für alle Vorlagen und bleibt erhalten: deshalb "checkout -B" (legt den
// Zweig an ODER setzt ihn zurück) statt "-b", das beim zweiten Lauf scheitert.
// Die Dateien einer Vorlage schreibt der Runner bei JEDEM Lauf neu — ein
// Folgeschritt, der auf dem Stand des ersten aufbaut, braucht daher eine eigene
// Vorlage ohne Dateien (real nachgestellt: sonst bricht "checkout -" mit
// "local changes would be overwritten" ab). "checkout -" (statt eines festen Zweignamens wie
// "main"/"master") umgeht dabei bewusst die Frage, welchen
// Standard-Zweignamen `git init` auf dem Runner wählt. clone/fetch/push/pull
// fehlen hier absichtlich — kein Netzwerk im Runner, siehe Hinweis im Widget.
import type { RunExpectation } from '@/widgets/lab/limits'

export interface GitTemplate {
  id: string
  title: { de: string; en: string }
  hint: { de: string; en: string }
  files: Record<string, string>
  commands: string[]
  expect?: RunExpectation
}

export const GIT_TEMPLATES: GitTemplate[] = [
  {
    id: 'init-commit',
    title: { de: 'Repository anlegen + erster Commit', en: 'Init repository + first commit' },
    hint: {
      de: 'Legt ein neues Repository an und erstellt den ersten Commit. Ein zweiter Lauf endet mit '
        + '„nothing to commit“ und Rückgabewert 1 — echtes git-Verhalten: Es gibt nichts Neues.',
      en: 'Creates a new repository and makes the first commit. A second run ends with '
        + '"nothing to commit" and return code 1 — real git behavior: there is nothing new.',
    },
    files: { 'README.md': '# Kurs-Repo\n' },
    commands: ['init', 'add .', 'commit -m start'],
  },
  {
    id: 'branch-merge',
    title: { de: 'Zweig anlegen, wechseln, zusammenführen', en: 'Branch, switch, merge' },
    hint: {
      de: 'Für sich lauffähig: legt selbst ein Repository mit einem Basis-Commit an, verzweigt, '
        + 'kehrt zum Ausgangszweig zurück und führt zusammen.',
      en: 'Runnable on its own: creates its own repository with a base commit, branches off, '
        + 'switches back to the starting branch and merges.',
    },
    files: {},
    commands: [
      'init',
      'commit --allow-empty -m base',
      'checkout -B feature',
      'commit --allow-empty -m feature-work',
      'checkout -',
      'merge feature',
    ],
  },
  {
    id: 'merge-konflikt',
    title: { de: 'Merge-Konflikt, Schritt 1: zwei Zweige vorbereiten', en: 'Merge conflict, step 1: prepare two branches' },
    hint: {
      de: 'Legt einen Basis-Commit an und ändert shared.txt auf dem Zweig feature. Danach die Vorlage '
        + '„Merge-Konflikt, Schritt 2“ wählen — sie bringt bewusst keine Dateien mit, denn die Dateien '
        + 'einer Vorlage werden bei jedem Lauf neu ins Arbeitsverzeichnis geschrieben und würden den '
        + 'Stand aus Schritt 1 überschreiben.',
      en: 'Creates a base commit and changes shared.txt on the feature branch. Then pick the template '
        + '"Merge conflict, step 2" — it deliberately ships no files, because the files of a template are '
        + 'written into the workspace again on every run and would overwrite the state from step 1.',
    },
    files: {
      'shared.txt': 'Zeile von main\n',
      'feature-version.txt': 'Zeile von feature\n',
      'main-version.txt': 'Andere Zeile von main\n',
    },
    commands: [
      'init',
      'add shared.txt feature-version.txt main-version.txt',
      'commit -m base',
      'checkout -B feature',
      'mv -f feature-version.txt shared.txt',
      'commit -am feature-edit',
    ],
  },
  {
    id: 'merge-konflikt-2',
    title: { de: 'Merge-Konflikt, Schritt 2: Konflikt auslösen', en: 'Merge conflict, step 2: trigger the conflict' },
    hint: {
      de: 'Setzt Schritt 1 voraus. Wechselt zurück auf den Ausgangszweig, ändert dort dieselbe Datei anders '
        + 'und führt zusammen: git meldet „CONFLICT“ und Rückgabewert 1 — das ist hier das erwartete Ergebnis. '
        + 'Ersetze danach die Befehle durch status und diff, um die Konfliktmarkierungen zu sehen; '
        + 'merge --abort räumt wieder auf.',
      en: 'Requires step 1. Switches back to the starting branch, changes the same file differently there '
        + 'and merges: git reports "CONFLICT" and return code 1 — the expected result here. Then replace the '
        + 'commands with status and diff to see the conflict markers; merge --abort cleans up again.',
    },
    files: {},
    commands: [
      'checkout -',
      'mv -f main-version.txt shared.txt',
      'commit -m main-edit',
      'merge feature',
    ],
    expect: {
      rc: 1,
      output: 'CONFLICT',
      task: {
        de: 'Führe einen Lauf aus, dessen letzter Befehl „CONFLICT“ meldet (Rückgabewert 1).',
        en: 'Run a command batch whose last command reports "CONFLICT" (return code 1).',
      },
    },
  },
  {
    id: 'worktree',
    title: { de: 'Worktree anlegen und auflisten', en: 'Add and list a worktree' },
    hint: {
      de: 'Für sich lauffähig: legt ein Repository mit einem Basis-Commit an, dann einen zweiten '
        + 'Arbeitsbaum für einen neuen Zweig. Ein zweiter Lauf scheitert mit „already exists“ — der '
        + 'Arbeitsbaum ist ja schon da; worktree list allein zeigt ihn weiterhin.',
      en: 'Runnable on its own: creates a repository with a base commit, then a second working '
        + 'tree for a new branch. A second run fails with "already exists" — the working tree is '
        + 'already there; worktree list on its own still shows it.',
    },
    files: {},
    commands: [
      'init',
      'commit --allow-empty -m base',
      'worktree add wt-feature -b feature-wt',
      'worktree list',
    ],
  },
]

export const DEFAULT_TEMPLATE = GIT_TEMPLATES[0]

export function templateById(id: string): GitTemplate {
  return GIT_TEMPLATES.find((t) => t.id === id) ?? DEFAULT_TEMPLATE
}
