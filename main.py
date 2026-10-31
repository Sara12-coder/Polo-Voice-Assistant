"""
POLO - Next-Gen Optimal Voice Assistant
Reconstructed, maintainable version based on the original project code.

Note: SpeechRecognition's recognize_google() requires an internet connection.
pyttsx3 speech output is local. Online features also require internet access.
"""
import datetime
import math
import os
import random
import time
import warnings

import pyttsx3
import speech_recognition as sr

from YT_auto import music
from selenium_web_driver import inforr
from News import news
from weather import temp, des
from search import sear

try:
    import pyjokes
except ImportError:
    pyjokes = None

try:
    import randfacts
except ImportError:
    randfacts = None

try:
    import serial
except ImportError:
    serial = None


# ---------- Configuration ----------
ARDUINO_PORT = os.getenv("POLO_ARDUINO_PORT", "COM3")
ARDUINO_BAUD = int(os.getenv("POLO_ARDUINO_BAUD", "115200"))
WAKE_WORD = "hello polo"

warnings.filterwarnings("ignore", category=UserWarning)

# ---------- Speech engine ----------
engine = pyttsx3.init()
engine.setProperty("rate", 150)


def speak(text: str) -> None:
    """Speak text locally and print it for visibility."""
    text = str(text)
    print(f"Polo: {text}")
    engine.say(text)
    engine.runAndWait()


def wishme() -> str:
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Morning"
    if 12 <= hour < 16:
        return "Afternoon"
    if 16 <= hour < 19:
        return "Evening"
    return "Night"


def listen_command(retries: int = 2) -> str:
    """Capture speech and return recognized text in lowercase."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.energy_threshold = 300
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=12)
        return recognizer.recognize_google(audio).lower().strip()
    except sr.WaitTimeoutError:
        speak("I did not hear anything. Please try again.")
    except sr.UnknownValueError:
        speak("Sorry, I did not understand. Please repeat.")
    except sr.RequestError:
        speak("The speech recognition service is unavailable. Please check your internet connection.")
    except (OSError, AttributeError) as exc:
        speak(f"Microphone error: {exc}")
    return ""


def connect_arduino():
    """Connect to Arduino if available; return None if connection fails."""
    if serial is None:
        print("PySerial is not installed. Arduino features are disabled.")
        return None
    try:
        board = serial.Serial(ARDUINO_PORT, ARDUINO_BAUD, timeout=1)
        time.sleep(2)  # Allow Arduino to reset after serial connection.
        print(f"Connected to Arduino on {ARDUINO_PORT}.")
        return board
    except serial.SerialException as exc:
        print(f"Arduino connection unavailable: {exc}")
        return None


def send_arduino_command(board, command: str) -> bool:
    if board is None or not getattr(board, "is_open", False):
        speak("Arduino is not connected. Please check the USB connection.")
        return False
    try:
        board.write((command.strip().upper() + "\n").encode("utf-8"))
        board.flush()
        return True
    except (serial.SerialException, OSError) as exc:
        speak(f"Could not send the command to Arduino: {exc}")
        return False


def play_number_game():
    speak("Enter your lower limit.")
    try:
        lower = int(listen_command())
        speak("Enter your upper limit.")
        upper = int(listen_command())
        if lower >= upper:
            speak("The upper limit must be greater than the lower limit.")
            return
        secret = random.randint(lower, upper)
        max_guesses = max(1, math.ceil(math.log2(upper - lower + 1)))
        speak(f"You have {max_guesses} chances to guess the number.")
        for attempt in range(1, max_guesses + 1):
            speak("Say your guess.")
            guess_text = listen_command()
            try:
                guess = int(guess_text)
            except ValueError:
                speak("I could not understand that as a number.")
                continue
            if guess == secret:
                speak(f"Congratulations! You guessed it in {attempt} attempts.")
                return
            speak("Your guess is too small." if guess < secret else "Your guess is too high.")
        speak(f"Game over. The number was {secret}. Better luck next time!")
    except ValueError:
        speak("Please provide valid whole numbers.")


def handle_command(command: str, board) -> bool:
    """Run a command. Return False when the user asks Polo to exit."""
    text = command.lower()

    if not text:
        return True

    if "information" in text or "wikipedia" in text:
        speak("Which topic do you need information about?")
        topic = listen_command()
        if topic:
            inforr().get_info(topic)

    elif ("play" in text and ("video" in text or "youtube" in text)) or text == "play":
        speak("Which video would you like to find?")
        query = listen_command()
        if query:
            music().play(query)

    elif "news" in text:
        speak("Here are the latest available headlines.")
        for headline in news():
            print(headline)
            speak(headline)

    elif "temperature" in text or "weather" in text:
        try:
            temperature = temp()
            description = des()
            message = f"The temperature in Chennai is {temperature} degrees Celsius, with {description}."
            speak(message)
        except Exception as exc:
            speak(f"I could not retrieve the weather right now. {exc}")

    elif "funny" in text or "joke" in text:
        if pyjokes:
            joke = pyjokes.get_joke()
            speak(joke)
        else:
            speak("Please install the pyjokes package to use this feature.")

    elif "your name" in text:
        speak("My name is Polo, the Next-Gen Optimal Voice Assistant.")

    elif "fact" in text:
        if randfacts:
            speak(randfacts.getFact())
        else:
            speak("Please install the randfacts package to use this feature.")

    elif "search" in text or "google" in text:
        speak("What should I search for?")
        query = listen_command()
        if query:
            sear().get_infoo(query)
            speak(f"I opened search results for {query}.")

    elif "game" in text:
        play_number_game()

    elif "restart" in text or "reboot" in text:
        speak("Do you want to restart this computer? Say yes to confirm.")
        response = listen_command()
        if "yes" in response:
            if os.name == "nt":
                os.system("shutdown /r /t 60")
                speak("Restart scheduled in 60 seconds.")
            else:
                speak("Automatic restart is configured for Windows in this project.")
        else:
            speak("Restart cancelled.")

    elif "light off" in text or "turn off light" in text:
        if send_arduino_command(board, "OFF"):
            speak("The light-off command was sent to Arduino.")

    elif "light on" in text or "turn on light" in text:
        if send_arduino_command(board, "ON"):
            speak("The light-on command was sent to Arduino.")

    elif "how are you" in text:
        speak("I am functioning well. Thank you for asking.")

    elif "stop" in text or "exit" in text or "quit" in text or "end" in text:
        speak("It was a pleasure helping you. Goodbye!")
        return False

    else:
        speak("I do not have a command for that yet. Try saying search, news, weather, or play video.")

    return True


def main():
    board = connect_arduino()
    speak("Please say the wake-up word, Hello Polo.")
    wakeword = listen_command()

    if WAKE_WORD not in wakeword:
        speak("Wake-up word not detected. Polo is going offline.")
        if board and board.is_open:
            board.close()
        return

    speak(f"Hello! Good {wishme()}. I am Polo, here to assist you.")
    speak("How are you?")
    answer = listen_command()
    if "what about you" in answer:
        speak("I am doing well, thank you.")

    try:
        while True:
            speak("What can I do for you?")
            command = listen_command()
            if not handle_command(command, board):
                break
    except KeyboardInterrupt:
        speak("Polo is shutting down.")
    finally:
        if board and getattr(board, "is_open", False):
            board.close()


if __name__ == "__main__":
    main()
