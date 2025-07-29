#!/bin/bash

# Verzeichnis des Skripts ermitteln
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Virtuelle Umgebung erstellen, falls sie nicht existiert
if [ ! -d ".venv" ]; then
  echo "Erstelle virtuelle Umgebung..."
  python3 -m venv .venv
fi

# Aktivieren der Umgebung
source .venv/bin/activate

# Installieren der notwendigen Pakete
echo "Installiere Python-Abhängigkeiten..."
pip install --upgrade pip
pip install yt-dlp

# Prüfen ob ffmpeg vorhanden ist
if ! command -v ffmpeg &> /dev/null; then
  echo "ffmpeg nicht gefunden. Versuche Installation mit brew..."
  if command -v brew &> /dev/null; then
    brew install ffmpeg
  else
    echo "Homebrew ist nicht installiert. Bitte installiere ffmpeg manuell: https://ffmpeg.org/download.html"
  fi
else
  echo "ffmpeg ist bereits installiert."
fi

# Starten der App
echo "Starte app.py..."
python app.py
