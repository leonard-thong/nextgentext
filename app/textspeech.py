from google.cloud import texttospeech
from dotenv import load_dotenv

load_dotenv()

client = texttospeech.TextToSpeechClient()

voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)


def list_voices(language_code="en-US"):
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")


def text_to_wav(voice_name, text, filename):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    with open(f"audio/{filename}.mp3", "wb") as out:
        out.write(response.audio_content)
    print(f"Saved {filename}.mp3")

# text_to_wav("en-US-Wavenet-J", "hello world", "testing")
