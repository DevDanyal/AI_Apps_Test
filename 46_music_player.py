import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os

class MusicPlayer:
    def __init__(self, master):
        self.master = master
        master.title("Music Player")
        master.geometry("400x200")
        master.resizable(False, False)

        pygame.mixer.init()

        self.current_song = ""
        self.paused = False

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=20)

        self.play_button = tk.Button(button_frame, text="Play", command=self.play_music)
        self.play_button.grid(row=0, column=0, padx=10)

        self.pause_button = tk.Button(button_frame, text="Pause", command=self.pause_music)
        self.pause_button.grid(row=0, column=1, padx=10)

        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_music)
        self.stop_button.grid(row=0, column=2, padx=10)

        self.open_button = tk.Button(self.master, text="Open File", command=self.open_file)
        self.open_button.pack(pady=10)

        self.song_label = tk.Label(self.master, text="No song loaded", wraplength=350)
        self.song_label.pack(pady=10)

    def open_file(self):
        self.current_song = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select Music File",
            filetypes=(("MP3 files", "*.mp3"), ("WAV files", "*.wav"), ("All files", "*.*"))
        )
        if self.current_song:
            self.song_label.config(text=f"Playing: {os.path.basename(self.current_song)}")
            self.stop_music()  # Stop any current music before loading a new one
            pygame.mixer.music.load(self.current_song)
        else:
            self.song_label.config(text="No song loaded")

    def play_music(self):
        if self.current_song:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            else:
                pygame.mixer.music.play()
        else:
            messagebox.showwarning("No Song", "Please select a song first.")

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True
        else:
            messagebox.showwarning("No Song Playing", "No song is currently playing to pause.")

    def stop_music(self):
        pygame.mixer.music.stop()
        self.paused = False
        self.song_label.config(text=f"Stopped: {os.path.basename(self.current_song)}" if self.current_song else "No song loaded")


if __name__ == "__main__":
    root = tk.Tk()
    player = MusicPlayer(root)
    root.mainloop()
