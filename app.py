import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import shutil # For checking if yt-dlp and ffmpeg are available
import threading # For running download in a separate thread

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("500x350") # Slightly increased height for better spacing
        self.root.resizable(False, False) # Fixed window size

        # Initialize variables
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="video") # Default to video download
        
        # --- ANPASSUNG HIER: Setze den Ausgabepfad auf den Downloads-Ordner ---
        # Dies funktioniert für macOS, Linux und die meisten Windows-Installationen
        self.output_path = os.path.join(os.path.expanduser("~"), "Downloads")
        # Optional: Für Windows könnte es manchmal "Download" statt "Downloads" sein,
        # oder ein anderer Pfad, je nach Spracheinstellung.
        # Eine robustere Lösung für Windows wäre:
        # import winreg
        # try:
        #     sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        #     downloads_guid = '{374DE290-123F-4565-9164-39C4925E4640}'
        #     with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
        #         self.output_path = winreg.QueryValueEx(key, downloads_guid)[0]
        # except Exception:
        #     self.output_path = os.path.join(os.path.expanduser("~"), "Downloads")
        # --------------------------------------------------------------------

        # Check for yt-dlp and ffmpeg availability
        self.yt_dlp_path = self._find_executable("yt-dlp")
        self.ffmpeg_path = self._find_executable("ffmpeg")

        self.yt_dlp_available = self.yt_dlp_path is not None
        self.ffmpeg_available = self.ffmpeg_path is not None

        self.create_widgets()

    def _find_executable(self, name):
        """
        Checks if an executable is available in the system's PATH.
        Returns the full path to the executable if found, otherwise None.
        """
        return shutil.which(name)

    def create_widgets(self):
        """Creates and arranges the GUI widgets."""
        # URL Input Section
        url_frame = ttk.Frame(self.root, padding="10")
        url_frame.pack(pady=10, fill=tk.X)
        ttk.Label(url_frame, text="YouTube URL:").pack(anchor=tk.W)
        ttk.Entry(url_frame, textvariable=self.url_var, width=60).pack(fill=tk.X, expand=True)

        # Format Selection Section
        format_frame = ttk.Frame(self.root, padding="10")
        format_frame.pack(pady=10)
        ttk.Radiobutton(format_frame, text="Video (MP4)", variable=self.format_var, value="video") \
            .pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(format_frame, text="Audio (MP3)", variable=self.format_var, value="audio") \
            .pack(side=tk.LEFT)

        # Download Button
        self.download_button = ttk.Button(self.root, text="Download", command=self.start_download_thread)
        self.download_button.pack(pady=15)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, length=400, mode="determinate")
        self.progress.pack(pady=10)

        # Status Label
        self.status_label = ttk.Label(self.root, text="", font=("Arial", 10))
        self.status_label.pack()

        # Warnings for missing tools
        if not self.yt_dlp_available:
            ttk.Label(self.root, text="Warnung: yt-dlp wurde nicht gefunden. Download ist nicht möglich.",
                      foreground="red", font=("Arial", 9, "bold")).pack(pady=5)
            ttk.Label(self.root, text="Bitte installiere yt-dlp (z.B. 'pip install yt-dlp').",
                      foreground="red", font=("Arial", 8)).pack()
            self.download_button.config(state=tk.DISABLED) # Disable button if yt-dlp is missing

        if not self.ffmpeg_available:
            ttk.Label(self.root, text="Warnung: ffmpeg wurde nicht gefunden. MP3-Konvertierung funktioniert nicht.",
                      foreground="orange", font=("Arial", 9, "bold")).pack(pady=5)
            # Note: We don't disable the button for ffmpeg, as video download might still work

    def start_download_thread(self):
        """Starts the download process in a separate thread to keep GUI responsive."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Eingabefehler", "Bitte gib eine gültige YouTube-URL ein.")
            return

        # Disable button during download
        self.download_button.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.status_label.config(text="Starte Download...")

        # Run download in a new thread
        download_thread = threading.Thread(target=self._perform_download)
        download_thread.start()

    def _perform_download(self):
        """Performs the actual download using yt-dlp in the background thread."""
        url = self.url_var.get().strip()
        selected_format = self.format_var.get()

        try:
            # Ensure the output directory exists
            os.makedirs(self.output_path, exist_ok=True)

            # Base command for yt-dlp
            # Added --no-playlist to ensure only single video is downloaded even if URL is part of a mix/playlist
            command = [self.yt_dlp_path, url, "--no-playlist", "-o", os.path.join(self.output_path, "%(title)s.%(ext)s")]

            if selected_format == "audio":
                if not self.ffmpeg_available:
                    self.root.after(0, lambda: messagebox.showerror("Fehler", "ffmpeg wird für die MP3-Konvertierung benötigt, wurde aber nicht gefunden."))
                    self.root.after(0, lambda: self.status_label.config(text="Download fehlgeschlagen: ffmpeg nicht gefunden."))
                    return

                # yt-dlp options for audio only and convert to mp3
                command.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"]) # 0 is best quality
            else: # video
                # yt-dlp will download best available video by default
                pass

            # Add progress reporting options for yt-dlp
            command.extend(["--no-warnings", "--progress", "--newline"])

            # Execute yt-dlp command
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)

            # Read stdout line by line to update progress
            for line in process.stdout:
                if "%" in line and "ETA" in line:
                    try:
                        # Example line: "[download]   0.1% of 10.00MiB at 1.23MiB/s ETA 00:08"
                        percentage_str = line.split('%')[0].split()[-1]
                        percentage = float(percentage_str)
                        self.root.after(0, lambda p=percentage: self.progress.config(value=p))
                        self.root.after(0, lambda s=line.strip(): self.status_label.config(text=s))
                    except (ValueError, IndexError):
                        pass # Ignore lines that don't match expected progress format

            # Wait for the process to finish and get return code
            process.stdout.close()
            stderr_output = process.stderr.read()
            return_code = process.wait()

            if return_code == 0:
                self.root.after(0, lambda: self.progress.config(value=100))
                self.root.after(0, lambda: self.status_label.config(text="Download abgeschlossen!"))
                self.root.after(0, lambda: messagebox.showinfo("Fertig", f"Download abgeschlossen!\nGespeichert unter: {self.output_path}"))
            else:
                error_message = f"yt-dlp Fehler (Code {return_code}):\n{stderr_output}"
                self.root.after(0, lambda: self.status_label.config(text="Download fehlgeschlagen."))
                self.root.after(0, lambda: messagebox.showerror("Download-Fehler", error_message))

        except FileNotFoundError:
            self.root.after(0, lambda: messagebox.showerror("Fehler", "yt-dlp wurde nicht gefunden. Bitte installiere es."))
            self.root.after(0, lambda: self.status_label.config(text="Download fehlgeschlagen: yt-dlp nicht gefunden."))
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text="Ein unerwarteter Fehler ist aufgetreten."))
            self.root.after(0, lambda: messagebox.showerror("Fehler", f"Ein unerwarteter Fehler ist aufgetreten: {str(e)}"))
        finally:
            # Re-enable button after download (success or failure)
            self.root.after(0, lambda: self.download_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.progress.config(value=0)) # Reset progress bar


# Main application entry point
if __name__ == "__main__":
    app = tk.Tk()
    # Apply a modern theme for ttk widgets
    style = ttk.Style()
    style.theme_use("clam") # Or "alt", "default", "vista", "xpnative" on Windows, "aqua" on macOS
    YouTubeDownloader(app)
    app.mainloop()
