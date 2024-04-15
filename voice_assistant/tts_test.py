from gtts import gTTS
import pygame
import io


def text_to_speech(text, language='da'):
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

if __name__ == "__main__":
    # Example usage:
    input_text = "Markus er awesome, og han er den dejligste person i verden!"
    text_to_speech(input_text)
