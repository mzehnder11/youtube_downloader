# YouTube Downloader (yt-dlp GUI)

Ein schlanker, benutzerfreundlicher YouTube Downloader mit grafischer Oberfläche (Tkinter). Das Tool nutzt das leistungsstarke `yt-dlp` Backend, um Videos herunterzuladen oder direkt in hochwertige MP3-Dateien zu konvertieren.

---

## Features

* **Einfache GUI:** Intuitive Oberfläche für die Eingabe von URLs.
* **Formatwahl:** Download als **Video (MP4)** oder reine **Audiodatei (MP3)**.
* **Live-Fortschritt:** Anzeige des aktuellen Fortschritts und der Download-Geschwindigkeit direkt im Fenster.
* **Vollautomatisches Setup & Updates:** Die App prüft beim Start selbstständig alle Abhängigkeiten und hält `yt-dlp` automatisch auf dem neuesten Stand, um Kompatibilität mit neuen YouTube-Änderungen zu garantieren.
* **Intelligente Fehlerprüfung:** Überprüft automatisch, ob notwendige Tools vorhanden sind und gibt hilfreiche Hinweise.

---

## Voraussetzungen

Die App benötigt lediglich eine installierte Python-Version:
* **Python 3.x**

Alle weiteren Abhängigkeiten (`yt-dlp`, `ffmpeg`) werden beim ersten Start automatisch durch die `app.py` eingerichtet.

---

## Start der Anwendung

Du musst keine manuellen Installationen vornehmen. Starte einfach die Hauptdatei:

### Windows / macOS / Linux
1.  Öffne ein Terminal/PowerShell im Projektordner.
2.  Führe folgenden Befehl aus:
    ```bash
    python app.py
    ```
    *(Hinweis: Je nach Installation kann der Befehl auch `python3 app.py` lauten.)*

Das Skript prüft beim ersten Start alle Abhängigkeiten, aktualisiert `pip` und installiert `yt-dlp`. Auf Windows wird zudem versucht, `ffmpeg` via `winget` zu installieren, falls es fehlt.

---

## Benutzung

1.  Starte die App via `python app.py`.
2.  Kopiere einen **YouTube-Link** in das Eingabefeld.
3.  Wähle das gewünschte **Zielformat** (Video oder Audio).
4.  Klicke auf **"Download starten"**.
5.  Die Datei wird standardmäßig in deinem **Downloads-Ordner** gespeichert.

---

## Projektstruktur

* `app.py`: Die Hauptanwendung inklusive automatischer Dependency-Verwaltung.
* `README.md`: Diese Dokumentation.

---

## Wichtige Hinweise

* **FFmpeg:** Ohne FFmpeg ist der Download von MP3-Dateien nicht möglich. Die App versucht dies unter Windows automatisch zu installieren. Auf anderen Systemen erhältst du einen Hinweis, falls es manuell installiert werden muss.
* **Rechtliches:** Bitte beachte die Urheberrechtsbestimmungen und die Nutzungsbedingungen von YouTube. Dieses Tool ist nur für den privaten Gebrauch gedacht.

---

## Fehlerbehebung

| Problem | Lösung |
| :--- | :--- |
| **"yt-dlp nicht gefunden"** | Das Programm sollte dies automatisch beheben. Falls nicht, prüfe deine Internetverbindung. |
| **MP3 Download schlägt fehl** | Stelle sicher, dass `ffmpeg` installiert ist (wird unter Windows automatisch versucht). |
| **URL wird nicht erkannt** | Prüfe, ob der Link korrekt kopiert wurde. |

---
*Erstellt für die YouTube Downloader App.*