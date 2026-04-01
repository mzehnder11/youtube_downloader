# YouTube Downloader (yt-dlp GUI)

Ein schlanker, benutzerfreundlicher YouTube Downloader mit grafischer Oberfläche (Tkinter). Das Tool nutzt das leistungsstarke `yt-dlp` Backend, um Videos herunterzuladen oder direkt in hochwertige MP3-Dateien zu konvertieren.

---

## Features

* **Einfache GUI:** Intuitive Oberfläche für die Eingabe von URLs.
* **Formatwahl:** Download als **Video (MP4)** oder reine **Audiodatei (MP3)**.
* **Live-Fortschritt:** Anzeige des aktuellen Fortschritts und der Download-Geschwindigkeit direkt im Fenster.
* **Automatisches Setup:** Inklusive Skripte zur automatischen Installation der Abhängigkeiten für Windows und macOS/Linux.
* **Intelligente Fehlerprüfung:** Überprüft automatisch, ob notwendige Tools wie `ffmpeg` vorhanden sind.

---

## Voraussetzungen

Die App benötigt folgende Komponenten:
1.  **Python 3.x**
2.  **yt-dlp** (wird durch Setup-Skript installiert)
3.  **FFmpeg** (erforderlich für die MP3-Konvertierung)

---

## Installation & Start

Du musst die Abhängigkeiten nicht manuell installieren. Nutze einfach die mitgelieferten Setup-Skripte:

### Windows
1.  Rechtsklick auf `setup.ps1`.
2.  Wähle **"Mit PowerShell ausführen"**.
    * Das Skript erstellt eine virtuelle Umgebung, installiert `yt-dlp` und versucht bei Bedarf, `ffmpeg` via winget nachzuinstallieren.

### macOS / Linux
1.  Öffne das Terminal im Projektordner.
2.  Mache das Skript ausführbar: `chmod +x setup.sh`
3.  Starte das Skript: `./setup.sh`
    * Das Skript nutzt Homebrew (falls vorhanden), um `ffmpeg` zu installieren und bereitet die Python-Umgebung vor.

---

## Benutzung

1.  Starte die App (wird nach den Setup-Skripten automatisch ausgeführt oder via `python app.py`).
2.  Kopiere einen **YouTube-Link** in das Eingabefeld.
3.  Wähle das gewünschte **Zielformat** (Video oder Audio).
4.  Klicke auf **"Download starten"**.
5.  Die Datei wird standardmäßig in deinem **Downloads-Ordner** gespeichert.

---

## Projektstruktur

* `app.py`: Die Hauptanwendung (Python/Tkinter).
* `setup.ps1`: Automatisierung für Windows-Nutzer.
* `setup.sh`: Automatisierung für Unix-basierte Systeme.
* `.venv/`: (Wird erstellt) Die isolierte Python-Umgebung für die Abhängigkeiten.

---

## Wichtige Hinweise

* **FFmpeg:** Ohne FFmpeg ist der Download von MP3-Dateien nicht möglich. Die App wird dich darauf hinweisen, falls es fehlt.
* **Rechtliches:** Bitte beachte die Urheberrechtsbestimmungen und die Nutzungsbedingungen von YouTube. Dieses Tool ist nur für den privaten Gebrauch gedacht.

---

## Fehlerbehebung

| Problem | Lösung |
| :--- | :--- |
| **"yt-dlp nicht gefunden"** | Führe das `setup` Skript erneut aus. |
| **MP3 Download schlägt fehl** | Stelle sicher, dass `ffmpeg` installiert ist. |
| **URL wird nicht erkannt** | Prüfe, ob der Link korrekt kopiert wurde. |

---
*Erstellt für die YouTube Downloader App.*