import datetime
import json
import os
import subprocess
import urllib.request
import webbrowser
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# --- CONFIGURATION ---
# Replace 'YOUR_API_KEY_HERE' with your actual Gemini API key from Google AI Studio
GEMINI_API_KEY = ""
# ---------------------


def speak(text):
    """Makes the assistant speak the given text."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def ask_gemini_without_pip(question):
    """Asks Gemini using only Python's built-in libraries."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        return "I'm sorry, you need to replace 'YOUR_API_KEY_HERE' with your real API key at the top of the script first."

    # Standard HTTPS API endpoint for the gemini-2.5-flash model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    # Keep answers brief and conversational for speech output
    prompt = f"Answer this question briefly and conversationally so it sounds good read aloud: {question}"

    # Build the required JSON payload structure
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        json_data = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(
            url, data=json_data, headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            # Extract and return the AI text response
            return result["candidates"][0]["content"]["parts"][0]["text"].strip()

    except Exception as e:
        return f"Sorry, I had trouble connecting to the network. Error: {e}"


def get_text_command():
    """Gets text input directly from the user via the terminal."""
    command = input("\nType your command here: ")
    return command.lower().strip()


def open_flexible_target(target):
    """Attempts to dynamically open a website or a system application."""
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "cmd": "cmd.exe",
        "spotify": "spotify",
        "explorer": "explorer",
    }

    if target in apps:
        speak(f"Opening {target}.")
        try:
            subprocess.Popen(apps[target])
        except Exception:
            os.system(apps[target])
        return

    domain = target.replace(" ", "")
    if (
        not domain.endswith(".com")
        and not domain.endswith(".org")
        and not domain.endswith(".net")
    ):
        domain += ".com"

    url = f"https://www.{domain}"
    speak(f"Opening {target} at {url}")
    webbrowser.open(url)


def execute_task(command):
    """Executes tasks based on the text command."""
    if command == "":
        return True

    if command.startswith("open "):
        target = command.replace("open ", "").strip()
        open_flexible_target(target)

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    elif "goodbye" in command or "exit" in command:
        speak("Goodbye! Have a great day.")
        return False

    # FALLBACK: If it's none of the above, it treats it as a general question for Gemini
    else:
        print("Thinking...")
        ai_response = ask_gemini_without_pip(command)
        speak(ai_response)

    return True


# --- Main Execution Loop ---
if __name__ == "__main__":
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        print(
            "⚠️ Reminder: Don't forget to replace 'YOUR_API_KEY_HERE' on line 14 with your actual Gemini API key!"
        )

    speak("Hello! I am ready for your orders. How can I help you today?")

    is_running = True
    while is_running:
        user_command = get_text_command()
        is_running = execute_task(user_command)