# 🎙️ POLO – Next-Gen Optimal Voice Assistant

A Python voice assistant with speech recognition, spoken responses, web-based information services, entertainment commands, system automation, and Arduino serial control.

## Features

- Wake phrase: **Hello Polo**
- Speech input using `SpeechRecognition` and Google's recognition service
- Local text-to-speech using `pyttsx3`
- Wikipedia summary lookup
- YouTube search in the default browser
- News headlines through RSS feeds
- Chennai weather through Open-Meteo
- Google search in the default browser
- Random jokes and facts
- Voice-controlled number guessing game
- Windows restart command with spoken confirmation
- Arduino serial commands for light ON/OFF

> **Connectivity note:** The speech-recognition function `recognize_google()` and online information features require internet access. `pyttsx3` speech output is local. This version is not a fully offline assistant.

## Requirements

- Python 3.9 or later recommended
- Microphone and speakers
- Internet connection for online features
- Arduino board and USB cable for hardware features
- Windows is assumed for the default `COM3` port and restart command

## Setup

```bash
git clone https://github.com/Sara12-coder/Polo-Voice-Assistant.git
cd Polo-Voice-Assistant

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
python main.py
```

On Linux/macOS, activate the environment with:

```bash
source .venv/bin/activate
```

PyAudio installation can vary by operating system. Install the appropriate PyAudio wheel/package if `SpeechRecognition` cannot access the microphone.

## Arduino setup

1. Open `Arduino/light_control.ino` in the Arduino IDE.
2. Connect your board and select the correct board and port.
3. Upload the sketch.
4. Set the Python serial port if needed:

Windows PowerShell:
```powershell
$env:POLO_ARDUINO_PORT="COM3"
$env:POLO_ARDUINO_BAUD="115200"
python main.py
```

The sketch listens for newline-terminated `ON` and `OFF` commands. It uses pin 13 as a demonstration output. Adapt the circuit and code for your hardware. Do not connect mains-voltage lighting directly to an Arduino pin; use a properly rated, isolated relay module and qualified supervision.

## Voice commands

| Say | Action |
|---|---|
| Hello Polo | Activates the assistant |
| Information | Asks for a topic and retrieves a Wikipedia summary |
| Play video | Asks for a video and opens YouTube search |
| News | Reads available RSS headlines |
| Temperature / Weather | Reads Chennai weather |
| Funny / Joke | Tells a joke |
| Fact | Reads a random fact |
| Search | Opens Google search results |
| Game | Starts the number guessing game |
| Restart | Asks for confirmation before scheduling a Windows restart |
| Light on | Sends `ON` to Arduino |
| Light off | Sends `OFF` to Arduino |
| Stop / Exit | Closes Polo |

## Project structure

```text
Polo-Voice-Assistant/
├── main.py
├── YT_auto.py
├── selenium_web_driver.py
├── News.py
├── weather.py
├── search.py
├── requirements.txt
├── Arduino/
│   └── light_control.ino
├── README.md
└── .gitignore
```

## Notes

- `COM3` is only a default. Change `POLO_ARDUINO_PORT` to match your computer.
- Close the Arduino Serial Monitor before running Polo because only one program can normally own the serial port at a time.
- YouTube and Google helpers open search result pages; they do not automatically play a selected video or scrape search results.
- The Wikipedia helper uses the Wikipedia REST API rather than Selenium. The filename is retained to match the original main-program import.
- Weather coordinates are configured for Chennai.
- The restart command schedules a Windows restart after 60 seconds. Test carefully and cancel with `shutdown /a` if needed.

## Future improvements

- Add offline speech recognition.
- Add configurable locations and languages.
- Improve command matching with natural-language intent detection.
- Add more Arduino sensors and actuators.
- Add a graphical user interface and automated tests.

## Developer

**Sara R**  
B.Tech – Information Technology  
GitHub: [@Sara12-coder](https://github.com/Sara12-coder)

---

⭐ If you find this project useful, consider starring the repository.

**Polo – Making everyday interactions smarter through voice, Python, and IoT.**
