// Vier Vorlagen fürs Git-Lab (Modul cc_git_collaboration: Worktrees und
// Zusammenarbeit). Jede Vorlage ist für sich lauffähig in einem frischen
// Arbeitsverzeichnis; "checkout -" (statt eines festen Zweignamens wie
// "main"/"master") umgeht dabei bewusst die Frage, welchen
// Standard-Zweignamen `git init` auf dem Runner wählt. clone/fetch/push/pull
// fehlen hier absichtlich — kein Netzwerk im Runner, siehe Hinweis im Widget.
export interface GitTemplate {
  id: string
  title: { de: string; en: string }
  hint: { de: string; en: string }
  files: Record<string, string>
  commands: string[]
}

export const GIT_TEMPLATES: GitTemplate[] = [
  {
    id: 'init-commit',
    title: { de: 'Repository anlegen + erster Commit', en: 'Init repository + first commit' },
    hint: {
      de: 'Legt ein neues Repository an und erstellt den ersten Commit.',
      en: 'Creates a new repository and makes the first commit.',
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
      'checkout -b feature',
      'commit --allow-empty -m feature-work',
      'checkout -',
      'merge feature',
    ],
  },
  {
    id: 'merge-konflikt',
    title: { de: 'Merge-Konflikt herbeiführen', en: 'Provoke a merge conflict' },
    hint: {
      de: 'Erster Schritt: legt zwei Zweige an, die dieselbe Datei unterschiedlich ändern könnten. '
        + 'Lass diesen Lauf einmal laufen, dann trage als zweiten Lauf ein: checkout -, '
        + 'mv -f main-version.txt shared.txt, commit -am main-edit, merge feature, status, diff — '
        + 'das Arbeitsverzeichnis bleibt zwischen Läufen erhalten, der echte Konflikt erscheint erst dann.',
      en: 'First step: creates two branches that could each change the same file differently. '
        + 'Run this once, then enter as a second run: checkout -, mv -f main-version.txt shared.txt, '
        + 'commit -am main-edit, merge feature, status, diff — the workspace persists between runs, '
        + 'the real conflict only appears then.',
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
      'checkout -b feature',
      'mv -f feature-version.txt shared.txt',
      'commit -am feature-edit',
    ],
  },
  {
    id: 'worktree',
    title: { de: 'Worktree anlegen und auflisten', en: 'Add and list a worktree' },
    hint: {
      de: 'Für sich lauffähig: legt ein Repository mit einem Basis-Commit an, dann einen zweiten '
        + 'Arbeitsbaum für einen neuen Zweig.',
      en: 'Runnable on its own: creates a repository with a base commit, then a second working '
        + 'tree for a new branch.',
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
