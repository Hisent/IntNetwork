// Die Uebungen schreiben ausschliesslich nach {{ lab_dir }} — das ist das
// teilnehmereigene Verzeichnis im Runner (siehe runner/worker.py). Feste Pfade wie
// /tmp/uebung waeren fuer alle Teilnehmenden dasselbe Verzeichnis: Der zweite
// Mensch saehe dann beim ERSTEN Lauf schon "nichts geaendert" und die
// Idempotenz-Uebung ginge ins Leere.
// Sechs Übungsvorlagen für das Ansible-Lab. Jede ist ein lauffähiges (bzw. im
// Fall "Fehler lesen" absichtlich kaputtes, aber reparierbares) Playbook, das
// nur unter {{ lab_dir }} im Container schreibt — kein Netzwerk, kein Zugriff auf den
// Host. Aufgabentexte bilingual, analog zu den STR-Konstanten der Widgets.
// Der Runner kennt nur ansible-core (ansible.builtin.*) und nimmt genau EINE
// Playbook-Datei an: Die Template-Übung legt ihre .j2-Quelle deshalb selbst per
// copy ab, statt eine zweite Datei vorauszusetzen.
import type { RecapTotals } from '@/widgets/ansiblelab/labOutput'

/** Was die Challenge einer Übung über den letzten Lauf wissen darf. */
export interface ChallengeState {
  /** Recap des letzten Laufs; null = noch kein Lauf oder Abbruch vor dem Recap. */
  recap: RecapTotals | null
  /** Rohausgabe des letzten Laufs ('' = noch kein Lauf). */
  output: string
  /** true, sobald der letzte Lauf ein echter (kein --check) Folgelauf war. */
  rerun: boolean
}

export interface LabExercise {
  id: string
  /** Modul-Key (backend/app/content/an_*.py), in dem diese Übung vorgewählt wird. */
  module: string
  title: { de: string; en: string }
  task: { de: string; en: string }
  challenge: { de: string; en: string }
  /** Zielzustand der Challenge, live aus dem letzten Lauf berechnet (ungewertet). */
  done: (state: ChallengeState) => boolean
  playbook: string
}

const clean = (s: ChallengeState) => s.recap !== null && s.recap.failed === 0

