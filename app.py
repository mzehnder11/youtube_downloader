import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import shutil
import threading


class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        # --- Ästhetische Anpassungen: Sanftere Farbpalette und Stil ---
        self.ACCENT_COLOR = "#00796B"
        self.BACKGROUND_COLOR = "#F0F0F0"
        self.WIDGET_BG = "#FFFFFF"
        self.TEXT_COLOR = "#333333"

        self._configure_style()
        self.root.configure(bg=self.BACKGROUND_COLOR)

        # Initialize variables (Funktionalität unverändert)
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="video")
        self.output_path = os.path.join(os.path.expanduser("~"), "Downloads")

        # Check for yt-dlp and ffmpeg availability (Funktionalität unverändert)
        self.yt_dlp_path = self._find_executable("yt-dlp")
        self.ffmpeg_path = self._find_executable("ffmpeg")

        self.yt_dlp_available = self.yt_dlp_path is not None
        self.ffmpeg_available = self.ffmpeg_path is not None

        self.create_widgets()

        # Initial die Fortschrittsanzeige ausblenden
        self._hide_progress_elements()

    def _configure_style(self):
        """Konfiguriert den ttk Style für ein natürlicheres Aussehen."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure('.', background=self.BACKGROUND_COLOR)
        style.configure('TLabel', font=("Segoe UI", 10), foreground=self.TEXT_COLOR, background=self.BACKGROUND_COLOR)
        style.configure('TEntry', fieldbackground=self.WIDGET_BG, foreground=self.TEXT_COLOR, bordercolor="#AAAAAA",
                        borderwidth=1, relief='flat')
        style.configure('TRadiobutton', background=self.BACKGROUND_COLOR, foreground=self.TEXT_COLOR,
                        font=("Segoe UI", 10))
        style.configure('Accent.TButton', background=self.ACCENT_COLOR, foreground=self.WIDGET_BG,
                        font=("Segoe UI", 10, "bold"), borderwidth=1, relief='raised')
        style.map('Accent.TButton', background=[('active', '#004D40'), ('disabled', '#B0B0B0')],
                  foreground=[('disabled', '#E0E0E0')])
        style.configure("TProgressbar", thickness=10, troughcolor="#E8E8E8", background=self.ACCENT_COLOR,
                        relief='flat')
        style.configure('Status.TLabel', font=("Segoe UI", 9, "italic"), foreground="#666666",
                        background=self.BACKGROUND_COLOR)

    def _find_executable(self, name):
        """Checks if an executable is available in the system's PATH."""
        return shutil.which(name)

    def _show_progress_elements(self):
        """Macht Progress Bar und Status Label sichtbar."""
        # Wir verwenden pack() wieder, um sie ins Layout aufzunehmen
        self.progress.pack(pady=5, padx=30)
        self.status_label.pack(pady=(5, 5))

    def _hide_progress_elements(self):
        """Blendet Progress Bar und Status Label aus."""
        # Wir verwenden pack_forget(), um sie aus dem Layout zu entfernen
        self.progress.pack_forget()
        self.status_label.pack_forget()

    def create_widgets(self):
        """Creates and arranges the GUI widgets."""

        title_label = ttk.Label(self.root, text="YouTube Downloader",
                                font=("Segoe UI", 18, "bold"),
                                style='TLabel')
        title_label.pack(pady=(25, 15))

        # --- URL Input Section ---
        url_frame = ttk.Frame(self.root, padding="15", style='TFrame')
        url_frame.pack(pady=5, padx=30, fill=tk.X)

        ttk.Label(url_frame, text="YouTube Video-Link:",
                  font=("Segoe UI", 10, "bold"),
                  style='TLabel').pack(anchor=tk.W, pady=(0, 5))

        ttk.Entry(url_frame, textvariable=self.url_var, width=60).pack(fill=tk.X, expand=True)

        # --- Format Selection Section ---
        format_frame = ttk.Frame(self.root, padding="0", style='TFrame')
        format_frame.pack(pady=10, padx=30)

        ttk.Label(format_frame, text="Zielformat:", style='TLabel').pack(side=tk.LEFT, padx=(0, 15))

        ttk.Radiobutton(format_frame, text="Video (MP4)", variable=self.format_var, value="video",
                        style='TRadiobutton').pack(side=tk.LEFT, padx=15)

        ttk.Radiobutton(format_frame, text="Audio (MP3)", variable=self.format_var, value="audio",
                        style='TRadiobutton').pack(side=tk.LEFT)

        # --- Download Button ---
        self.download_button = ttk.Button(self.root, text="Download starten",
                                          command=self.start_download_thread,
                                          style='Accent.TButton')
        self.download_button.pack(pady=20, ipadx=15, ipady=6)

        # --- Progress Bar und Status Label (Zuerst initialisieren, dann verstecken) ---
        self.progress = ttk.Progressbar(self.root, length=400, mode="determinate", style="TProgressbar")
        self.status_label = ttk.Label(self.root, text="", style="Status.TLabel")

        # Warnings for missing tools (Funktionalität unverändert)
        if not self.yt_dlp_available:
            ttk.Label(self.root, text="Warnung: yt-dlp nicht gefunden. Download nicht möglich.",
                      foreground="#CC0000", font=("Segoe UI", 9, "bold"), background=self.BACKGROUND_COLOR).pack(
                pady=(5, 0))
            self.download_button.config(state=tk.DISABLED)

        if not self.ffmpeg_available:
            ttk.Label(self.root, text="Hinweis: ffmpeg fehlt. MP3-Konvertierung funktioniert nicht.",
                      foreground="#B8860B", font=("Segoe UI", 9, "bold"), background=self.BACKGROUND_COLOR).pack(
                pady=(5, 0))

    # --- Die folgenden Methoden sind funktional unverändert ---
    def start_download_thread(self):
        """Starts the download process in a separate thread to keep GUI responsive."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Eingabefehler", "Bitte geben Sie eine gültige YouTube-URL ein.")
            return

        # Fortschrittsanzeige einblenden, bevor der Thread startet
        self._show_progress_elements()

        self.download_button.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.status_label.config(text="Vorbereitung...")

        download_thread = threading.Thread(target=self._perform_download)
        download_thread.start()

    def _perform_download(self):
        """Performs the actual download using yt-dlp in the background thread."""
        url = self.url_var.get().strip()
        selected_format = self.format_var.get()

        try:
            os.makedirs(self.output_path, exist_ok=True)
            command = [self.yt_dlp_path, url, "--no-playlist", "-o",
                       os.path.join(self.output_path, "%(title)s.%(ext)s")]

            if selected_format == "audio":
                if not self.ffmpeg_available:
                    self.root.after(0, lambda: messagebox.showerror("Fehler",
                                                                    "ffmpeg wird für die MP3-Konvertierung benötigt, wurde aber nicht gefunden."))
                    self.root.after(0, lambda: self.status_label.config(
                        text="Download fehlgeschlagen: ffmpeg nicht gefunden."))
                    self.root.after(0, lambda: self._cleanup_after_download())
                    return

                command.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"])
            else:
                pass

            command.extend(["--no-warnings", "--progress", "--newline"])

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1,
                                       universal_newlines=True)

            for line in process.stdout:
                if "%" in line and "ETA" in line:
                    try:
                        percentage_str = line.split('%')[0].split()[-1]
                        percentage = float(percentage_str)
                        self.root.after(0, lambda p=percentage: self.progress.config(value=p))
                        self.root.after(0, lambda s=line.strip(): self.status_label.config(text=s))
                    except (ValueError, IndexError):
                        pass

            process.stdout.close()
            stderr_output = process.stderr.read()
            return_code = process.wait()

            if return_code == 0:
                self.root.after(0, lambda: self.progress.config(value=100))
                self.root.after(0, lambda: self.status_label.config(text="Download erfolgreich abgeschlossen!"))
                self.root.after(0, lambda: messagebox.showinfo("Fertig",
                                                               f"Download abgeschlossen!\nGespeichert unter: {self.output_path}"))
            else:
                error_message = f"yt-dlp Fehler (Code {return_code}):\n{stderr_output}"
                self.root.after(0, lambda: self.status_label.config(text="Download fehlgeschlagen."))
                self.root.after(0, lambda: messagebox.showerror("Download-Fehler", error_message))

        except FileNotFoundError:
            self.root.after(0, lambda: messagebox.showerror("Fehler",
                                                            "yt-dlp wurde nicht gefunden. Bitte installieren Sie es."))
            self.root.after(0, lambda: self.status_label.config(text="Download fehlgeschlagen: yt-dlp nicht gefunden."))
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text="Ein unerwarteter Fehler ist aufgetreten."))
            self.root.after(0, lambda: messagebox.showerror("Fehler",
                                                            f"Ein unerwarteter Fehler ist aufgetreten: {str(e)}"))
        finally:
            self.root.after(0, lambda: self._cleanup_after_download())

    def _cleanup_after_download(self):
        """Helper to reset GUI elements on the main thread and hide them."""
        self.download_button.config(state=tk.NORMAL)
        self.progress.config(value=0)
        # Fortschrittsanzeige wieder ausblenden
        self._hide_progress_elements()


# Main application entry point (Funktionalität unverändert)
if __name__ == "__main__":
    app = tk.Tk()
    YouTubeDownloader(app)
    app.mainloop()