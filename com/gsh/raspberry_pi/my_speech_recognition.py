import speech_recognition as sr
r = sr.Recognizer()
# mic = sr.Microphone()
mic = sr.Microphone(device_index=0)
with mic as source:
    audio = r.listen(source)
    # print(r.recognize_ibm(audio))
    print(r.recognize_sphinx(audio,show_all=True))
