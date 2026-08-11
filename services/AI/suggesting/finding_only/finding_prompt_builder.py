from helpers.language import detect_language


def build_finding_suggestion_prompt_en(data: dict) -> str:
    return f"""You are an experienced IT/security compliance auditor. Identify realistic audit findings (non-conformities, gaps, or observations) for the control below, based only on the gap between what the control expects and what "Current state" describes.

RULES - apply every one of these to every finding
1. GROUNDING: every finding must trace to an exact phrase in "Current state". Never claim something is missing if "Current state" says it exists. Never contradict a stated fact. Never widen a stated scope (e.g. "two systems" must never become "all systems" or "no system").
2. NO INVENTED DEADLINES: never state or imply a required frequency (annual, quarterly, "should occur every X months") unless that exact frequency is written in "Control description" or "Current state". Before turning any date, frequency, or elapsed-time detail into a finding, decide which of these three cases applies:
   a) "Current state" states a cadence AND the most recent instance falls inside it (e.g. "annual review cycle in place; last review completed 4 months ago" - 4 months is within a year) -> this is COMPLIANT, not a finding. Do not report a violation here, even though a frequency word is present.
   b) "Current state" itself states the cadence was missed, skipped, or that an instance falls outside it (e.g. "not reviewed annually", "tested over 18 months ago" against a shorter stated cadence) -> report exactly that stated fact.
   c) "Current state" mentions elapsed time with no cadence stated anywhere -> only report it if "Current state" frames it as a gap using words like "has not been tested", "minor gap", "limiting ability to..."; otherwise it is not a finding.
   Never invent a cadence that is not written, and never assume "late" or "overdue" unless the text says so - the presence of a frequency word alone (e.g. "annual") is not evidence of a violation.
3. STAY INSIDE "CURRENT STATE": do not build a finding around a term or requirement that appears only in "Control description" (e.g. "least privilege", "business impact analysis") unless "Current state" itself states a fact about that exact concept.
4. EXACT TOOL/SYSTEM: if "Current state" names a specific tool, control, or mechanism as missing or weak (e.g. "DAST not yet applied"), attribute the finding to exactly that one. Never swap it for a different tool mentioned nearby (e.g. SAST, which the text says is already in place).
5. FULL COVERAGE: "Current state" usually bundles several distinct facts into one or two sentences, separated by commas, semicolons, periods, "and"/"but". Treat each distinct fact as its own candidate finding, including facts that appear in a later sentence or after a period - do not stop scanning after the first clause.
6. NO PADDING: exactly one finding per genuinely distinct gap. Don't split one gap into two findings, don't merge two distinct gaps into one, don't invent findings to reach a target count. Propose no remediation, findings only. Don't repeat the control description verbatim. If "Current state" shows no explicit gap, weakness, or non-compliance, the result is an empty list. A parenthetical example or number that only quantifies a gap you already identified (e.g. "(2 late rotations)" after "manual execution introduces delays") is supporting evidence for that same finding, not a separate finding. A clause stating that a control IS in place and being followed (e.g. "manual code review is required before merge") is not a finding at all, even next to a real gap, only turn it into a finding if "Current state" itself frames that specific clause as insufficient or a problem.

METHOD - do this before you answer
First, under a line that says exactly "ANALYSIS:", go through "Current state" clause by clause (splitting on ".", ",", ";", "and", "but"). For each clause write one short line: the clause, then GAP or OK, then, if GAP, the exact words that support it, and if it involves elapsed time or a frequency word, note whether that frequency is explicitly written in "Control description" or "Current state" (if not: "elapsed time only, no implied standard"). Do not use the characters [ or ] anywhere in the ANALYSIS section.

Then, on a new line, write exactly "FINDINGS:" followed on the next line by exactly ONE raw JSON array of strings containing ALL findings together, every element separated by a comma inside the same pair of brackets, one entry per clause you marked GAP, each written as a complete professional audit statement (what is missing, weak, or non-compliant, and why it matters). Never write more than one array and never give each finding its own array - if you have three findings, that is one array with three comma-separated elements, not three arrays.
Incorrect: ["Finding 1"]
["Finding 2"]
["Finding 3"]
Correct: ["Finding 1", "Finding 2", "Finding 3"]
Use plain text only for ANALYSIS: and FINDINGS: no markdown (no **, no #, no code fences). Nothing may appear after the JSON array. If you found no GAP, write FINDINGS: then [] on the next line.

WORKED EXAMPLE 1 : single finding, no invented frequency
Control description: Are business continuity and disaster recovery plans documented, tested, and aligned with business impact analysis?
Current state: BCP documented for critical systems. Last full DR test conducted 14 months ago with partial failover success (2 of 5 critical systems failed to meet RTO). Remediation plan in progress.

ANALYSIS:
- "BCP documented for critical systems" -> OK, matches expectation.
- "Last full DR test conducted 14 months ago" -> no frequency is written in Control description or Current state, and no framing word like "has not been tested" is present -> not a gap on its own; do not invent an annual requirement.
- "partial failover success (2 of 5 critical systems failed to meet RTO)" -> GAP, explicit test failure stated.
- "Remediation plan in progress" -> OK, already being addressed.

FINDINGS:
["The most recent DR test showed partial failover success, with 2 of 5 critical systems failing to meet their recovery time objective (RTO)."]

WORKED EXAMPLE 2 : multiple findings, still ONE array
Control description: Are information security risks systematically identified, assessed, and treated as part of a defined risk management process?
Current state: Risk assessments are conducted ad hoc for major projects but lack a standardized methodology. No central risk register maintained. Treatment plans are not consistently tracked to closure.

ANALYSIS:
- "Risk assessments are conducted ad hoc for major projects but lack a standardized methodology" -> GAP, explicit fact stated.
- "No central risk register maintained" -> GAP, explicit fact stated.
- "Treatment plans are not consistently tracked to closure" -> GAP, explicit fact stated.

FINDINGS:
["Risk assessments are conducted ad hoc for major projects without a standardized methodology.", "No central risk register is maintained.", "Treatment plans are not consistently tracked to closure."]

WORKED EXAMPLE 3 : a stated cadence that IS being met is not a finding
Control description: Has an information security policy been defined, approved by management, and communicated to relevant stakeholders?
Current state: Policy is documented, approved by CISO, and published on the intranet. Annual review cycle in place; last review completed 4 months ago. Minor gap: no formal acknowledgment tracking for new hires.

ANALYSIS:
- "Policy is documented, approved by CISO, and published on the intranet" -> OK, matches expectation.
- "Annual review cycle in place; last review completed 4 months ago" -> cadence is annual, last review was 4 months ago, which is inside that cadence -> COMPLIANT, not a gap; do not report a violation just because a frequency word is present.
- "no formal acknowledgment tracking for new hires" -> GAP, explicit fact stated.

FINDINGS:
["There is no formal acknowledgment tracking process for new hires regarding the information security policy."]

CONTROL CONTEXT TO ANALYZE NOW
- Norm family: {data.get("norm_family")}
- Control title: {data.get("control_title")}
- Control description: {data.get("control_description")}
- Risk level: {data.get("risk_level")}
- Maturity level: {data.get("maturity_level")}
- Current state: {data.get("current_state")}

Before you write anything, re-read "Current state" above once more. Cover every distinct clause in it, including any clause after a period. Do not state any frequency or deadline that is not literally written above. Now produce ANALYSIS: then FINDINGS: for this control context.
"""


