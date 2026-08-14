import textwrap

from helpers.language import detect_language


def build_measure_suggestion_prompt_de(data: dict) -> str:
    return textwrap.dedent(f"""\
        Sie sind ein professioneller Auditor. Lesen Sie eine Prüfungsfeststellung und formulieren Sie eine einzelne Korrekturmaßnahme dafür.

        Stil:
        - Geben Sie ausschließlich den Text der Korrekturmaßnahme aus — keine Überschriften, keine Erklärungen.
        - Professioneller Audit-/Berichtsstil.
        - Ein Absatz, 1–4 Sätze, Länge proportional zur Feststellung.

        Beispiele:

        Feststellung: Sicherheitsereignisse von Servern werden nicht zentral erfasst oder überwacht.
        Maßnahme: Zentrale Protokollerfassung und -überwachung mit geeigneter Alarmierung implementieren.

        Feststellung: Mehrere Benutzerkonten ehemaliger Mitarbeiter sind im Active Directory weiterhin aktiv.
        Maßnahme: Einen Prozess zur regelmäßigen Deaktivierung oder Löschung inaktiver Benutzerkonten implementieren.

        Feststellung: Die aktuelle Passwortrichtlinie erlaubt Passwörter mit nur sechs Zeichen ohne Komplexitätsanforderungen.
        Falsch: Die Passwortrichtlinie stärken, um mindestens acht Zeichen mit Komplexitätsanforderungen zu verlangen. (erfindet eine Zahl, die in der Feststellung nicht enthalten ist)
        Richtig: Die Passwortrichtlinie stärken, um eine größere Länge und Komplexität zu verlangen.

        Feststellung: Der Verlust oder Diebstahl von Wechselmedien könnte vertrauliche Kundendaten offenlegen.
        Maßnahme: Kontrollen implementieren, um den unbefugten Verlust oder die Offenlegung vertraulicher Daten auf Wechselmedien zu verhindern.

        Feststellung: Mehrere Arbeitsplatzrechner verwenden veraltete Antivirensoftware.
        Maßnahme: Die Antivirensoftware auf allen betroffenen Arbeitsplatzrechnern auf eine unterstützte und aktuelle Version aktualisieren.

        Feststellung: Verfahren zur Reaktion auf Sicherheitsvorfälle sind vorhanden, wurden jedoch nicht getestet.
        Maßnahme: Die bestehenden Verfahren zur Reaktion auf Sicherheitsvorfälle testen, um deren Wirksamkeit zu bestätigen.

        Feststellung: Eine Richtlinie zur Datenklassifizierung ist vorhanden, wird jedoch nicht einheitlich in allen Abteilungen angewendet.
        Maßnahme: Die einheitliche Anwendung der bestehenden Datenklassifizierungsrichtlinie in allen Abteilungen durchsetzen.

        Feststellung: Die Aufbewahrungsfrist für Sicherungen beträgt derzeit 15 Tage, was möglicherweise nicht den Geschäftsanforderungen entspricht.
        Falsch: Die Aufbewahrungsfrist für Sicherungen auf mindestens 30 Tage erhöhen. (erfindet eine Zahl)
        Richtig: Die Aufbewahrungsfrist für Sicherungen überprüfen und an die Geschäftsanforderungen anpassen.

        Feststellung: Audit-Protokolle können von Systemadministratoren ohne Überwachung geändert werden.
        Falsch: Die Änderung von Audit-Protokollen durch Systemadministratoren muss durch ein Überwachungssystem kontrolliert und protokolliert werden. (erfindet ein konkretes System, das in der Feststellung nicht genannt wird)
        Richtig: Die Möglichkeit für Systemadministratoren, Audit-Protokolle zu ändern, einschränken und Änderungen einer unabhängigen Überprüfung unterziehen.

        Feststellung: Nach Beendigung von Lieferantenverträgen bleiben die zugehörigen Systemzugänge weiterhin aktiv.
        Falsch: Die Aktivität aller Systemzugänge ehemaliger Lieferanten nach Vertragsende regelmäßig überprüfen und bei Bedarf deaktivieren. (schwächt die Maßnahme zu einer wiederkehrenden Überprüfung ab, obwohl die Feststellung einen bereits bestehenden, aktiven Zugang beschreibt)
        Richtig: Systemzugänge nach Beendigung von Lieferantenverträgen unverzüglich deaktivieren.

        Feststellung: Bei der letzten internen Prüfung wurden mehrere Dienstkonten mit übermäßigen Berechtigungen festgestellt. Sofortige Abhilfe erforderlich.
        Falsch: Einen periodischen Überprüfungsprozess implementieren, um übermäßige Berechtigungen künftig zu erkennen. (ersetzt die geforderte Sofortmaßnahme für den bereits identifizierten Fall durch einen wiederkehrenden Prozess)
        Richtig: Die Berechtigungen der betroffenen Dienstkonten unverzüglich auf das erforderliche Minimum reduzieren.

        Feststellung: Eine Cloud-Speicherfreigabe mit vertraulichen Dokumenten ist ohne Authentifizierung öffentlich zugänglich.
        Falsch: Ein Data-Loss-Prevention-System und ein Inventarverwaltungstool einführen, um solche Freigaben künftig zu erkennen. (erfindet konkrete Werkzeuge/Systeme, die die Feststellung nicht nennt)
        Richtig: Den öffentlichen Zugriff auf die betroffene Freigabe umgehend entfernen und Cloud-Speicherkonfigurationen entsprechend dem Prinzip der minimalen Rechtevergabe überprüfen.

        Kontrolle 3.1 hat u. a. folgende separate Feststellungen zum selben aktuellen Zustand:
        (a) "Kein formaler Prozess zur regelmäßigen Überprüfung von Zugriffsrechten." (b) "Privilegierte Konten werden nicht regelmäßig auditiert." (c) "Mehrere Dienstkonten mit übermäßigen Berechtigungen, sofortige Abhilfe erforderlich."
        Falsch (für Feststellung a): Einen formalen Überprüfungsprozess implementieren und sicherstellen, dass privilegierte Konten auditiert werden und Dienstkonten keine übermäßigen Berechtigungen haben. (vermischt Inhalte aus b und c, die in Feststellung a nicht erwähnt sind)
        Richtig (für Feststellung a): Einen formalen Prozess zur regelmäßigen Überprüfung von Zugriffsrechten implementieren.

        Wichtige Regeln:
        - Stützen Sie die Maßnahme AUSSCHLIESSLICH auf Fakten, die explizit in der Feststellung genannt werden. Fügen Sie keine Zahlen, Schwellenwerte, benannten Kontrollen, Technologien oder Standards hinzu, die die Feststellung nicht erwähnt.
        - Wenn die Feststellung eine bestimmte Zahl enthält (z. B. "sechs Zeichen"), darf Ihre Maßnahme KEINE Zahl enthalten — weder dieselbe noch eine andere. Beschreiben Sie die erforderliche Änderung nur in Worten (z. B. "größere Länge", "stärkere Komplexität").
        - Nennen Sie keine konkreten Werkzeuge, Systeme, Plattformen, Technologien oder Schulungsprogramme, es sei denn, die Feststellung selbst nennt sie. Beschreiben Sie die erforderliche Kontrolle nur allgemein.
        - Der "Aktuelle Zustand" kann mehrere Aspekte oder Probleme beschreiben, die über diese eine Feststellung hinausgehen (z. B. wenn mehrere Feststellungen denselben aktuellen Zustand teilen). Adressieren Sie AUSSCHLIESSLICH das, was in dieser Feststellung steht — übernehmen Sie keine Inhalte aus anderen Teilen des aktuellen Zustands oder aus benachbarten/verwandten Feststellungen, die hier nicht genannt sind.
        - Wenn die Feststellung Dringlichkeit signalisiert (z. B. "sofortige Abhilfe erforderlich", "kritisch", "aktive Gefährdung/Offenlegung"), muss die Maßnahme eine unmittelbare, korrigierende Handlung für den bereits identifizierten Einzelfall fordern — nicht nur einen künftigen, wiederkehrenden oder periodischen Überprüfungsprozess.
        - Prüfen Sie vor der endgültigen Antwort still: (1) Kommt jedes konkrete Substantiv, jede Zahl oder jedes benannte System in meiner Maßnahme auch in der Feststellung vor? (2) Ist meine Antwort auf Deutsch? (3) Adressiert meine Maßnahme ausschließlich diese eine Feststellung, ohne Inhalte aus anderen Feststellungen oder nicht wiederholten Details des aktuellen Zustands einzubeziehen, und spiegelt sie eine in der Feststellung genannte Dringlichkeit angemessen wider? Falls eine dieser Prüfungen fehlschlägt, korrigieren Sie die Antwort.

        ZU ANALYSIERENDER KONTROLLKONTEXT
        - Normfamilie: {data.get("norm_family")}
        - Kontrolltitel: {data.get("control_title")}
        - Kontrollbeschreibung: {data.get("control_description")}
        - Risikostufe: {data.get("risk_level")}
        - Reifegrad: {data.get("maturity_level")}
        - Aktueller Zustand: {data.get("current_state")}
        - Feststellung: {data.get("finding")}

        Maßnahme:""").strip()


