import speech_recognition as sr
import time
import requests
import os

keys = ["题", "抽", "点", "分", "同学"]

def get_trigger() -> str:
    with open("trigger.config", 'r') as f: # trigger api from IFTTT
        url = f.readline().strip()
    return url

def notify(text: str):
    requests.post(trigger, data={"text": f"{text}"})
    os.system("notify-send 'key word detected'")

def deal(r: sr.Recognizer, audio: sr.AudioData):
    try:
        text = r.recognize_google(audio, language="zh-CN")
    except sr.UnknownValueError:
        return
    if isinstance(text, str):
        filter(text)
    else:
        print(f"Error type: {repr(text)}")
    return

def filter(text: str):
    print(f"Got: {text}")
    for key in keys:
        if text.find(key) != -1:
            print(f"!! Detected: {text}")
            notify(text)
    return


trigger = get_trigger()

if __name__ == '__main__':
    notify("Course Guard Running!")

    r = sr.Recognizer()
    mic = sr.Microphone()
    stopper = r.listen_in_background(mic, deal, 5)
    time.sleep(10000)