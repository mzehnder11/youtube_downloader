# Verzeichnis des Skripts setzen
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

# Falls .venv nicht existiert → erstellen
if (!(Test-Path ".venv")) {
    Write-Host "Erstelle virtuelle Umgebung..."
    python -m venv .venv
}

# Aktivieren der Umgebung
. .\.venv\Scripts\Activate.ps1

# Pakete installieren
Write-Host "Installiere Python-Abhängigkeiten..."
pip install --upgrade pip
pip install yt-dlp

# Prüfen ob ffmpeg vorhanden ist
if (!(Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "ffmpeg nicht gefunden. Versuche Installation mit winget..."
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id=Gyan.FFmpeg --source=winget --accept-source-agreements --accept-package-agreements
    } else {
        Write-Host "winget ist nicht verfügbar. Bitte installiere ffmpeg manuell: https://ffmpeg.org/download.html"
    }
} else {
    Write-Host "ffmpeg ist bereits installiert."
}

# app.py starten
Write-Host "Starte app.py..."
python app.py