export const EXERCISES: LabExercise[] = [
  {
    id: 'idempotenz',
    module: 'fehlerbehandlung-idempotenz',
    title: { de: 'Idempotenz', en: 'Idempotency' },
    task: {
      de: 'Lass das Playbook zweimal laufen (Ausführen, nicht --check). Vergleiche die changed-Zahl '
        + 'zwischen erstem und zweitem Lauf und erkläre, warum sie unterschiedlich ausfällt.',
      en: 'Run the playbook twice (Run, not --check). Compare the changed count between the first '
        + 'and second run and explain why it differs.',
    },
    challenge: {
      de: 'Lass dasselbe Playbook zweimal laufen und erkläre den Unterschied.',
      en: 'Run the same playbook twice and explain the difference.',
    },
    done: (s) => s.rerun && s.recap !== null,
    playbook: `---
- hosts: all
  tasks:
    - name: Verzeichnis anlegen
      ansible.builtin.file:
        path: "{{ lab_dir }}/idempotenz"
        state: directory

    - name: Datei mit Inhalt anlegen
      ansible.builtin.copy:
        content: "Hallo vom Ansible-Lab\\n"
        dest: "{{ lab_dir }}/idempotenz/hello.txt"

    - name: Zeitstempel protokollieren
      ansible.builtin.command: echo "Lauf ausgeführt"
      changed_when: true
`,
  },
  {
    id: 'fehler-lesen',
    module: 'playbooks-grundlagen',
    title: { de: 'Fehler lesen', en: 'Reading errors' },
    task: {
      de: 'Dieses Playbook enthält einen falschen Modulnamen. Lass es laufen, lies die Fehlermeldung, '
        + 'repariere den Modulnamen im Editor (ansible.builtin.file statt ansible.builtin.filee) und lass es erneut laufen.',
      en: 'This playbook has a wrong module name. Run it, read the error message, fix the module '
        + 'name in the editor (ansible.builtin.file instead of ansible.builtin.filee), and run it again.',
    },
    challenge: {
      de: 'Repariere den Modulnamen, bis der Lauf ein PLAY RECAP mit failed=0 zeigt.',
      en: 'Fix the module name until the run shows a PLAY RECAP with failed=0.',
    },
    done: clean,
    playbook: `---
- hosts: all
  tasks:
    - name: Ordner für Notizen anlegen
      ansible.builtin.filee:
        path: "{{ lab_dir }}/notizen"
        state: directory
`,
  },
  {
    id: 'kontrollfluss',
    module: 'schleifen-handler',
    title: { de: 'Kontrollfluss', en: 'Control flow' },
    task: {
      de: 'Lass das Playbook laufen und sieh dir die Ausgabe an: Welches Element wird per when '
        + 'übersprungen (skipped)? Wann feuert der per notify angestoßene Handler?',
      en: 'Run the playbook and look at the output: which loop item gets skipped by when? '
        + 'When does the notify-triggered handler fire?',
    },
    challenge: {
      de: 'Ändere die when-Bedingung so, dass auch beta angelegt wird, und lass erneut laufen: Feuert der Handler wieder?',
      en: 'Change the when condition so that beta is created as well, then run again: does the handler fire again?',
    },
    // Ein per when übersprungenes Schleifenelement zählt im Recap NICHT als skipped
    // (real geprüft: skipped=0) — messbar ist nur, dass der Folgelauf wieder ändert.
    done: (s) => s.rerun && clean(s) && (s.recap?.changed ?? 0) > 0,
    playbook: `---
- hosts: all
  vars:
    pakete:
      - alpha
      - beta
      - gamma
  tasks:
    - name: Arbeitsverzeichnis anlegen
      ansible.builtin.file:
        path: "{{ lab_dir }}/kontrollfluss"
        state: directory

    - name: Datei je Paket anlegen, außer für beta
      ansible.builtin.copy:
        content: "Paket {{ item }}\\n"
        dest: "{{ lab_dir }}/kontrollfluss/{{ item }}.txt"
      loop: "{{ pakete }}"
      when: item != 'beta'
      notify: Übersicht aktualisieren

  handlers:
    - name: Übersicht aktualisieren
      ansible.builtin.command: echo "Übersicht aktualisiert"
      changed_when: true
`,
  },
  {
    id: 'variablen-vorrang',
    module: 'variablen-vorrang',
    title: { de: 'Variablen-Vorrang', en: 'Variable precedence' },
    task: {
      de: 'Lass das Playbook einmal ohne Extra-Vars laufen (Ausgabe zeigt "staging"). Trage dann im '
        + 'Feld „Extra-Vars“ umgebung=produktion ein und lass es erneut laufen — welcher Wert gewinnt?',
      en: 'Run the playbook once without extra vars (output shows "staging"). Then enter '
        + 'umgebung=produktion in the "Extra vars" field and run it again — which value wins?',
    },
    challenge: {
      de: 'Bring die Ausgabe ohne Änderung am Playbook dazu, eine andere Umgebung als staging zu zeigen.',
      en: 'Without editing the playbook, make the output show an environment other than staging.',
    },
    done: (s) => clean(s) && s.output.includes('Aktive Umgebung:') && !s.output.includes('Aktive Umgebung: staging'),
    playbook: `---
- hosts: all
  vars:
    umgebung: staging
  tasks:
    - name: Umgebung ausgeben
      ansible.builtin.debug:
        msg: "Aktive Umgebung: {{ umgebung }}"
`,
  },
  {
    id: 'templates',
    module: 'templates-jinja2',
    title: { de: 'Templates', en: 'Templates' },
    task: {
      de: 'Das Playbook legt eine Jinja2-Vorlage ab und rendert sie mit ansible.builtin.template. '
        + 'Lass es laufen und lies den Diff: Was wurde aus {{ http_port }}, der for-Schleife und dem '
        + 'if-Block (tls_aktiv ist nicht gesetzt)?',
      en: 'The playbook stores a Jinja2 template and renders it with ansible.builtin.template. Run it '
        + 'and read the diff: what became of {{ http_port }}, the for loop and the if block '
        + '(tls_aktiv is not set)?',
    },
    challenge: {
      de: 'Ändere http_port oder ergänze eine Domain und lass erneut laufen: Der Diff zeigt nur noch die geänderten Zeilen.',
      en: 'Change http_port or add a domain and run again: the diff now shows only the changed lines.',
    },
    done: (s) => s.rerun && clean(s) && (s.recap?.changed ?? 0) > 0,
    playbook: `---
- hosts: all
  vars:
    http_port: 8080
    server_names:
      - intranet.example.com
      - wiki.example.com
  tasks:
    - name: Arbeitsverzeichnis anlegen
      ansible.builtin.file:
        path: "{{ lab_dir }}/templates"
        state: directory
        mode: "0755"
      check_mode: false

    # !unsafe: Der Inhalt wird hier NICHT gerendert, sondern roh als .j2 abgelegt.
    # check_mode: false: auch bei --check ablegen, sonst fehlt dem Rendern die Quelle.
    - name: Vorlage site.conf.j2 ablegen
      ansible.builtin.copy:
        dest: "{{ lab_dir }}/templates/site.conf.j2"
        mode: "0644"
        content: !unsafe |
          # Verwaltet von Ansible auf {{ inventory_hostname }}
          server {
              listen {{ http_port | default(80) }};
          {% for domain in server_names %}
              server_name {{ domain }};
          {% endfor %}
          {% if tls_aktiv | default(false) %}
              ssl_certificate /etc/ssl/{{ server_names | first }}.pem;
          {% endif %}
          }
      check_mode: false

    - name: Vorlage rendern
      ansible.builtin.template:
        src: "{{ lab_dir }}/templates/site.conf.j2"
        dest: "{{ lab_dir }}/templates/site.conf"
        mode: "0644"
      diff: true
`,
  },
  {
    id: 'fakten',
    module: 'fakten-bedingungen',
    title: { de: 'Fakten & when', en: 'Facts & when' },
    task: {
      de: 'Lass das Playbook laufen: Welche Facts meldet der Lab-Host, welcher der beiden '
        + 'Betriebssystem-Tasks wird übersprungen, und warum läuft der letzte Task?',
      en: 'Run the playbook: which facts does the lab host report, which of the two operating system '
        + 'tasks is skipped, and why does the last task run?',
    },
    challenge: {
      de: 'Trage bei Extra-Vars min_ram_mb=99999999 ein: Jetzt muss auch der letzte Task skipped melden.',
      en: 'Enter min_ram_mb=99999999 as extra vars: now the last task must report skipped as well.',
    },
    // Im Lab-Container (Debian) ist ohnehin ein OS-Task skipped; zwei heisst: der RAM-Task auch.
    done: (s) => clean(s) && (s.recap?.skipped ?? 0) >= 2,
    playbook: `---
- hosts: all
  gather_facts: true
  vars:
    min_ram_mb: 256
  tasks:
    - name: Ausgewählte Facts anzeigen
      ansible.builtin.debug:
        msg:
          - "Familie: {{ ansible_facts['os_family'] }}"
          - "Distribution: {{ ansible_facts['distribution'] }} {{ ansible_facts['distribution_version'] }}"
          - "RAM in MB: {{ ansible_facts['memtotal_mb'] }}"

    - name: Nur auf Debian-artigen Systemen
      ansible.builtin.debug:
        msg: "Hier wäre ansible.builtin.apt das passende Paketmodul."
      when: ansible_facts['os_family'] == "Debian"

    - name: Nur auf RedHat-artigen Systemen
      ansible.builtin.debug:
        msg: "Hier wäre ansible.builtin.dnf das passende Paketmodul."
      when: ansible_facts['os_family'] == "RedHat"

    # check_mode: false: reiner Lesebefehl, darf auch bei --check laufen.
    - name: Kernel-Version abfragen (nur lesen)
      ansible.builtin.command: uname -r
      register: kernel
      changed_when: false
      check_mode: false

    # Extra-Vars der Form schluessel=wert sind Strings, deshalb "| int".
    - name: Nur bei erfolgreicher Abfrage und genug Arbeitsspeicher
      ansible.builtin.debug:
        msg: "Kernel {{ kernel.stdout }}: genug Speicher für den Agenten."
      when:
        - kernel.rc == 0
        - ansible_facts['memtotal_mb'] >= (min_ram_mb | int)
`,
  },
]

export const DEFAULT_EXERCISE = EXERCISES[0]

export function exerciseById(id: string): LabExercise {
  return EXERCISES.find((e) => e.id === id) ?? DEFAULT_EXERCISE
}

/** Übung, die zum Modul gehört (Modul-Key aus der URL), sonst undefined. */
export function exerciseForModule(moduleKey: string | undefined): LabExercise | undefined {
  return moduleKey ? EXERCISES.find((e) => e.module === moduleKey) : undefined
}
