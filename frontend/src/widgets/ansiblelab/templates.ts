// Die Uebungen schreiben ausschliesslich nach {{ lab_dir }} — das ist das
// teilnehmereigene Verzeichnis im Runner (siehe runner/app.py). Feste Pfade wie
// /tmp/uebung waeren fuer alle Teilnehmenden dasselbe Verzeichnis: Der zweite
// Mensch saehe dann beim ERSTEN Lauf schon "nichts geaendert" und die
// Idempotenz-Uebung ginge ins Leere.
// Vier Übungsvorlagen für das Ansible-Lab. Jede ist ein lauffähiges (bzw. im
// Fall "Fehler lesen" absichtlich kaputtes, aber reparierbares) Playbook, das
// nur unter /tmp im Container schreibt — kein Netzwerk, kein Zugriff auf den
// Host. Aufgabentexte bilingual, analog zu den STR-Konstanten der Widgets.
export interface LabExercise {
  id: string
  title: { de: string; en: string }
  task: { de: string; en: string }
  playbook: string
}

export const EXERCISES: LabExercise[] = [
  {
    id: 'idempotenz',
    title: { de: 'Idempotenz', en: 'Idempotency' },
    task: {
      de: 'Lass das Playbook zweimal laufen (Ausführen, nicht --check). Vergleiche die changed-Zahl '
        + 'zwischen erstem und zweitem Lauf und erkläre, warum sie unterschiedlich ausfällt.',
      en: 'Run the playbook twice (Run, not --check). Compare the changed count between the first '
        + 'and second run and explain why it differs.',
    },
    playbook: `---
- hosts: all
  tasks:
    - name: Verzeichnis anlegen
      file:
        path: "{{ lab_dir }}/idempotenz"
        state: directory

    - name: Datei mit Inhalt anlegen
      copy:
        content: "Hallo vom Ansible-Lab\\n"
        dest: "{{ lab_dir }}/idempotenz/hello.txt"

    - name: Zeitstempel protokollieren
      command: echo "Lauf ausgeführt"
      changed_when: true
`,
  },
  {
    id: 'fehler-lesen',
    title: { de: 'Fehler lesen', en: 'Reading errors' },
    task: {
      de: 'Dieses Playbook enthält einen falschen Modulnamen. Lass es laufen, lies die Fehlermeldung, '
        + 'repariere den Modulnamen im Editor (file statt filee) und lass es erneut laufen.',
      en: 'This playbook has a wrong module name. Run it, read the error message, fix the module '
        + 'name in the editor (file instead of filee), and run it again.',
    },
    playbook: `---
- hosts: all
  tasks:
    - name: Ordner für Notizen anlegen
      filee:
        path: "{{ lab_dir }}/notizen"
        state: directory
`,
  },
  {
    id: 'kontrollfluss',
    title: { de: 'Kontrollfluss', en: 'Control flow' },
    task: {
      de: 'Lass das Playbook laufen und sieh dir die Ausgabe an: Welches Element wird per when '
        + 'übersprungen (skipped)? Wann feuert der per notify angestoßene Handler?',
      en: 'Run the playbook and look at the output: which loop item gets skipped by when? '
        + 'When does the notify-triggered handler fire?',
    },
    playbook: `---
- hosts: all
  vars:
    pakete:
      - alpha
      - beta
      - gamma
  tasks:
    - name: Arbeitsverzeichnis anlegen
      file:
        path: "{{ lab_dir }}/kontrollfluss"
        state: directory

    - name: Datei je Paket anlegen, außer für beta
      copy:
        content: "Paket {{ item }}\\n"
        dest: "{{ lab_dir }}/kontrollfluss/{{ item }}.txt"
      loop: "{{ pakete }}"
      when: item != 'beta'
      notify: Übersicht aktualisieren

  handlers:
    - name: Übersicht aktualisieren
      command: echo "Übersicht aktualisiert"
      changed_when: true
`,
  },
  {
    id: 'variablen-vorrang',
    title: { de: 'Variablen-Vorrang', en: 'Variable precedence' },
    task: {
      de: 'Lass das Playbook einmal ohne Extra-Vars laufen (Ausgabe zeigt "staging"). Trage dann im '
        + 'Feld „Extra-Vars“ umgebung=produktion ein und lass es erneut laufen — welcher Wert gewinnt?',
      en: 'Run the playbook once without extra vars (output shows "staging"). Then enter '
        + 'umgebung=produktion in the "Extra vars" field and run it again — which value wins?',
    },
    playbook: `---
- hosts: all
  vars:
    umgebung: staging
  tasks:
    - name: Umgebung ausgeben
      debug:
        msg: "Aktive Umgebung: {{ umgebung }}"
`,
  },
]

export const DEFAULT_EXERCISE = EXERCISES[0]

export function exerciseById(id: string): LabExercise {
  return EXERCISES.find((e) => e.id === id) ?? DEFAULT_EXERCISE
}
