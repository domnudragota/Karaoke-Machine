# Karaoke Machine

## Overview

The Karaoke Machine is a Python-based application that provides a fun and interactive karaoke experience. Users can load lyrics, play audio files or YouTube links, and follow along with highlighted lyrics. The application also includes features for voice detection and saving/loading the karaoke session state.

## Features

- **Load Lyrics:** Load lyrics from a text file to display in the application.
- **Play Audio:** Play audio files (MP3, WAV, OGG) or YouTube links as background music for the karaoke session.
- **Highlighted Lyrics:** Follow along with highlighted lyrics to stay in sync with the music.
- **Voice Detection:** Detect voice input using a microphone and provide feedback.
- **Save/Load State:** Save and load the current state of the karaoke session, including the current line of lyrics and the audio playback position.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/karaoke-machine.git
   cd karaoke-machine

- **Make sure you have the following modules:**

```bash
tk
speechrecognition
python-vlc
```
2. **Usage:**
Run the Karaoke Machine:
```bash
python karaoke_machine.py
```
**Load Lyrics:**
Click the "Load Lyrics" button and select a text file containing the lyrics.

**Select Audio Source:**
- Click the "Select Audio Source" button.
- Enter 'file' to load a local audio file or 'youtube' to play a YouTube link.
- If 'file' is chosen, click the "Load Audio File" button and select an audio file.
- If 'youtube' is chosen, enter the YouTube URL when prompted.
**Start Karaoke:**
- Click the "Start Karaoke" button to begin the session.

### Follow along with the highlighted lyrics and enjoy your singing session!

**Save and Load State:**
- Click the "Save State" button to save the current state of the karaoke session.
- Click the "Load State" button to load the previously saved state.
