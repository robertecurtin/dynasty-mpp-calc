from Tkinter import *
from ttk import *
import team
import tkMessageBox
import winsound, sys
import threading

global choices

class gits(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            winsound.PlaySound('iu.wav', winsound.SND_FILENAME)
g = gits()
g.start()

#winsound.PlaySound, ['iu.wav', winsound.SND_FILENAME]

owners = open('owners.txt', 'rb')
namelist = [owner.rstrip() for owner in owners]
owners.close()

global teams
teams = {}

for name in namelist:
    teams[name] = team.Team(name)

selected = []

def getOptions():
    choices = [""]
    choices += [choice for choice in namelist if choice not in selected]
    return sorted(choices)

choices = getOptions()

def update(owner, index):
    old = oldselects[index]
    if old != "":selected.remove(old)
    oldselects[index]=owner
    if owner == "":
        scores[index].set("")
        mpps[index].set("")
    else:
        selected.append(owner)
        scores[index].set(teams[owner].score)
        mpps[index].set(teams[owner].mpp)
    choices = getOptions()
    for idx, opp in enumerate(opponents):
        if stringvars[idx].get() != "":
            menu = [""] + choices
            opponents[idx].set_menu(*menu)
        else:
            opponents[idx].set_menu(*choices)

def getOutput(*args):
    global teams
    left = ""
    right = ""
    if '' in [op.get() for op in stringvars]:
        tkMessageBox.showwarning(title="NOW YOU FUCKED UP", message="Team entry is unfinished.")
        return
    for idx,opp in enumerate(stringvars):
        owner = opp.get()
        tm = teams[owner]
        i = idx - 1 if idx % 2 else idx + 1
        s1 = teams[owner].score
        o2 = stringvars[i].get()
        s2 = teams[o2].score
        if s1 > s2:
            teams[owner].win()
            teams[o2].lose()
        teams[owner].cry()
        teams[o2].cry()
        tm = teams[owner]
    teamvals = sorted(teams.values(), key=lambda x:float(x.salt), reverse=True)
    #espn
    for idx,tm in enumerate(teamvals):
        if idx == 0 or idx == 1:
            left += '[b]{}. {}[/b]: ({}-{}) * {} = [b]{}[/b] salty tears'\
                  .format(idx+1,tm.owner,tm.mpp,tm.score,\
                          tm.result,tm.salt)
        else:
            left += '{}. {}: ({}-{}) * {} = {} salty tears'\
                  .format(idx+1,tm.owner,tm.mpp,tm.score,\
                          tm.result,tm.salt)
        left += '\n'

        #fb    
        right += '{}. {}: ({}-{}) * {} = {} salty tears'\
               .format(idx+1,tm.owner,tm.mpp,tm.score,\
                          tm.result,tm.salt)
        right += '\n'
    leftText.insert(1.0, left)
    rightText.insert(1.0, right)

def lcopy(*args):
    master.clipboard_clear()
    master.clipboard_append(leftText.get(1.0, END))

def rcopy(*args):
    master.clipboard_clear()
    master.clipboard_append(rightText.get(1.0, END))

master = Tk()
master.title("Dy-NASTY!")
master.config(pady=30, padx=10)


master.grid_columnconfigure(2, minsize=75)
master.grid_columnconfigure(4, minsize=75)


master.grid_rowconfigure(4, minsize=25)
master.grid_rowconfigure(9, minsize=25)
master.grid_rowconfigure(19, minsize=35)
master.grid_rowconfigure(14, minsize=25)

Label(master, text="Game 1").grid(row=0, column=1, columnspan=5)
Label(master, text="Game 2").grid(row=5, column=1, columnspan=5)
Label(master, text="Game 3").grid(row=10, column=1, columnspan=5)
Label(master, text="Game 4").grid(row=15, column=1, columnspan=5)

Label(master, text=" vs ").grid(column=3, row=1)
Label(master, text=" vs ").grid(column=3, row=6)
Label(master, text=" vs ").grid(column=3, row=11)
Label(master, text=" vs ").grid(column=3, row=16)

Label(master, text=" score ").grid(column = 3, row=2)
Label(master, text=" score ").grid(column = 3, row=7)
Label(master, text=" score ").grid(column = 3, row=12)
Label(master, text=" score ").grid(column = 3, row=17)

Label(master, text=" MPP ").grid(column = 3, row=3)
Label(master, text=" MPP ").grid(column = 3, row=8)
Label(master, text=" MPP ").grid(column = 3, row=13)
Label(master, text=" MPP ").grid(column = 3, row=18)

Label(master, text=" ").grid(column=3, row=4)
Label(master, text=" ").grid(column=3, row=9)
Label(master, text=" ").grid(column=3, row=14)
Label(master, text=" ").grid(column=3, row=19)
Label(master, text=" ").grid(column=3, row=21)
Label(master, text=" ").grid(column=1, row=0)
Label(master, text=" ").grid(column=7, row=0)

opponents = []
stringvars = []
teamvars = []
scores = []
scoreboxes = []
mpps = []
mppboxes = []
oldselects = [""] * 8

row = 1
column =2
for i in xrange(8):
    stringvars.append(StringVar(master))
    opponents.append(
        OptionMenu(
            master, stringvars[i], *choices,
            command=lambda caller,i=i:update(caller, i)))
    opponents[i].grid(column=column, row=row)
    if (i % 2):
        scores.append(StringVar(master))
        scoreboxes.append(Label(master, textvariable=scores[i]))
        scoreboxes[i].grid(column=4, row=row+1)
        mpps.append(StringVar(master))
        mppboxes.append(Label(master, textvariable=mpps[i]))
        mppboxes[i].grid(column=4, row = row+2)
        column = 2
        row += 5
    else:
        scores.append(StringVar(master))
        scoreboxes.append(Label(master, textvariable=scores[i]))
        scoreboxes[i].grid(column=2, row = row+1)
        mpps.append(StringVar(master))
        mppboxes.append(Label(master, textvariable=mpps[i]))
        mppboxes[i].grid(column=2, row = row+2)
        column = 4

b = Button(master, text="Get Output", command=getOutput)
b.grid(row=20, column=3)

leftLabel= Label(master, text="ESPN")
leftLabel.grid(column=1, row=21, columnspan=2)
leftText = Text(master, height=10, width=65)
leftText.grid(column=1, row=22, columnspan=2)
leftCopy = Button(master, text="Copy to Clipboard", command=lcopy)
leftCopy.grid(column=1, row=23, columnspan=2)

rightLabel= Label(master, text="Facebook")
rightLabel.grid(column=4, row=21, columnspan=2)
rightText = Text(master, height=10, width=65)
rightText.grid(column=4, row=22, columnspan=2)
rightCopy = Button(master, text="Copy to Clipboard", command=rcopy)
rightCopy.grid(column=4, row=23, columnspan=2)
        
master.mainloop()
