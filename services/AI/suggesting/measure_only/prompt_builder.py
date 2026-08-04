import textwrap
import re
from langdetect import detect, DetectorFactory

# Set a seed value for the random number generator used by language detection algorithm.
# To ensure that the language detection results are consistent every time the code runs.
DetectorFactory.seed = 0

def detect_language(text: str) -> str:
    """
    Detects the language of a text and verify if the detected language is correct.
    """
    try:
        lang = detect(text)
    except Exception:
        lang = "en"

    # Guard: langdetect is unreliable on short technical sentences.
    # Check for strong German-specific signals before trusting a "de" result.
    german_markers = re.search(r"[äöüßÄÖÜ]|(\bnicht\b|\bwerden\b|\bkönnte\b|\bsind\b|\bkeine\b|\bfür\b|\bmit\b|\bohne\b)", text, re.IGNORECASE)

    if lang == "de" and not german_markers:
        lang = "en"  # override false positive

    return lang

def build_suggestion_prompt(text: str) -> str:

    if detect_language(text) == "de":
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

        Wichtige Regeln:
        - Stützen Sie die Maßnahme AUSSCHLIESSLICH auf Fakten, die explizit in der Feststellung genannt werden. Fügen Sie keine Zahlen, Schwellenwerte, benannten Kontrollen, Technologien oder Standards hinzu, die die Feststellung nicht erwähnt.
        - Wenn die Feststellung eine bestimmte Zahl enthält (z. B. "sechs Zeichen"), darf Ihre Maßnahme KEINE Zahl enthalten — weder dieselbe noch eine andere. Beschreiben Sie die erforderliche Änderung nur in Worten (z. B. "größere Länge", "stärkere Komplexität").
        - Prüfen Sie vor der endgültigen Antwort: (1) Kommt jedes konkrete Substantiv oder jede Zahl in meiner Maßnahme auch in der Feststellung vor? (2) Ist meine Antwort auf Deutsch? Falls eine der beiden Prüfungen fehlschlägt, korrigieren Sie die Antwort.

        Feststellung: {text}
        Maßnahme:""").strip()

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
    Measure: Restrict access using the principle of least privilege, remove public permissions, and review all cloud storage configurations.

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
    Measure: Test and validate the incident response procedures to confirm their effectiveness.

    Finding: Data classification policy exists but is not consistently applied across departments.
    Measure: Enforce consistent application of the existing data classification policy across all departments.

    Finding: Backup retention is currently set to 15 days, which may not meet business requirements.
    Wrong: Increase backup retention to at least 30 days. (invents a number)
    Correct: Review and adjust the backup retention period to meet business requirements.

    Finding: Audit logs can be modified by system administrators without oversight.
    Measure: Restrict the ability to modify audit logs and ensure changes are subject to independent oversight.

    Critical rules:
    - Base the measure ONLY on facts explicitly stated in the finding. Do not add numbers, thresholds, named controls (e.g., "immutability," "inventory management system"), technologies, or standards that the finding does not mention.
    - If the finding contains a specific number (e.g., "six characters"), your measure must NOT include any number, not the same one, not a different one. Describe the required change in words only.
    - Before writing your final answer, check silently: (1) is every specific noun or number in my measure also present in the finding? (2) is my measure in the same language as the finding? If either check fails, correct it.

    Finding: {text}
    Measure:""").strip()
