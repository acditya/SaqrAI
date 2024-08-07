import pyttsx3
from faster_whisper import WhisperModel

def say(message):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160) # 160 wpm average for an interview
    engine.setProperty('volume', 1.0) # between 0.0 and 1.0
    voices = engine.getProperty('voices')       # getting details of current voice
    #engine.setProperty('voice', voices[0].id)  # 0 for male
    engine.setProperty('voice', voices[1].id)   # 1 for female

    engine.say(message)

    engine.runAndWait()
    engine.stop()

def transcribe(audio_file):
    model_size = "small.en" # tiny.en, tiny, base.en, base, small.en, small, medium.en, medium, large-v1, large-v2, large-v3, large, distil-large-v2, distil-medium.en, distil-small.en, distil-large-v3

    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_file, beam_size=5)

    text = []
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        text.append(segment.text)

    text = "".join(text)
    return text