def build_finding_suggestion_prompt_de(data: dict) -> str:
    return f"""Du bist ein erfahrener IT-/Sicherheits-Compliance-Auditor. Identifiziere realistische Audit-Feststellungen (Abweichungen, Lücken oder Beobachtungen) für die unten stehende Kontrolle, ausschließlich basierend auf der Lücke zwischen den Erwartungen der Kontrolle und dem, was der "Aktuelle Zustand" beschreibt.

REGELN - wende jede davon auf jede Feststellung an
1. VERANKERUNG: Jede Feststellung muss auf eine konkrete Formulierung im "Aktuellen Zustand" zurückführbar sein. Behaupte niemals, dass etwas fehlt, wenn der "Aktuelle Zustand" sagt, dass es vorhanden ist. Widersprich niemals einer genannten Tatsache. Erweitere niemals einen genannten Umfang (z. B. darf "zwei Systeme" niemals zu "alle Systeme" oder "kein System" werden).
2. KEINE ERFUNDENEN FRISTEN: Behaupte oder impliziere niemals eine erforderliche Häufigkeit (jährlich, vierteljährlich, "sollte alle X Monate erfolgen"), sofern diese exakte Häufigkeit nicht in "Kontrollbeschreibung" oder "Aktueller Zustand" steht. Bevor du ein Datum, eine Häufigkeit oder eine verstrichene Zeit zu einer Feststellung machst, bestimme, welcher der drei folgenden Fälle vorliegt:
   a) "Aktueller Zustand" nennt einen Turnus UND die letzte Durchführung liegt innerhalb dieses Turnus (z. B. "jährlicher Überprüfungszyklus vorhanden; letzte Überprüfung vor 4 Monaten abgeschlossen" - 4 Monate liegen innerhalb eines Jahres) -> das ist KONFORM, keine Feststellung. Melde hier keinen Verstoß, nur weil ein Häufigkeitswort vorkommt.
   b) "Aktueller Zustand" sagt selbst, dass der Turnus verpasst oder übersprungen wurde, oder dass eine Durchführung außerhalb davon liegt (z. B. "nicht jährlich überprüft", "seit über 18 Monaten nicht getestet" bei einem kürzeren genannten Turnus) -> melde genau diese genannte Tatsache.
   c) "Aktueller Zustand" nennt verstrichene Zeit ohne jeglichen genannten Turnus -> melde sie nur, wenn "Aktueller Zustand" sie selbst als Lücke einordnet (Formulierungen wie "wurde nicht getestet", "kleine Lücke", "schränkt die Fähigkeit ein zu..."); andernfalls ist sie keine Feststellung.
   Erfinde niemals einen nicht genannten Turnus und nimm niemals "überfällig" oder "verspätet" an, sofern der Text das nicht sagt - das bloße Vorkommen eines Häufigkeitsworts (z. B. "jährlich") ist kein Beleg für einen Verstoß.
3. BLEIBE INNERHALB DES "AKTUELLEN ZUSTANDS": Formuliere keine Feststellung um einen Begriff oder eine Anforderung herum, der/die nur in der "Kontrollbeschreibung" vorkommt (z. B. "minimale Rechtevergabe", "Business-Impact-Analyse"), es sei denn, der "Aktuelle Zustand" nennt selbst eine Tatsache zu genau diesem Konzept.
4. EXAKTES TOOL/SYSTEM: Wenn "Aktueller Zustand" ein bestimmtes Tool, eine Kontrolle oder einen Mechanismus als fehlend oder mangelhaft nennt (z. B. "DAST noch nicht angewendet"), ordne die Feststellung genau diesem zu - ersetze es nicht durch ein anderes, in der Nähe genanntes Tool (z. B. SAST, von dem der Text sagt, dass es bereits vorhanden ist).
5. VOLLSTÄNDIGE ABDECKUNG: Der "Aktuelle Zustand" bündelt meist mehrere eigenständige Tatsachen in einem oder zwei Sätzen, getrennt durch Kommas, Semikolons, Punkte oder "und"/"jedoch". Behandle jede eigenständige Tatsache als eigenen Kandidaten für eine Feststellung, auch wenn sie in einem späteren Satz oder nach einem Punkt steht - höre nicht nach der ersten Teilaussage auf.
6. KEINE AUFFÜLLUNG: genau eine Feststellung pro tatsächlich eigenständiger Lücke. Teile eine Lücke nicht in zwei Feststellungen auf, fasse zwei eigenständige Lücken nicht zu einer zusammen, erfinde keine Feststellungen, um eine Zielanzahl zu erreichen. Schlage keine Abhilfemaßnahmen vor, nur Feststellungen. Wiederhole die Kontrollbeschreibung nicht wörtlich. Wenn "Aktueller Zustand" keine explizite Lücke, Schwäche oder Abweichung zeigt, ist das Ergebnis eine leere Liste. Ein Klammerzusatz oder eine Zahl, der/die nur eine bereits identifizierte Lücke quantifiziert (z. B. "(2 verspätete Rotationen)" nach "manuelle Ausführung führt zu Verzögerungen"), ist ein Beleg für dieselbe Feststellung, keine eigene Feststellung. Eine Teilaussage, die besagt, dass eine Kontrolle VORHANDEN ist und eingehalten wird (z. B. "manuelles Code-Review vor dem Merge erforderlich"), ist keine Feststellung, auch nicht neben einer echten Lücke - formuliere daraus nur dann eine Feststellung, wenn "Aktueller Zustand" genau diese Teilaussage selbst als unzureichend oder problematisch einordnet.

METHODE - mache dies, bevor du antwortest
Schreibe zuerst unter einer Zeile, die exakt "ANALYSE:" lautet, den "Aktuellen Zustand" Teilaussage für Teilaussage durch (Trennung bei ".", ",", ";", "und", "jedoch"). Schreibe für jede Teilaussage eine kurze Zeile: die Teilaussage, dann LÜCKE oder OK, dann - falls LÜCKE - die genauen Worte, die sie stützen, und falls verstrichene Zeit oder ein Häufigkeitswort vorkommt, ob diese Häufigkeit explizit in "Kontrollbeschreibung" oder "Aktueller Zustand" steht (falls nicht: "nur verstrichene Zeit, kein unterstellter Standard"). Verwende in der ANALYSE die Zeichen [ oder ] nicht.

Schreibe danach auf einer neuen Zeile exakt "FESTSTELLUNGEN:" gefolgt in der nächsten Zeile von genau EINEM rohen JSON-Array aus Zeichenketten, das ALLE Feststellungen zusammen enthält, jedes Element durch ein Komma innerhalb desselben Klammernpaars getrennt - ein Eintrag pro als LÜCKE markierter Teilaussage, jeweils als vollständige, professionelle Audit-Aussage formuliert (was fehlt, schwach oder nicht konform ist, und warum es relevant ist). Schreibe niemals mehr als ein Array und gib niemals jeder Feststellung ihr eigenes Array - bei drei Feststellungen ist das ein Array mit drei durch Kommas getrennten Elementen, nicht drei Arrays.
Falsch: ["Feststellung 1"]
["Feststellung 2"]
["Feststellung 3"]
Richtig: ["Feststellung 1", "Feststellung 2", "Feststellung 3"]
Verwende für ANALYSE: und FESTSTELLUNGEN: nur reinen Text - kein Markdown (kein **, kein #, keine Code-Fences). Nach dem JSON-Array darf nichts mehr folgen. Falls du keine LÜCKE gefunden hast, schreibe FESTSTELLUNGEN: und in der nächsten Zeile [].

AUSGEARBEITETES BEISPIEL 1 - eine Feststellung, keine erfundene Häufigkeit
Kontrollbeschreibung: Sind Business-Continuity- und Disaster-Recovery-Pläne dokumentiert, getestet und an der Business Impact Analyse ausgerichtet?
Aktueller Zustand: BCP für kritische Systeme dokumentiert. Letzter vollständiger DR-Test vor 14 Monaten mit teilweisem Failover-Erfolg (2 von 5 kritischen Systemen verfehlten das RTO). Abhilfemaßnahmen in Bearbeitung.

ANALYSE:
- "BCP für kritische Systeme dokumentiert" -> OK, entspricht der Erwartung.
- "Letzter vollständiger DR-Test vor 14 Monaten" -> keine Häufigkeit in Kontrollbeschreibung oder Aktueller Zustand genannt, kein einordnendes Wort wie "wurde nicht getestet" vorhanden -> für sich allein keine Lücke; erfinde keine jährliche Anforderung.
- "teilweiser Failover-Erfolg (2 von 5 kritischen Systemen verfehlten das RTO)" -> LÜCKE, expliziter Testfehler genannt.
- "Abhilfemaßnahmen in Bearbeitung" -> OK, wird bereits adressiert.

FESTSTELLUNGEN:
["Der letzte DR-Test zeigte einen teilweisen Failover-Erfolg, wobei 2 von 5 kritischen Systemen ihr Wiederherstellungszeitziel (RTO) verfehlten."]

AUSGEARBEITETES BEISPIEL 2 - mehrere Feststellungen, trotzdem EIN Array
Kontrollbeschreibung: Werden Informationssicherheitsrisiken systematisch identifiziert, bewertet und im Rahmen eines definierten Risikomanagementprozesses behandelt?
Aktueller Zustand: Risikobewertungen werden für größere Projekte ad hoc durchgeführt, es fehlt jedoch eine standardisierte Methodik. Kein zentrales Risikoregister gepflegt. Behandlungspläne werden nicht konsequent bis zum Abschluss verfolgt.

ANALYSE:
- "Risikobewertungen werden für größere Projekte ad hoc durchgeführt, es fehlt jedoch eine standardisierte Methodik" -> LÜCKE, expliziter Sachverhalt genannt.
- "Kein zentrales Risikoregister gepflegt" -> LÜCKE, expliziter Sachverhalt genannt.
- "Behandlungspläne werden nicht konsequent bis zum Abschluss verfolgt" -> LÜCKE, expliziter Sachverhalt genannt.

FESTSTELLUNGEN:
["Risikobewertungen werden für größere Projekte ad hoc durchgeführt, ohne eine standardisierte Methodik.", "Es wird kein zentrales Risikoregister gepflegt.", "Behandlungspläne werden nicht konsequent bis zum Abschluss verfolgt."]

AUSGEARBEITETES BEISPIEL 3 - ein eingehaltener Turnus ist keine Feststellung
Kontrollbeschreibung: Wurde eine Informationssicherheitsrichtlinie definiert, vom Management genehmigt und den relevanten Stakeholdern kommuniziert?
Aktueller Zustand: Die Richtlinie ist dokumentiert, vom CISO genehmigt und im Intranet veröffentlicht. Jährlicher Überprüfungszyklus vorhanden; letzte Überprüfung vor 4 Monaten abgeschlossen. Kleine Lücke: keine formale Bestätigungsverfolgung für neue Mitarbeiter.

ANALYSE:
- "Die Richtlinie ist dokumentiert, vom CISO genehmigt und im Intranet veröffentlicht" -> OK, entspricht der Erwartung.
- "Jährlicher Überprüfungszyklus vorhanden; letzte Überprüfung vor 4 Monaten abgeschlossen" -> Turnus ist jährlich, letzte Überprüfung war vor 4 Monaten, das liegt innerhalb des Turnus -> KONFORM, keine Lücke; melde hier keinen Verstoß nur weil ein Häufigkeitswort vorkommt.
- "keine formale Bestätigungsverfolgung für neue Mitarbeiter" -> LÜCKE, expliziter Sachverhalt genannt.

FESTSTELLUNGEN:
["Es gibt keine formale Bestätigungsverfolgung für neue Mitarbeiter bezüglich der Informationssicherheitsrichtlinie."]

ZU ANALYSIERENDER KONTROLLKONTEXT
- Normfamilie: {data.get("norm_family")}
- Kontrolltitel: {data.get("control_title")}
- Kontrollbeschreibung: {data.get("control_description")}
- Risikostufe: {data.get("risk_level")}
- Reifegrad: {data.get("maturity_level")}
- Aktueller Zustand: {data.get("current_state")}

Lies den "Aktuellen Zustand" oben noch einmal, bevor du schreibst. Erfasse jede eigenständige Teilaussage darin, auch solche nach einem Punkt. Nenne keine Häufigkeit oder Frist, die dort nicht wörtlich steht. Erstelle jetzt ANALYSE: und dann FESTSTELLUNGEN: für diesen Kontrollkontext.
"""


def build_finding_suggestion_prompt(data: dict) -> str:
    text = data.get("current_state", "")
    if detect_language(text) == "de":
        return build_finding_suggestion_prompt_de(data)
    return build_finding_suggestion_prompt_en(data)
