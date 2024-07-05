import webbrowser
from tkinter import filedialog, messagebox, simpledialog
import speech_recognition as sr
import vlc
import time
import threading
import tkinter as tk
import json

# Function to load lyrics from a text file
def load_lyrics():
    lyrics_file_path = filedialog.askopenfilename(
        title="Select Lyrics File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")),
    )
    if lyrics_file_path:
        try:
            with open(lyrics_file_path, "r") as file:
                lyrics = file.readlines()
            return lyrics
        except Exception as e:
            messagebox.showerror("Error loading file", f"Error: {e}")
    return []

# Function to detect voice input
def detect_voice(mic_device_index=None):
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=mic_device_index) as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for voice input...")

        try:
            # Listen with increased timeout to avoid WaitTimeoutError
            audio = recognizer.listen(source, timeout=5)
            print("Audio captured:", audio)  # Debug print to check if audio is captured correctly

            # Recognize speech or sound
            recognized_text = recognizer.recognize_google(audio)
            print("Recognized text:", recognized_text)  # Debug print to check recognized text

            # If successful, trigger feedback
            messagebox.showinfo("Great!", "Nice, keep it on!")
        except sr.UnknownValueError as e:
            # If no recognizable speech or sound, continue
            print("Speech recognition could not understand audio:", e)
            messagebox.showinfo("No Speech Detected", "Try again.")
        except sr.WaitTimeoutError:
            # If timeout occurs, suggest trying again
            messagebox.showinfo("Timeout", "Listening timed out, please try again.")
        except sr.RequestError as e:
            messagebox.showerror("Speech Recognition Error", f"Error: {e}")

# Class representing the Karaoke application
class KaraokeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Karaoke Machine")
        self.geometry("400x300")

        # Create a text tag for highlighting the current line
        self.lyrics_display = tk.Text(self, height=10, width=40, state=tk.DISABLED)
        self.lyrics_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.lyrics_display.tag_configure("current_line", background="yellow")

        # Load lyrics button
        self.load_lyrics_button = tk.Button(
            self, text="Load Lyrics", command=self.load_lyrics_file
        )
        self.load_lyrics_button.grid(row=1, column=0, padx=10, pady=10)

        # Play YouTube button
        self.play_youtube_button = tk.Button(
            self, text="Play YouTube Link", command=self.play_youtube_link
        )
        self.play_youtube_button.grid(row=1, column=1, padx=10, pady=10)

        # Load audio file button
        self.load_audio_button = tk.Button(
            self, text="Load Audio File", command=self.load_audio_file
        )
        self.load_audio_button.grid(row=2, column=0, padx=10, pady=10)

        # Start karaoke button
        self.start_karaoke_button = tk.Button(
            self, text="Start Karaoke", command=self.start_karaoke
        )
        self.start_karaoke_button.grid(row=2, column=1, padx=10, pady=10)

        # Save and Load state buttons
        self.save_state_button = tk.Button(
            self, text="Save State", command=self.save_state
        )
        self.save_state_button.grid(row=3, column=0, padx=10, pady=10)

        self.load_state_button = tk.Button(
            self, text="Load State", command=self.load_state
        )
        self.load_state_button.grid(row=3, column=1, padx=10, pady=10)

        # Select audio source button
        self.select_audio_button = tk.Button(
            self, text="Select Audio Source", command=self.select_audio_source
        )
        self.select_audio_button.grid(row=0, column=1, padx=10, pady=10)

        # VLC media player for audio
        self.audio_player = None
        self.audio_file = None

        # Lyrics data
        self.lyrics = []
        self.current_line = 0
        self.delay_between_lines = 2000  # milliseconds (2 seconds)
        self.karaoke_running = False

        # Specify microphone device index (default is None, meaning system's default device)
        self.mic_device_index = None  # You can set this to a specific index if needed

        # State file path
        self.state_file = "karaoke_state.json"

    def load_lyrics_file(self):
        self.lyrics = load_lyrics()
        self.current_line = 0
        self.karaoke_running = False
        self.update_lyrics_display(clear=True)

    def load_audio_file(self):
        audio_file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=(("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")),
        )
        if audio_file_path:
            self.audio_file = audio_file_path

    def select_audio_source(self):
        # Ask the user to choose an audio source
        audio_source = simpledialog.askstring("Select Audio Source", "Enter 'file' for local file or 'youtube' for YouTube link:")

        if audio_source == 'file':
            self.load_audio_file()
        elif audio_source == 'youtube':
            self.play_youtube_link()
        else:
            messagebox.showwarning("Invalid Input", "Please enter 'file' or 'youtube'.")

    def update_lyrics_display(self, clear=False):
        self.lyrics_display.configure(state=tk.NORMAL)
        if clear:
            self.lyrics_display.delete("1.0", tk.END)

        if self.lyrics and 0 <= self.current_line < len(self.lyrics):
            # Highlight the current line being sung
            current_line_text = self.lyrics[self.current_line]
            self.lyrics_display.insert(tk.END, current_line_text, "current_line")
        else:
            self.lyrics_display.insert(tk.END, "")

        self.lyrics_display.configure(state=tk.DISABLED)

    def start_karaoke(self):
        if not self.lyrics:
            return
        if not self.audio_file:
            messagebox.showwarning("Audio Not Loaded", "Please load an audio file.")
            return

        # Start the audio playback
        self.play_audio()

        self.karaoke_running = True
        self.current_line = 0
        self.show_next_line()

        # Start voice detection in a separate thread, specifying microphone device
        voice_thread = threading.Thread(target=detect_voice, args=(self.mic_device_index,), daemon=True)
        voice_thread.start()

    def show_next_line(self):
        if not self.karaoke_running or self.current_line >= len(self.lyrics):
            return

        # Display the current line of lyrics
        self.update_lyrics_display(clear=True)

        # Schedule the next line to show after a delay
        self.current_line += 1
        self.after(self.delay_between_lines, self.show_next_line)

    def play_audio(self):
        if self.audio_player:
            self.audio_player.stop()  # Stop any ongoing playback
        if self.audio_file:
            self.audio_player = vlc.MediaPlayer(self.audio_file)
            self.audio_player.play()

    def play_youtube_link(self):
        # Ask for a YouTube link
        youtube_link = simpledialog.askstring("YouTube Link", "Enter the YouTube URL:")
        if youtube_link:
            webbrowser.open(youtube_link)

    def save_state(self):
        state = {
            "current_line": self.current_line,
            "audio_position": self.get_audio_position(),
        }
        with open(self.state_file, "w") as file:
            json.dump(state, file)

    def load_state(self):
        try:
            with open(self.state_file, "r") as file:
                state = json.load(file)
            self.current_line = state["current_line"]
            self.set_audio_position(state["audio_position"])
        except FileNotFoundError:
            messagebox.showwarning("State Not Found", "No previous state found.")
        except Exception as e:
            messagebox.showerror("Error Loading State", f"Error: {e}")

    def get_audio_position(self):
        if self.audio_player:
            return self.audio_player.get_time()
        return 0

    def set_audio_position(self, position):
        if self.audio_player:
            self.audio_player.set_time(position)

if __name__ == "__main__":
    app = KaraokeApp()
    app.mainloop()
