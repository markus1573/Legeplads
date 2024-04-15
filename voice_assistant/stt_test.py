import speech_recognition as sr
from gtts import gTTS
import pygame
import io

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="da-DK")
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def speak(text, language='da'):
    """
    Convert text to speech and play it without saving to a file.

    Parameters:
    - text (str): The text you want to convert to speech.
    - language (str): Language code (default is 'da' for Danish).
    """
    tts = gTTS(text=text, lang=language, slow=False)
    
    # Create an in-memory file-like object
    audio_stream = io.BytesIO()
    
    # Save the speech to the in-memory file-like object
    tts.write_to_fp(audio_stream)
    
    # Reset the file-like object to the beginning
    audio_stream.seek(0)

    # Initialize pygame mixer
    pygame.mixer.pre_init(44100, 16, 2, 4096*2) #frequency, size, channels, buffersize
    pygame.mixer.init()
    
    # Load and play the in-memory audio stream

    pygame.mixer.music.load(audio_stream)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    print("Audio playback complete.")


def process_command(command):
    if "hej" in command:
        speak("Hej, hvordan har du det?")
    elif "aske er sej" in command:
        # Define your custom actions here
        speak("det passer vidst ikke")
    else:
        speak("Undskyld, jeg forstod ikke hvad du sagde.")

if __name__ == "__main__":
    while True:
        user_input = listen()
        if user_input:
            process_command(user_input)

