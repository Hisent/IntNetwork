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
 'goals_en': ['Explain how an LLM generates text (predicting the next token)',
              'Understand the role of the Transformer and attention at a high level',
              'Understand tokenization and the context window and know their limits',
              'Understand why context quality determines answer quality'],
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
 'blocks': [{'type': 'text', 'id': 'text-1',
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
                             '- Das Modell **rechnet Wahrscheinlichkeiten**, es „weiß“ nichts im '
                             'menschlichen Sinn.\n'
                             '- Gleiche Eingabe kann leicht **unterschiedliche** Ausgaben liefern '
                             '(Sampling / Temperatur).\n'
                             '- Es kann **plausibel klingenden Unsinn** erzeugen (*Halluzination*) '
                             '— deshalb verifizieren wir Ergebnisse.',
                       'en': '## What an LLM Actually Does\n'
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
                             '- The model **computes probabilities**; it doesn\'t “know” anything '
                             'in the human sense.\n'
                             '- The same input can yield slightly **different** outputs (sampling / '
                             'temperature).\n'
                             '- It can produce **plausible-sounding nonsense** (*hallucination*) — '
                             'which is why we verify results.'},
             'note': 'Live am Tokenizer zeigen, dass Umlaute/Bezeichner in mehrere Tokens '
                     'zerfallen; das Kontextfenster als endliche Ressource betonen. Die Demo ist '
                     'eine Heuristik und überzeichnet: echte Tokenizer fassen häufige Wörter '
                     'zusammen, die Tendenz (Nicht-ASCII und seltene Bezeichner kosten mehr) stimmt.'},
            {'type': 'text', 'id': 'text-2',
             'value': {'de': '## Der Transformer & Attention (in aller Kürze)\n'
                             '\n'
                             'Moderne LLMs beruhen auf der **Transformer**-Architektur (2017). Ihr '
                             'Kern ist der **Attention-Mechanismus**: Jedes Token kann beim '
                             'Verarbeiten auf *alle anderen* Tokens im Kontext „schauen“ und '
                             'gewichten, welche gerade relevant sind. So erfasst das Modell '
                             'Zusammenhänge über weite Distanzen — etwa dass sich ein `return` '
                             'weit unten auf eine Funktionssignatur weit oben bezieht.\n'
                             '\n'
                             'Für den Workshop reicht diese Intuition: **Attention = das Modell '
                             'verknüpft Kontext.** Je klarer und relevanter der Kontext, desto '
                             'besser die Verknüpfung — und desto besser die Antwort.',
                       'en': '## The Transformer & Attention (in Brief)\n'
                             '\n'
                             'Modern LLMs are built on the **Transformer** architecture (2017). '
                             'Its core is the **attention mechanism**: while processing, each '
                             'token can “look” at *all other* tokens in the context and weigh '
                             'which ones are currently relevant. This is how the model captures '
                             'relationships across long distances — for example, that a `return` '
                             'far below refers back to a function signature far above.\n'
                             '\n'
                             'For this workshop, this intuition is enough: **attention = the model '
                             'links context.** The clearer and more relevant the context, the '
                             'better the linking — and the better the answer.'}},
            {'type': 'text', 'id': 'text-3',
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
                       'en': '## Tokenization: Text Becomes Numbers\n'
                             '\n'
                             "Models don't see text — they see **tokens**, short character "
                             'sequences, often word fragments. A tokenizer breaks input into these '
                             'building blocks and maps them to numbers.\n'
                             '\n'
                             'Rules of thumb (English/code):\n'
                             '\n'
                             '- ~4 characters ≈ 1 token, ~100 tokens ≈ 75 words.\n'
                             '- Common words = 1 token; rare words, IDs, or umlauts get '
                             'split into multiple tokens.\n'
                             '- Code symbols (`{`, `}`, `::`) are their own tokens.\n'
                             '\n'
                             'Why this matters: **everything costs tokens** — your prompt, the '
                             'files Claude reads, the tool results, and the response. Tokens are '
                             'the currency of both the context window *and* cost.'}},
            {'type': 'diagram',
             'id': 'diagram-token-pipeline',
             'note': 'Schrittweise durchklicken; beim letzten Schritt auf die Schleife zeigen: jedes erzeugte '
                     'Token wird Teil der nächsten Eingabe.',
             'payload': {'kind': 'flow',
                         'title_de': 'Vom Text zum nächsten Token',
                         'title_en': 'From Text to the Next Token',
                         'caption_de': 'Eine Runde der Schleife – sie läuft für jedes einzelne Token der '
                                       'Antwort.',
                         'caption_en': 'One turn of the loop – it runs for every single token of the answer.',
                         'nodes': [{'id': 'text',
                                    'row': 0,
                                    'col': 0,
                                    'label_de': 'Eingabetext',
                                    'label_en': 'Input text'},
                                   {'id': 'tok', 'row': 1, 'col': 0, 'label': 'Tokenizer'},
                                   {'id': 'ids',
                                    'row': 1,
                                    'col': 1,
                                    'label_de': 'Token-Folge (Zahlen)',
                                    'label_en': 'Token sequence (numbers)'},
                                   {'id': 'model',
                                    'row': 1,
                                    'col': 2,
                                    'label_de': 'Transformer (Attention)',
                                    'label_en': 'Transformer (attention)'},
                                   {'id': 'probs',
                                    'row': 2,
                                    'col': 2,
                                    'label_de': 'Wahrschein-\nlichkeiten',
                                    'label_en': 'Probabilities'},
                                   {'id': 'pick',
                                    'row': 2,
                                    'col': 1,
                                    'label_de': 'Sampling: ein Token',
                                    'label_en': 'Sampling: one token'}],
                         'edges': [{'id': 'e1', 'from': 'text', 'to': 'tok'},
                                   {'id': 'e2', 'from': 'tok', 'to': 'ids'},
                                   {'id': 'e3', 'from': 'ids', 'to': 'model'},
                                   {'id': 'e4', 'from': 'model', 'to': 'probs'},
                                   {'id': 'e5', 'from': 'probs', 'to': 'pick'},
                                   {'id': 'e6',
                                    'from': 'pick',
                                    'to': 'ids',
                                    'label_de': 'anhängen',
                                    'label_en': 'append',
                                    'style': 'dashed'}],
                         'steps': [{'highlight': ['text', 'e1', 'tok', 'e2', 'ids'],
                                    'text_de': 'Der Tokenizer zerlegt den Text in Tokens und bildet sie auf '
                                               'Zahlen ab. Das Modell sieht nur diese Zahlenfolge.',
                                    'text_en': 'The tokenizer splits the text into tokens and maps them to '
                                               'numbers. The model only ever sees this sequence of numbers.'},
                                   {'highlight': ['ids', 'e3', 'model'],
                                    'text_de': 'Der Transformer verarbeitet die ganze Folge; über Attention '
                                               'gewichtet er, welche Tokens füreinander relevant sind.',
                                    'text_en': 'The Transformer processes the whole sequence; through '
                                               'attention it weighs which tokens are relevant to each other.'},
                                   {'highlight': ['model', 'e4', 'probs'],
                                    'text_de': 'Ergebnis ist kein Text, sondern eine Wahrscheinlichkeit für '
                                               'jedes mögliche nächste Token.',
                                    'text_en': 'The result is not text but a probability for every possible '
                                               'next token.'},
                                   {'highlight': ['probs', 'e5', 'pick'],
                                    'text_de': 'Per Sampling wird genau ein Token gewählt. Deshalb kann '
                                               'dieselbe Eingabe verschiedene Ausgaben liefern.',
                                    'text_en': 'Sampling picks exactly one token. That is why the same input '
                                               'can produce different outputs.'},
                                   {'highlight': ['pick', 'e6', 'ids'],
                                    'text_de': 'Das Token wird angehängt und die verlängerte Folge läuft '
                                               'erneut durch das Modell – bis ein Stopp-Signal kommt.',
                                    'text_en': 'The token is appended and the longer sequence runs through the '
                                               'model again – until a stop signal appears.'}]}},
            {'type': 'widget',
             'id': 'tokenizer-demo',
             'note': 'Teilnehmende einen deutschen Satz und ein Code-Snippet eingeben lassen — '
                     'sichtbar machen, dass Umlaute und Bezeichner in mehrere Tokens zerfallen. '
                     'Vergleich „Größe“ gegen „Größe“ zeigen; dazusagen, dass die Demo eine '
                     'Heuristik ist und keine exakten Token-Zahlen eines echten Modells liefert.'},
            {'type': 'check', 'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Grob geschätzt: Wie viele Tokens sind ~750 Wörter Text?',
                         'prompt_en': 'As a rough estimate: how many tokens are ~750 words of text?',
                         'answer': 1,
                         'options_de': ['~100 Tokens', '~1000 Tokens', '~10.000 Tokens'],
                         'options_en': ['~100 tokens', '~1000 tokens', '~10,000 tokens']}},
            {'type': 'text', 'id': 'text-4',
             'value': {'de': '## Das Kontextfenster\n'
                             '\n'
                             'Das **Kontextfenster** ist die maximale Menge Tokens, die das Modell '
                             'in *einem* Durchgang berücksichtigen kann — Eingabe **und** Ausgabe '
                             'zusammen. Alles, was Claude Code gerade „im Kopf“ hat, liegt darin: '
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
                       'en': '## The Context Window\n'
                             '\n'
                             'The **context window** is the maximum number of tokens the model can '
                             'take into account in a *single* pass — input **and** output '
                             'combined. Everything Claude Code currently has “in mind” lives in '
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
            {'type': 'match',
             'id': 'match-llm-begriffe',
             'payload': {'prompt_de': 'Ordne jedem Begriff zu, was er beschreibt.',
                         'prompt_en': 'Match each term to what it describes.',
                         'pairs': [{'left': 'Token',
                                    'right_de': 'Textbaustein, oft ein Wortteil, in dem das Modell rechnet',
                                    'right_en': 'Unit of text, often part of a word, that the model works with'},
                                   {'left_de': 'Kontextfenster',
                                    'left_en': 'Context window',
                                    'right_de': 'Obergrenze an Tokens, die das Modell auf einmal '
                                                'berücksichtigt',
                                    'right_en': 'Maximum number of tokens the model takes into account at once'},
                                   {'left': 'Attention',
                                    'right_de': 'Mechanismus, der Tokens nach Relevanz miteinander verknüpft',
                                    'right_en': 'Mechanism that links tokens to each other by relevance'},
                                   {'left': 'Sampling',
                                    'right_de': 'Auswahl eines Tokens aus der berechneten Verteilung',
                                    'right_en': 'Choosing one token from the computed distribution'},
                                   {'left_de': 'Halluzination',
                                    'left_en': 'Hallucination',
                                    'right_de': 'Plausibel klingende Ausgabe, die sachlich nicht stimmt',
                                    'right_en': 'Plausible-sounding output that is factually wrong'}],
                         'explanation_de': 'Alle fünf Begriffe hängen an derselben Schleife: Tokens füllen das '
                                           'Kontextfenster, Attention verknüpft sie, Sampling wählt das '
                                           'nächste Token – und weil nur Wahrscheinlichkeiten gerechnet '
                                           'werden, kann das Ergebnis falsch sein.',
                         'explanation_en': 'All five terms belong to the same loop: tokens fill the context '
                                           'window, attention links them, sampling picks the next token – and '
                                           'because only probabilities are computed, the result can be wrong.'}},
            {'type': 'order', 'id': 'order-1',
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
                                      'The extended text goes back into the model — until it stops']}},
            {'type': 'reflect', 'id': 'reflect-1',
             'payload': {'prompt_de': 'Denk an eine Aufgabe, die du zuletzt an eine KI gestellt '
                                      'hast. Welche Informationen hätte das Modell im '
                                      'Kontextfenster gebraucht, um sie wirklich gut zu lösen — '
                                      'und welche davon hast du mitgeliefert?',
                         'prompt_en': 'Think of a task you recently gave an AI. What information '
                                      'would the model have needed in the context window to solve '
                                      'it really well — and how much of that did you actually '
                                      'provide?'}},
            {'type': 'reveal', 'id': 'reveal-1',
             'payload': {'teaser_de': 'Kurzfrage zum Selbst-Prüfen: Warum liefert derselbe Prompt '
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
                         'explanation': {'de': 'Ein LLM lernt im Training genau eine Aufgabe: aus dem bisherigen Text das nächste Token vorherzusagen. Der naheliegende Irrtum ist das Bild vom Nachschlagewerk – das Modell schlägt nichts in einer Datenbank nach, sondern rechnet Wahrscheinlichkeiten, und kann deshalb auch Falsches flüssig formulieren.', 'en': 'During training an LLM learns exactly one task: predicting the next token from the text so far. The obvious misconception is the image of a reference work – the model does not look anything up in a database, it computes probabilities, and can therefore also state wrong things fluently.'},
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
                         'explanation': {'de': 'Attention gewichtet für jedes Token, welche anderen Tokens im Kontext gerade relevant sind – so entstehen Bezüge über weite Distanzen. Mit Speichern hat das nichts zu tun: Was nicht im Kontextfenster steht, kann Attention auch nicht verknüpfen.', 'en': 'For each token, attention weighs which other tokens in the context are relevant right now – that is how long-distance relationships are captured. It has nothing to do with storage: what is not in the context window cannot be linked by attention.'},
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
                         'explanation': {'de': 'Im Kontextfenster liegt nur, was in dieser Session hineingegeben wurde: System-Prompt, geladene CLAUDE.md, Verlauf, gelesene Dateien und Tool-Ergebnisse. Die Trainingsdaten stecken dagegen in den Gewichten des Modells – sie liegen nicht als Text im Fenster und lassen sich dort auch nicht nachlesen.', 'en': "The context window holds only what was put in during this session: system prompt, loaded CLAUDE.md, history, files read and tool results. The training data, by contrast, is baked into the model's weights – it is not present as text in the window and cannot be read back from there."},
                         'type': 'multi',
                         'prompt': {'de': 'Was liegt alles im Kontextfenster einer '
                                          'Claude-Code-Session?',
                                    'en': 'What is contained in the context window of a Claude '
                                          'Code session?'},
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
                         'explanation': {'de': 'Halluzination heißt: Das Modell erzeugt eine plausibel klingende, aber falsche Ausgabe – hier eine Funktion, die es nicht gibt. Das ist kein Tokenisierungs- oder Attention-Fehler, sondern Folge der Wahrscheinlichkeitsrechnung; deshalb werden Ergebnisse durch Ausführen und Tests geprüft.', 'en': 'Hallucination means the model produces plausible-sounding but wrong output – here a function that does not exist. It is not a tokenization or attention bug but a consequence of computing probabilities; that is why results are checked by running and testing them.'},
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
                         'explanation': {'de': 'Als Faustregel gelten bei englischem Text und Code etwa vier Zeichen je Token. Es ist eine Schätzung, kein fester Wert: Deutsch, Umlaute, seltene Bezeichner und Sonderzeichen brauchen meist mehr Tokens je Zeichen.', 'en': 'As a rule of thumb, English text and code come to about four characters per token. It is an estimate, not a fixed value: German, umlauts, rare identifiers and special characters usually need more tokens per character.'},
                         'type': 'number',
                         'prompt': {'de': 'Faustregel: Etwa wie viele Zeichen entsprechen grob '
                                          'einem Token bei englischem Text/Code?',
                                    'en': 'Rule of thumb: roughly how many characters correspond '
                                          'to one token for English text/code?'},
                         'answer': 4},
                        {'id': 'llm6',
                         'type': 'single',
                         'prompt': {'de': 'In einer sehr langen Session hält sich Claude nicht mehr an eine Regel, die du '
                                          'ganz am Anfang im Chat genannt hast. Was ist die plausibelste Erklärung und die '
                                          'passende Reaktion?',
                                    'en': 'In a very long session Claude no longer follows a rule you stated in chat at '
                                          'the very beginning. What is the most plausible explanation and the appropriate response?'},
                         'options': {'de': ['Das Modell wurde zwischenzeitlich neu trainiert; man kann nichts tun',
                                            'Das Kontextfenster ist endlich: Frühe Inhalte wurden verdichtet oder gehen im '
                                            'Rauschen unter – dauerhafte Regeln gehören in die CLAUDE.md',
                                            'Attention funktioniert nur für die letzten zehn Nachrichten',
                                            'Die Regel war zu kurz; längere Regeln wirken grundsätzlich stärker'],
                                     'en': ['The model was retrained in the meantime; nothing can be done',
                                            'The context window is finite: early content has been condensed or is drowned out by noise '
                                            '– durable rules belong in CLAUDE.md',
                                            'Attention only works for the last ten messages',
                                            'The rule was too short; longer rules always have more impact']},
                         'answer': 1,
                         'explanation': {'de': 'Alles, was Claude berücksichtigt, muss im Kontextfenster stehen; in langen '
                                               'Sessions wird der Verlauf verdichtet, und Details vom Anfang können dabei '
                                               'verloren gehen. Länge hilft nicht – Relevanz schlägt Menge. Regeln, die '
                                               'immer gelten sollen, stehen deshalb in der CLAUDE.md statt nur im Chat.',
                                         'en': 'Everything Claude takes into account has to be in the context window; in '
                                               'long sessions the history is condensed and details from the start can get '
                                               'lost. Length does not help – relevance beats volume. Rules that should '
                                               'always apply therefore live in CLAUDE.md rather than only in chat.'}},
                        {'id': 'llm7',
                         'type': 'multi',
                         'prompt': {'de': 'Welche Aussagen über Tokens treffen zu?',
                                    'en': 'Which statements about tokens are true?'},
                         'options': {'de': ['Auch gelesene Dateien und Tool-Ergebnisse verbrauchen Tokens im '
                                            'Kontextfenster',
                                            'Ein Token entspricht immer genau einem Wort',
                                            'Seltene Bezeichner werden meist in mehrere Tokens zerlegt',
                                            'Die Antwort des Modells zählt ebenfalls gegen das Kontextfenster'],
                                     'en': ['Files read and tool results also consume tokens in the context window',
                                            'One token always corresponds to exactly one word',
                                            'Rare identifiers are usually split into several tokens',
                                            "The model's answer also counts against the context window"]},
                         'answer': [0, 2, 3],
                         'explanation': {'de': 'Tokens sind Textbausteine, häufig Wortteile – ein langes oder seltenes '
                                               'Wort besteht aus mehreren. Der verbreitete Irrtum ist „ein Wort = ein '
                                               'Token“. Gezählt wird alles, was durch das Modell läuft: Prompt, Dateien, '
                                               'Tool-Ergebnisse und die Ausgabe.',
                                         'en': 'Tokens are pieces of text, often parts of words – a long or rare word '
                                               'consists of several. The common misconception is “one word = one token”. '
                                               'Everything that passes through the model counts: prompt, files, tool '
                                               'results and the output.'}},
                        {'id': 'llm8',
                         'type': 'single',
                         'prompt': {'de': 'Du stellst denselben Prompt zweimal und bekommst zwei unterschiedliche '
                                          'Implementierungen. Wie ordnest du das ein?',
                                    'en': 'You send the same prompt twice and get two different implementations. How do '
                                          'you interpret that?'},
                         'options': {'de': ['Eine der beiden Antworten muss halluziniert sein',
                                            'Das ist ein Fehler im Tokenizer',
                                            'Erwartbar, weil das nächste Token per Sampling gewählt wird – entscheidend '
                                            'ist, welche Variante Tests und Review besteht',
                                            'Das Kontextfenster war beim zweiten Mal voll'],
                                     'en': ['One of the two answers must be hallucinated',
                                            'It is a bug in the tokenizer',
                                            'Expected, because the next token is chosen by sampling – what matters is '
                                            'which variant passes tests and review',
                                            'The context window was full the second time']},
                         'answer': 2,
                         'explanation': {'de': 'Die Generierung ist probabilistisch: Aus der Verteilung wird ein Token '
                                               'gezogen, kleine Unterschiede setzen sich über die ganze Antwort fort. '
                                               'Unterschiedlich heißt nicht falsch – beide Varianten können korrekt sein. '
                                               'Deshalb entscheidet der Nachweis (Tests, Review), nicht die Formulierung.',
                                         'en': 'Generation is probabilistic: a token is drawn from the distribution, and '
                                               'small differences propagate through the whole answer. Different does not '
                                               'mean wrong – both variants can be correct. That is why evidence (tests, '
                                               'review) decides, not the wording.'}},
                        ]}}
