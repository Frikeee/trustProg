import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from tkinter import *
import re
import os
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import time
from threading import *

mainWindow = Tk()

mainWindow['bg'] = '#AFEEEE'
mainWindow.title('Trust Sound')
mainWindow.geometry('300x300')
mainWindow.resizable(width=False, height=False)

file = ''
y = []
sr = 0
S = []
fileLoad = False
finalyMass = []
DecibelMIN = 0
DecibelArr = []
DoLoading = False

def openPowerSpec():
    fig, ax = plt.subplots()
    img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max, top_db=None), y_axis='log', x_axis='time', ax=ax)
    ax.set_title('Cпектрограмма мощности')
    fig.colorbar(img, ax=ax, format="%+2.0f dB")
    ax.set_xlabel("Время")
    ax.set_ylabel("Герц")
    plt.show()

def openFile():
    global fileLoad, finalyMass, DecibelMIN, file, S, sr, y
    fileLoad = False
    finalyMass = []
    DecibelMIN = 0
    filename = askopenfilename()
    loading()
    file = os.path.basename(filename)
    print(file)
    y, sr = librosa.load(filename)
    y = abs(y)
    S = np.abs(librosa.stft(y))
    btn['state'] = 'normal'
    loading_stop()

def is_valid(newval):
    result = re.match("^\d{0,1}\.{0,1}\d{0,2}$", newval) is not None
    return result


def audioSpec():
    fig, ax = plt.subplots(nrows=1, sharex=True, sharey=True)
    librosa.display.waveshow(y, sr=sr, ax=ax)
    ax.set(title='Спектр аудиофайла')
    ax.set_xlabel("Время")
    ax.set_ylabel("Амплитуда")
    ax.label_outer()
    plt.show()

def probabFunc():
    global fileLoad, DecibelMIN, finalyMass, DecibelArr
    userProb = (float)(userProbTF.get())
    if fileLoad == False:
        Db = librosa.amplitude_to_db(S, ref=np.max, top_db=None)
        clearDB = []
        summar = 0
        for i in range(len(Db[1])):
            for z in range(len(Db)):
                summar += Db[z][i] / 1025
            clearDB.append(round(abs(summar)))
            summar = 0
        D = clearDB
        D.sort()
        DecibelMAX = np.max(D)
        DecibelMIN = np.min(D)
        renges = 0
        Gistoram = []
        iterat = 0
        DecibelArr = []
        for i in range(DecibelMAX - DecibelMIN + 1):
            DecibelArr.append(DecibelMIN + i)
        while renges <= DecibelMAX - DecibelMIN:
            for i in D:
                if DecibelMIN + renges == i:
                    iterat += 1
            Gistoram.append(iterat)
            iterat = 0
            renges += 1
        relProb = []
        for i in Gistoram:
            relProb.append(float("{0:.5f}".format(i / sum(Gistoram))))
        probab = 0
        for i in relProb:
            finalyMass.append(probab + i)
            probab = probab + i
        fileLoad = True
    for index in range(len(finalyMass)):
        if finalyMass[index] > userProb:
            textProb["text"] = "Доверительная громкость: " + str(index + DecibelMIN) + " dB"
            break
    else: messagebox.showerror(title='Некорректные данные', message='Проверьте пожалуйста введённое значение доверительной вероятности. \nФормат ввода: "x.xx" , где x - цифра.\nДиапазон значений от 0.01 до 0.99')

def decibelFunc():
    global DecibelArr, finalyMass
    fig, ax = plt.subplots()
    ax.plot(DecibelArr, finalyMass)
    ax.set(title='Доверительный спектр')
    ax.grid(color = 'black', linewidth = 0.5)
    ax.set_xlabel("Акустическая мощность, Дб")
    ax.set_ylabel("Доверительная вероятность")
    ax.label_outer()
    plt.show()

def dow():
    global DoLoading
    while DoLoading:
        textProb["text"] = "Загрузка."
        time.sleep(1)
        textProb["text"] = "Загрузка.."
        time.sleep(1)
        textProb["text"] = "Загрузка..."
        time.sleep(1)
        textProb["text"] = "Загрузка...."
        time.sleep(1)
    textProb["text"] = "Успешно загружено"

def loading():
    global DoLoading
    DoLoading = True
    Thread(target = dow).start()

def loading_stop():
    global DoLoading
    DoLoading = False

check = (mainWindow.register(is_valid), "%P")

canvas = Canvas(mainWindow, height=300, width= 300)
canvas.pack()
frame = Frame(mainWindow, bg='#ADD8E6')
frame.place(relx=0.025, rely=0.025, relheight=0.95, relwidth=0.95)
btn = Button(frame, text='Открыть файл', command=openFile)
btn.pack(anchor="nw", padx=5, pady=5)
textProb = Label(frame, text='Введите доверительную вероятность:', bg='#ADD8E6')
textProb.pack(anchor="w", padx=5)
userProbTF = Entry(frame, validatecommand=check, validate="key")
userProbTF.pack(anchor="w", padx=5)
textProb = Label(frame, bg='#ADD8E6')
textProb.pack(anchor="w", padx=5)
btn = Button(frame, text='Спектр аудиофайла', command=audioSpec)
btn.pack(anchor="w", padx=5, pady=15)
btn = Button(frame, text='Cпектрограмма мощности', command=openPowerSpec)
btn.pack(anchor="w", padx=5)
btn = Button(frame, text='Доверительный спектр', command=decibelFunc)
btn.pack(anchor="w", padx=5, pady=15)
btn = Button(frame, text='Рассчитать', command=probabFunc)
btn.pack(anchor="se", padx=5, pady=15)

mainWindow.mainloop()