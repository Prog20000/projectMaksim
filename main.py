import sys

import config
import tts
from fuzzywuzzy import fuzz
import datetime
from num2t4ru import num2text
import webbrowser
import vosk
import sys
import sounddevice as sd
import queue
import json
import os
f = 0
ki = 0
print(f"{config.VA_NAME} ({config.VA_VER}) начал свою работу ...")

model = vosk.Model("model_small")
samplerate = 16000
device = 1

q = queue.Queue()

a = 0
teext = 0
aktualn = 0
cell = 0
zadacha = 0
def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def va_listen(callback):
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                callback(json.loads(rec.Result())["text"])
            # else:
            #    print(rec.PartialResult())


def va_respond(voice: str):
    global a
    a = voice
    if voice.startswith(config.VA_ALIAS):
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak("Да?")
            print(voice)
        else:
            execute_cmd(cmd['cmd'])


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str):
    global ki
    global a
    global teext
    global aktualn
    global cell
    global zadacha
    global f
    if cmd == 'help':
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "и открывать браузер"
        tts.va_speak(text)
        pass
    elif cmd == 'ctime':
        now = datetime.datetime.now()
        text = "Сейчас " + num2text(now.hour) + " " + num2text(now.minute)
        tts.va_speak(text)

    elif cmd == 'pismo':
        print(1)

    elif cmd == 'nazv':
        textt = "К сожалению наблюдалась такая проблема, что мой считыватель голоса не мог коректно определить моё имя и выдавал ошибку, это и стало причиной переименования, хотя стоит признать, что имя прометей было лучше"
        tts.va_speak(textt)

    elif cmd == 'rika' and ki == 0:
        tts.va_speak('как будет называться ваш проект?')
        ki = 1

    elif ki == 1 and cmd == "tema":
        teext = a[16:]
        tts.va_speak(teext + ' прекрасное название')
        tts.va_speak('теперь опишите продукт')
        ki += 1

    elif ki == 2 and cmd == 'aktual':
        aktualn = a[16:]
        ki += 1
        tts.va_speak(aktualn + ' отличное описание, так и запишем')
        tts.va_speak('какова ваша цель?')
    elif ki == 3 and cmd == 'cel':
        cell = a[12:]
        tts.va_speak('хорошо')
        ki += 1
    elif ki == 4 and cmd == 'glava21':
        zadacha = a[19:]
        tts.va_speak('ваш проект готов!')
        f = open(f'{teext}.txt', 'w')
        f.write(str(aktualn) + ' ' + str(cell) + ' ' + str(zadacha))
        f.close()
        os.startfile(f"{teext}.txt", "print")
        tts.va_speak('всё готово')
        ki = 0
    elif cmd == 'stop':
        textt1 = 'программа приостановленна'
        tts.va_speak(textt1)
        sys.exit()

    elif cmd == 'open_browser':
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open("http://python.org")


va_listen(va_respond)
f = open('example.txt','w')
f.write(str(aktualn) + ' ' + str(cell) + ' ' + str(zadacha))
f.close()