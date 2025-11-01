# Vidsnap-AI

A small Flask-based utility to create short vertical 'reels' from uploaded images and generated audio. The app accepts image uploads and a description, converts the description to speech via ElevenLabs, then uses FFmpeg to combine images and the generated audio into a 1080×1920 vertical video saved under `static/reels/`.

## Quick summary

- Web UI (Flask) for uploading images and a short text description.
- Text-to-speech using ElevenLabs (network/API key required).
- FFmpeg is used to concat images and audio into a vertical reel (1080×1920, 30 fps).
- A background processor watches `user_uploads/` and creates reels into `static/reels/`.

## Prerequisites

- Python 3.8+ installed
- FFmpeg installed and available on PATH (ffmpeg executable)
- An ElevenLabs API key (do NOT commit the key to source control)

Optional but recommended:
- Create a virtual environment for the project.

## Important security note

The repository currently contains a `config.py` with an ElevenLabs API key. Do not keep secrets in source files. Move the key into an environment variable and/or a proper secret manager. Example (PowerShell):

```powershell
$env:ELEVENLABS_API_KEY = "your_api_key_here"
```

Then modify `config.py` (or create a secure config loader) to read from the environment instead of hardcoding the key.

## Installation

1. Clone the repo and change into the project folder.
2. Create and activate a virtual environment:

```powershell
# Windows PowerShell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

3. Install Python dependencies:

```powershell
pip install flask elevenlabs
```

Note: There is no `requirements.txt` in the repo currently. If you'd like, create one using:

```powershell
pip freeze > requirements.txt
```

## Files and folders (important ones)

- `main.py` — Flask application; provides routes `/` (index), `/create` (upload images + description), and `/gallery`.
- `generate_process.py` — Background loop: reads `user_uploads/`, converts description to speech, runs FFmpeg to create `static/reels/<id>.mp4`, and appends processed folders to `done.txt`.
- `text_to_audio.py` — Uses the ElevenLabs client to generate an `audio.mp3` file from the description and save it under the upload folder.
- `config.py` — Stores configuration (currently contains an ElevenLabs key; move this to environment variables).
- `user_uploads/` — Per-upload folders are created here. Each folder contains the uploaded images, `desc.txt` (the description), and `input.txt` (FFmpeg concat file listing and durations).
- `static/reels/` — Generated MP4 reels are written here by `generate_process.py`.
- `templates/` and `static/` — Flask templates and static assets for the web UI.

## How it works (high-level)

1. The Flask UI in `main.py` lets users upload images and a description. When a post happens to `/create`, files are saved under `user_uploads/<uuid>/` and `input.txt` and `desc.txt` are generated.
2. `generate_process.py` periodically scans `user_uploads/` for new folders. For each new folder it:
   - Calls `text_to_audio()` to generate `audio.mp3` (via `text_to_audio.py` / ElevenLabs).
   - Runs FFmpeg to combine the images listed in `input.txt` with the generated `audio.mp3` into a vertical 1080×1920 MP4 at 30 fps and saves it to `static/reels/<folder>.mp4`.

The FFmpeg command template used by `generate_process.py` is:

```text
ffmpeg -f concat -safe 0 -i user_uploads/<folder>/input.txt -i user_uploads/<folder>/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/<folder>.mp4
```

This scales and pads images to fit a vertical 1080×1920 canvas and produces a widely compatible MP4.

## Running the app locally

1. Start the Flask web UI (for uploading):

```powershell
python main.py
```

Open http://127.0.0.1:5000/ in a browser to upload images + description.

2. In a separate terminal, start the background processor to create reels:

```powershell
python generate_process.py
```

It will poll `user_uploads/` every few seconds and write processed folder names to `done.txt`.

## Troubleshooting

- FFmpeg errors: ensure `ffmpeg` is installed and available on PATH. From PowerShell run `ffmpeg -version` to verify.
- ElevenLabs errors: ensure `ELEVENLABS_API_KEY` is set and valid; check any rate limits or model availability.
- Permissions: ensure the process has write permissions for `user_uploads/` and `static/reels/`.

## Next steps / recommendations

- Move secrets out of `config.py` and read them from environment variables.
- Add a `requirements.txt` or `pyproject.toml` to pin dependencies.
- Add a small supervisor/service file or systemd unit (or Windows scheduled task) to run `generate_process.py` persistently in production.
- Add unit tests for helper functions and a lightweight integration test to validate the FFmpeg command formatting.

## License

Choose a license for this project (e.g., MIT). Add a `LICENSE` file if you want others to reuse the code.

---

If you'd like, I can also:

- Create a `requirements.txt` with detected dependencies.
- Modify `config.py` to read the API key from an environment variable and add `.gitignore` entries to prevent committing secrets.