def build_measure_suggestion_prompt_en(data: dict) -> str:
    return textwrap.dedent(f"""\
    You are a professional auditor. Read an audit finding and write a single remediation measure for it.

    Style:
    - Output only the remediation measure text, no headers, no explanation.
    - Professional audit/report tone.
    - One paragraph, 1–4 sentences, length proportional to the finding.

    Examples:

    Finding: Security events from servers are not centrally collected or monitored.
    Measure: Implement centralized log collection and monitoring with appropriate alerting.

    Finding: A cloud storage bucket containing confidential engineering documents is publicly accessible without authentication.
    Wrong: Implement a data loss prevention system and an asset inventory tool to detect such exposures going forward. (invents specific tools/systems not named in the finding)
    Correct: Immediately remove public access to the affected storage bucket and review cloud storage configurations against the principle of least privilege.

    Finding: Third-party suppliers with access to sensitive information are not subject to documented security assessments before onboarding.
    Measure: Implement a supplier security assessment process that includes risk evaluation, contractual security requirements, and periodic reassessments.

    Finding: The current password policy allows passwords as short as six characters without complexity requirements.
    Wrong: Strengthen the password policy to require a minimum of eight characters with complexity requirements. (invents a number not in the finding)
    Correct: Strengthen the password policy to require greater length and complexity.

    Finding: Loss or theft of removable media could expose confidential customer information.
    Measure: Implement controls to prevent unauthorized loss or exposure of confidential data stored on removable media.

    Finding: Multiple workstations are running outdated antivirus software.
    Measure: Update antivirus software on all affected workstations to a supported and current version.

    Finding: Incident response procedures exist but have not been tested.
    Wrong: Conduct a tabletop exercise to test the incident response procedures within the next quarter. (invents a timeframe not stated in the finding)
    Correct: Test and validate the incident response procedures to confirm their effectiveness.

    Finding: Data classification policy exists but is not consistently applied across departments.
    Measure: Enforce consistent application of the existing data classification policy across all departments.

    Finding: Backup retention is currently set to 15 days, which may not meet business requirements.
    Wrong: Increase backup retention to at least 30 days. (invents a number)
    Correct: Review and adjust the backup retention period to meet business requirements.

    Finding: Audit logs can be modified by system administrators without oversight.
    Measure: Restrict the ability to modify audit logs and ensure changes are subject to independent oversight.

    Finding: Several service accounts were found with excessive permissions during the last internal check. Immediate remediation required.
    Wrong: Implement a periodic review process to identify and mitigate excessive permissions going forward. (replaces the required immediate fix for an already-identified case with a recurring process)
    Correct: Immediately reduce the permissions of the affected service accounts to the minimum required level.

    Control 3.1 has, among others, the following separate findings drawn from the same shared current state:
    (a) "No formal access review process." (b) "Privileged accounts are not regularly audited." (c) "Several service accounts found with excessive permissions, immediate remediation required."
    Wrong (for finding a): Implement a formal review process and ensure privileged accounts are audited and service accounts do not have excessive permissions. (pulls in content from b and c that finding a does not mention)
    Correct (for finding a): Implement a formal process for periodically reviewing access rights.

    Critical rules:
    - Base the measure ONLY on facts explicitly stated in the finding. Do not add numbers, thresholds, named controls, technologies, or standards that the finding does not mention.
    - If the finding contains a specific number (e.g., "six characters"), your measure must NOT include any number, not the same one, not a different one. Describe the required change in words only.
    - Do not name specific tools, systems, platforms, technologies, or training programs unless the finding itself names them. Describe the required control in generic terms only.
    - The "current state" may describe issues or details beyond this one finding (for example when several findings share the same current state). Address ONLY what this finding states — do not incorporate remediation for other issues mentioned in the current state or implied by sibling/related findings that are not part of this finding.
    - If the finding signals urgency (e.g. "immediate remediation required", "critical", "active exposure/disclosure"), the measure must call for immediate, corrective action on the already-identified instance — not merely a future, recurring, or periodic review process.
    - Before writing your final answer, check silently: (1) is every specific noun, number, or named system in my measure also present in the finding? (2) is my measure in the same language as the finding? (3) does my measure address only this one finding — without pulling in content from other findings or unrepeated current-state details — and does it appropriately reflect any urgency stated in the finding? If any check fails, correct the answer.

    CONTROL CONTEXT TO ANALYZE NOW
    - Norm family: {data.get("norm_family")}
    - Control title: {data.get("control_title")}
    - Control description: {data.get("control_description")}
    - Risk level: {data.get("risk_level")}
    - Maturity level: {data.get("maturity_level")}
    - Current state: {data.get("current_state")}
    - Finding: {data.get("finding")}

    Measure:""").strip()


def build_measure_suggestion_prompt(data: dict) -> str:
    text = data.get("current_state", "")
    if detect_language(text) == "de":
        return build_measure_suggestion_prompt_de(data)
    return build_measure_suggestion_prompt_en(data)
