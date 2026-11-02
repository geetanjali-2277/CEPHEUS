# CEPHEUS

CEPHEUS is a Python voice assistant that combines speech recognition, conversational AI, desktop automation, web search, music playback, and Telegram/WhatsApp messaging in one command-driven application.

## Features

- Listen for spoken commands and respond with text-to-speech.
- Chat using the Groq API.
- Open desktop applications and a built-in list of websites.
- Search the web with SerpAPI and DuckDuckGo.
- Open music searches on YouTube or control Spotify through desktop automation.
- Send messages through Telegram or WhatsApp desktop workflows.

Some features require third-party accounts, credentials, installed desktop applications, or a configured microphone and speakers. Desktop automation is designed for Windows and depends on the target application's UI.

## Requirements

- Python 3.10 or newer
- Windows
- A microphone and audio output for voice features
- Groq API key for conversational AI
- Telegram API credentials for the Telegram listener
- Optional SerpAPI key for one of the web search providers
- Telegram and/or WhatsApp desktop applications for their respective messaging workflows
- Spotify desktop application for Spotify playback

## Setup

1. Clone the repository and open a terminal in its root directory:

   ```powershell
   git clone https://github.com/geetanjali-2277/CEPHEUS.git
   cd CEPHEUS
   ```

2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install Python dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

   Speech recognition uses PyAudio to access the microphone. If its installation fails on your Python/Windows combination, install a compatible PyAudio wheel before continuing.

4. Create your private environment file from the template:

   ```powershell
   Copy-Item .env.example .env
   ```

5. Add your own credentials to `.env`:

   | Variable | Required for |
   | --- | --- |
   | `GROQ_API_KEY` | Conversational AI |
   | `TELEGRAM_API_ID` | Telegram listener |
   | `TELEGRAM_API_HASH` | Telegram listener |
   | `PHONE_NUMBER` | Telegram listener |
   | `SERPAPI_KEY` | SerpAPI search (optional; DuckDuckGo is also used) |

   Obtain Telegram API credentials from [my.telegram.org](https://my.telegram.org). Keep `.env` private; never paste credentials into source files or commit them.

6. Start the voice assistant from the repository root:

   ```powershell
   python -m backend.main
   ```

   On first use, Telethon may ask you to authenticate your Telegram account. It creates a local `.session` file; keep that file private and do not share it.

## Example commands

- “Open YouTube”
- “Play [song] on Spotify”
- “Search for [topic]”
- “Send [message] to [contact] on WhatsApp”
- “Send [message] to [contact] on Telegram”

## Privacy and ignored files

The repository ignores `.env` files (except the blank `.env.example` template), CSV and spreadsheet files, Telegram session files, local databases, generated audio, Python bytecode, and virtual environments. Personal datasets and account/session files are intentionally not part of the repository. Review `git status` before publishing and never force-add ignored private files.

## Project layout

```text
backend/   Voice assistant, integrations, and command handlers
data/      Built-in command cleanup, synonyms, and website data
```
