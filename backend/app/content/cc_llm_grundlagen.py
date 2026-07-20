# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

LLM_GRUNDLAGEN_MODULE = {'key': 'llm-grundlagen',
 'title': 'LLMs, Transformer & Tokenisierung',
 'title_en': 'LLMs, Transformers & Tokenization',
 'order': 101,
 'prerequisites': [],
 'goals': ['Erklären, wie ein LLM Text erzeugt (nächstes Token vorhersagen)',
           'Die Rolle von Transformer und Attention grob einordnen',
           'Tokenisierung und Kontextfenster verstehen und ihre Grenzen kennen',
           'Verstehen, warum Kontext-Qualität die Antwortqualität bestimmt'],
 'scenario': {'de': 'Bevor wir Claude Code sinnvoll steuern, brauchen wir ein mentales Modell '
                    'davon, was darunter arbeitet. Ein Large Language Model ist kein '
                    'Nachschlagewerk und kein deterministischer Compiler — es sagt **Wort für '
                    'Wort** das jeweils wahrscheinlichste nächste Stück Text voraus. Wer das '
                    'verinnerlicht, versteht auch, warum guter Kontext, klare Anweisungen und ein '
                    'aufgeräumtes Kontextfenster den Unterschied machen.',
              'en': 'Before we can control Claude Code effectively, we need a mental model of '
                    "what's working underneath. A Large Language Model is not a reference work and "
                    'not a deterministic compiler — it predicts the most likely next piece of text '
                    '**word by word**. Anyone who internalizes this also understands why good '
                    'context, clear instructions, and a tidy context window make all the '
                    'difference.'},
 'blocks': [{'type': 'text',
             'value': {'de': '## Was ein LLM eigentlich tut\n'
                             '\n'
                             'Ein **Large Language Model (LLM)** wie Claude ist auf eine scheinbar '
                             'simple Aufgabe trainiert: Gegeben ein Stück Text, sage das **nächste '
                             'Token** voraus. Diese Vorhersage wird immer wieder angewandt — Token '
                             'für Token entsteht so eine Antwort (*autoregressive Generierung*).\n'
                             '\n'
                             'Aus dieser einen Fähigkeit entstehen durch massives Training '
                             'erstaunlich viele: Code schreiben, Fehler erklären, Texte '
                             'zusammenfassen. Wichtig fürs mentale Modell:\n'
                             '\n'
                             '- Das Modell **rechnet Wahrscheinlichkeiten**, es „weiß” nichts im '
                             'menschlichen Sinn.\n'
                             '- Gleiche Eingabe kann leicht **unterschiedliche** Ausgaben liefern '
                             '(Sampling / Temperatur).\n'
                             '- Es kann **plausibel klingenden Unsinn** erzeugen (*Halluzination*) '
                             '— deshalb verifizieren wir Ergebnisse.',
                       'en': '## What an LLM actually does\n'
                             '\n'
                             'A **Large Language Model (LLM)** like Claude is trained on a '
                             'seemingly simple task: given a piece of text, predict the **next '
                             'token**. This prediction is applied over and over — token by token, '
                             'a response emerges (*autoregressive generation*).\n'
                             '\n'
                             'From this single capability, massive training gives rise to a '
                             'surprising range of others: writing code, explaining errors, '
                             'summarizing texts. What matters for the mental model:\n'
                             '\n'
                             '- The model **computes probabilities**; it doesn\'t "know" anything '
                             'in the human sense.\n'
                             '- The same input can yield **different** outputs (sampling / '
                             'temperature).\n'
                             '- It can produce **plausible-sounding nonsense** (*hallucination*) — '
                             'which is why we verify results.'},
             'note': 'Live am Tokenizer zeigen, dass Umlaute/Bezeichner in mehrere Tokens '
                     'zerfallen; das Kontextfenster als endliche Ressource betonen.'},
            {'type': 'text',
             'value': {'de': '## Der Transformer & Attention (in aller Kürze)\n'
                             '\n'
                             'Moderne LLMs beruhen auf der **Transformer**-Architektur (2017). Ihr '
                             'Kern ist der **Attention-Mechanismus**: Jedes Token kann beim '
                             'Verarbeiten auf *alle anderen* Tokens im Kontext „schauen” und '
                             'gewichten, welche gerade relevant sind. So erfasst das Modell '
                             'Zusammenhänge über weite Distanzen — etwa dass sich ein `return` '
                             'weit unten auf eine Funktionssignatur weit oben bezieht.\n'
                             '\n'
                             'Für den Workshop reicht diese Intuition: **Attention = das Modell '
                             'verknüpft Kontext.** Je klarer und relevanter der Kontext, desto '
                             'besser die Verknüpfung — und desto besser die Antwort.',
                       'en': '## The Transformer & Attention (in brief)\n'
                             '\n'
                             'Modern LLMs are built on the **Transformer** architecture (2017). '
                             'Its core is the **attention mechanism**: while processing, each '
                             'token can "look" at *all other* tokens in the context and weigh '
                             'which ones are currently relevant. This is how the model captures '
                             'relationships across long distances — for example, that a `return` '
                             'far below refers back to a function signature far above.\n'
                             '\n'
                             'For this workshop, this intuition is enough: **attention = the model '
                             'links context.** The clearer and more relevant the context, the '
                             'better the linking — and the better the answer.'}},
            {'type': 'text',
             'value': {'de': '## Tokenisierung: Text wird zu Zahlen\n'
                             '\n'
                             'Modelle sehen keinen Text, sondern **Tokens** — kurze Zeichenketten, '
                             'oft Wortteile. Ein Tokenizer zerlegt Eingaben in diese Bausteine und '
                             'bildet sie auf Zahlen ab.\n'
                             '\n'
                             'Faustregeln (Englisch/Code):\n'
                             '\n'
                             '- ~4 Zeichen ≈ 1 Token, ~100 Tokens ≈ 75 Wörter.\n'
                             '- Häufige Wörter = 1 Token; seltene Wörter, IDs oder Umlaute werden '
                             'in mehrere Tokens zerlegt.\n'
                             '- Code-Symbole (`{`, `}`, `::`) sind eigene Tokens.\n'
                             '\n'
                             'Warum das zählt: **Alles kostet Tokens** — dein Prompt, die Dateien, '
                             'die Claude liest, die Tool-Ergebnisse und die Antwort. Tokens sind '
                             'die Währung von Kontextfenster *und* Kosten.',
                       'en': '## Tokenization: text becomes numbers\n'
                             '\n'
                             "Models don't see text — they see **tokens**, short character "
                             'sequences, often word fragments. A tokenizer breaks input into these '
                             'building blocks and maps them to numbers.\n'
                             '\n'
                             'Rules of thumb (English/code):\n'
                             '\n'
                             '- ~4 characters ≈ 1 token, ~100 tokens ≈ 75 words.\n'
                             '- Common words = 1 token; rare words, IDs, or special characters get '
                             'split into multiple tokens.\n'
                             '- Code symbols (`{`, `}`, `::`) are their own tokens.\n'
                             '\n'
                             'Why this matters: **everything costs tokens** — your prompt, the '
                             'files Claude reads, the tool results, and the response. Tokens are '
                             'the currency of both the context window *and* cost.'}},
            {'type': 'widget',
             'id': 'tokenizer-demo',
             'note': 'Teilnehmende einen deutschen Satz und ein Code-Snippet eingeben lassen — '
                     'sichtbar machen, dass Umlaute und Bezeichner in mehrere Tokens zerfallen.'},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Grob geschätzt: Wie viele Tokens sind ~750 Wörter Text?',
                         'prompt_en': 'Roughly estimated: how many tokens is ~750 words of text?',
                         'answer': 1,
                         'options_de': ['~100 Tokens', '~1000 Tokens', '~10.000 Tokens'],
                         'options_en': ['~100 tokens', '~1000 tokens', '~10,000 tokens']}},
            {'type': 'text',
             'value': {'de': '## Das Kontextfenster\n'
                             '\n'
                             'Das **Kontextfenster** ist die maximale Menge Tokens, die das Modell '
                             'in *einem* Durchgang berücksichtigen kann — Eingabe **und** Ausgabe '
                             'zusammen. Alles, was Claude Code gerade „im Kopf” hat, liegt darin: '
                             'System-Prompt, deine `CLAUDE.md`, der bisherige Gesprächsverlauf, '
                             'gelesene Dateien und Tool-Ergebnisse.\n'
                             '\n'
                             'Zwei Konsequenzen fürs Arbeiten mit Claude Code:\n'
                             '\n'
                             '1. **Das Fenster ist endlich.** Läuft es voll, muss Kontext '
                             'verdichtet werden — dafür gibt es später `/compact`.\n'
                             '2. **Relevanz schlägt Menge.** Zehn präzise Zeilen `CLAUDE.md` '
                             'wirken stärker als 500 Zeilen Rauschen. Deshalb kümmern wir uns in '
                             'späteren Modulen aktiv um sauberen Kontext (Memory, Subagents, '
                             '`/context`).',
                       'en': '## The context window\n'
                             '\n'
                             'The **context window** is the maximum number of tokens the model can '
                             'take into account in a *single* pass — input **and** output '
                             'combined. Everything Claude Code currently has "in mind" lives in '
                             'it: the system prompt, your `CLAUDE.md`, the conversation so far, '
                             'files it has read, and tool results.\n'
                             '\n'
                             'Two consequences for working with Claude Code:\n'
                             '\n'
                             '1. **The window is finite.** When it fills up, context has to be '
                             "condensed — that's what `/compact` is for later on.\n"
                             '2. **Relevance beats volume.** Ten precise lines of `CLAUDE.md` have '
                             "more impact than 500 lines of noise. That's why later modules "
                             'actively focus on clean context (memory, subagents, `/context`).'}},
            {'type': 'order',
             'payload': {'prompt_de': 'Bring die autoregressive Text-Erzeugung in die richtige '
                                      'Reihenfolge:',
                         'prompt_en': 'Put autoregressive text generation into the correct order:',
                         'items_de': ['Eingabetext wird in Tokens zerlegt',
                                      'Das Modell berechnet Wahrscheinlichkeiten für das nächste '
                                      'Token',
                                      'Ein Token wird ausgewählt und angehängt',
                                      'Der erweiterte Text geht erneut ins Modell — bis Stopp'],
                         'items_en': ['Input text is split into tokens',
                                      'The model calculates probabilities for the next token',
                                      'A token is selected and appended',
                                      'The extended text goes back into the model — until stop']}},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Denk an eine Aufgabe, die du zuletzt an eine KI gestellt '
                                      'hast. Welche Informationen hätte das Modell im '
                                      'Kontextfenster gebraucht, um sie wirklich gut zu lösen — '
                                      'und welche davon hast du mitgeliefert?',
                         'prompt_en': 'Think of a task you recently gave an AI. What information '
                                      'would the model have needed in the context window to solve '
                                      'it really well — and how much of that did you actually '
                                      'provide?'}},
            {'type': 'reveal',
             'payload': {'teaser_de': 'Kurzfrage zum Selbst-Prüfen: Warum liefert dasselbe Prompt '
                                      'manchmal unterschiedliche Antworten? Formuliere eine '
                                      'Erklärung in einem Satz, dann aufdecken.',
                         'teaser_en': 'Quick self-check question: Why does the same prompt '
                                      'sometimes produce different answers? Formulate an '
                                      'explanation in one sentence, then reveal the answer.'},
             'value': {'de': 'Weil die Generierung **probabilistisch** ist: Aus den '
                             'Wahrscheinlichkeiten fürs nächste Token wird per Sampling ausgewählt '
                             '(gesteuert u.a. über die *Temperatur*). Bei Temperatur 0 wird meist '
                             'das wahrscheinlichste Token genommen und die Ausgabe ist nahezu '
                             'deterministisch; höhere Temperatur bringt mehr Variation.',
                       'en': 'Because generation is **probabilistic**: the next token is chosen '
                             'via sampling from the probabilities (controlled, among other things, '
                             'by *temperature*). At temperature 0, the most probable token is '
                             'usually chosen and the output is nearly deterministic; higher '
                             'temperature brings more variation.'}}],
 'quiz': {'questions': [{'id': 'llm1',
                         'type': 'single',
                         'prompt': {'de': 'Worauf ist ein LLM grundlegend trainiert?',
                                    'en': 'What is an LLM fundamentally trained to do?'},
                         'answer': 1,
                         'options': {'de': ['Fakten in einer Datenbank nachzuschlagen',
                                            'Das nächste Token vorherzusagen',
                                            'Programme fehlerfrei zu kompilieren',
                                            'Webseiten live abzurufen'],
                                     'en': ['Look up facts in a database',
                                            'Predict the next token',
                                            'Compile programs without errors',
                                            'Fetch web pages live']}},
                        {'id': 'llm2',
                         'type': 'single',
                         'prompt': {'de': 'Was leistet der Attention-Mechanismus im Transformer?',
                                    'en': 'What does the attention mechanism in the Transformer '
                                          'do?'},
                         'answer': 1,
                         'options': {'de': ['Er komprimiert die Ausgabe',
                                            'Er verknüpft Tokens über den Kontext hinweg nach '
                                            'Relevanz',
                                            'Er übersetzt Tokens in Maschinencode',
                                            'Er speichert das Gespräch dauerhaft auf der '
                                            'Festplatte'],
                                     'en': ['It compresses the output',
                                            'It links tokens across the context by relevance',
                                            'It translates tokens into machine code',
                                            'It permanently saves the conversation to disk']}},
                        {'id': 'llm3',
                         'type': 'multi',
                         'prompt': {'de': 'Was liegt alles im Kontextfenster einer '
                                          'Claude-Code-Session? (mehrere)',
                                    'en': 'What is contained in the context window of a Claude '
                                          'Code session? (multiple)'},
                         'answer': [0, 1, 2],
                         'options': {'de': ['System-Prompt',
                                            'Geladene CLAUDE.md',
                                            'Gelesene Dateien und Tool-Ergebnisse',
                                            'Der komplette Trainingsdatensatz des Modells'],
                                     'en': ['System prompt',
                                            'Loaded CLAUDE.md',
                                            'Files read and tool results',
                                            "The model's complete training dataset"]}},
                        {'id': 'llm4',
                         'type': 'single',
                         'prompt': {'de': 'Ein Modell erfindet eine Funktion, die es nicht gibt. '
                                          'Wie heißt dieses Phänomen?',
                                    'en': "A model invents a function that doesn't exist. What is "
                                          'this phenomenon called?'},
                         'answer': 1,
                         'options': {'de': ['Kompilierung',
                                            'Halluzination',
                                            'Tokenisierung',
                                            'Attention'],
                                     'en': ['Compilation',
                                            'Hallucination',
                                            'Tokenization',
                                            'Attention']}},
                        {'id': 'llm5',
                         'type': 'number',
                         'prompt': {'de': 'Faustregel: Etwa wie viele Zeichen entsprechen grob '
                                          'einem Token bei englischem Text/Code?',
                                    'en': 'Rule of thumb: roughly how many characters correspond '
                                          'to one token for English text/code?'},
                         'answer': 4}]}}
