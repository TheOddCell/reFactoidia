#!/usr/bin/python3
# reFactoidia. Factoidia, from almost scratch.
# Because Factoidia's a mess.
#
## Imports
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import StringVar, Label, Checkbutton, Button
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import *
import requests
import json
import sys
import os
from google import genai

# AI function
file = open("api.txt", "r")
client = genai.Client(api_key=file.read())
file.close()
def ai(ask):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=ask,
    )
    return response.text

## List of apis. Expandable
apis=[# URL                                               Type and keyword      Button label
    ["https://uselessfacts.jsph.pl/api/v2/facts/random",       1,"text",       "Create new fact"           ],
    ["https://techy-api.vercel.app/api/text",                  0,"",           "Modulate the tech"         ], 
    ["https://api.chucknorris.io/jokes/random",                1,"value",      "Talk to Chuck Norris"      ],
    ["https://excuser-three.vercel.app/v1/excuse",             2,"0-excuse",   "Excuse yourself"           ],
    ["https://meowfacts.herokuapp.com/",                       3,"data-0",     "Create a cat fact"         ],
    ["https://api.kanye.rest/",                                1,"quote",      "Create a Kanye West quote" ],
    ["https://sentence.underthekey.com/language?language=eng", 2,"0-content",  "Create a random sentence"  ],
    ["",                                                       4,"",           "Everything"                ]
    ] 

## Backend functions
def grabfact(id=4, i=0):
    if apis[id][1]==0:
        return requests.get(apis[id][0]).text
    elif apis[id][1]==1:
        return json.loads(requests.get(apis[id][0]).text)[apis[id][2]]
    elif apis[id][1]==2:
        return json.loads(requests.get(apis[id][0]).text)[int(apis[id][2].split("-")[0])][apis[id][2].split("-")[1]]
    elif apis[id][1]==3:
        return json.loads(requests.get(apis[id][0]).text)[apis[id][2].split("-")[0]][int(apis[id][2].split("-")[1])]
    elif apis[id][1]==4:
        return grabfact(i)

def newfact(mode,aimode=True,goodaimode=False):
    msg=""
    out=""
    j=-1
    for i in range(100):
        j=j+1
        if j==len(apis)-1:
            j=0
        try:
            cur=grabfact(mode, j)
            msg=msg+f"\n{cur}"
            out=out+cur.split(" ")[i]+" "
        except:
            break
    if aimode:
        if goodaimode:
            msg=msg+"\n\nPreAI: "+out
            out=ai(f"Rearrange the following jumble of words to make sense. You may add or remove words, but only do so if else the sentance would not be grammaticly correct, something that the output should be. Please do not respond anything more then the modified jumble. The words are the following:    {out}")
            msg=msg+"\n\nPostGoodAI "+out
        else:
            msg=msg+"\n\nPreAI: "+out
            out=ai(f"Rearrange the following jumble of words to make sense. Do not add any new words or change anything other than punctuation. Please do not respond anything more then the modified jumble. The words are the following:    {out}")
            msg=msg+"\n\nPostAI: "+out
    else:
        msg=msg+"\n\nOutput: "+out
    return [out[:-1], msg[1:]]


## GUI stuff
root = ttk.Window()
root.style.theme_use("darkly")
frm = ttk.Frame(root, padding=0)
#root.config(font=("Arial", 25))
frm.grid()
root.title("reFactoidia")
factAreaText = StringVar(frm, "Welcome to reFactoidia!")
factArea=Label(frm, textvariable=factAreaText).grid(column=0, row=0, columnspan=6)
root.resizable(False, False)
currentmode=0

aibuttonvalue = tk.BooleanVar()
aibutton=Checkbutton(frm, text='Use AI', bootstyle="danger-square-toggle", variable=aibuttonvalue).grid(column=0, row=2, columnspan=2)
aibuttonvalue.set(True)
extrabuttonvalue = tk.BooleanVar()
extrabutton=Checkbutton(frm, text='Extras', bootstyle="warning-square-toggle", variable=extrabuttonvalue).grid(column=2, row=2, columnspan=2)
extrabuttonvalue.set(False)
baibuttonvalue = tk.BooleanVar()
baibutton=Checkbutton(frm, text='Use AI+', bootstyle="primary-square-toggle", variable=baibuttonvalue).grid(column=4, row=2, columnspan=2)
baibuttonvalue.set(True)
buttonText=StringVar(frm, apis[0][3])

def guinewfact():
    isai=aibuttonvalue.get()
    isgoodai=baibuttonvalue.get()
    isextra=extrabuttonvalue.get()
    out=newfact(currentmode, isai, isgoodai)
    factAreaText.set(out[0])
    if isextra:
        Messagebox.ok(out[1], "reFactoidia Extra Info")

def switch():
    global currentmode
    currentmode=currentmode+1
    if currentmode==len(apis):
        currentmode=0
    buttonText.set(apis[currentmode][3])

try:
    if sys.argv[1]=="--bro":
        root.wm_attributes('-transparentcolor', '#222222')
except:
    pass
Button(frm, textvariable=buttonText, command=guinewfact, bootstyle=SUCCESS).grid(column=0, row=1, columnspan=3)
Button(frm, text="Switch Modes", command=switch, bootstyle=(INFO, OUTLINE)).grid(column=3, row=1, columnspan=3)
frm.pack(fill="both", expand=True, side="left")

root.mainloop()
