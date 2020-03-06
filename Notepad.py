import tkinter as tk
import tkinter.scrolledtext as ScrolledText
import tkinter.font as font
from tkinter import filedialog
import os


# Variables
files = []
indexes = []
buttons = []


# Window Settings
root = tk.Tk()
root.title("Notepad^")
root.geometry("900x700")
root.iconbitmap('Notepad.ico')


# Fonts
buttonFont = font.Font(family='Microsoft Sans Serif', size=10)
titleFont = font.Font(family='Georgia', size=30, weight="bold")
textFont = font.Font(family='Microsoft Sans Serif', size=14)

# Canvases
textCanvas = tk.Canvas(root)
textCanvas['bg'] = 'white'
textCanvas['highlightthickness'] = "0"
textCanvas.place(relx=0, rely=0.05, relwidth=1, relheight=1)

buttonCanvas = tk.Canvas(root)
buttonCanvas['bg'] = "white"
buttonCanvas['highlightthickness'] = "0"
buttonCanvas.place(relx=0, rely=0, relwidth=1, relheight=0.05)


# Classes


class FileButton(tk.Button):
    def __init__(self, index):
        super().__init__(buttonCanvas)
        self['bg'] = 'white'
        self['text'] = os.path.basename(files[index].name)
        self['fg'] = 'gray'
        self['border'] = '0'
        self["font"] = buttonFont
        self['command'] = lambda: displayText(index, indexes)
        self.pack(side=tk.LEFT, fill=tk.Y)
        self.config(width=len(os.path.basename(files[index].name)))
        self.bind('<Button-3>', lambda event: closeFile(False, index))


class TextField(tk.Text):
    def __init__(self):
        super().__init__(textCanvas)
        # Settings
        self['border'] = '0'
        self['fg'] = '#282828'
        self['font'] = textFont
        self['wrap'] = tk.WORD
        self['insertbackground'] = "gray"
        self['selectbackground'] = "gray"
        self['selectborderwidth'] = "20px"
        self['state'] = 'normal'
        self['padx'] = '80'
        self.bind("<Control-e>", title)
        self.bind("<Control-r>", color)
        self.bind("<Control-v>", paste)
        self.bind("<Control-d>", textReset)

        self.pack(fill=tk.X)

# Methods


def openFile():
    file = tk.filedialog.askopenfile(parent=root, mode='rb')
    entry = True
    for x in files:
        if x != None:
            if x.name == file.name:
                entry = False
        else:
            pass

    if file != None and entry:
        files.append(file)
        buttons.append(FileButton(files.index(file)))
        displayText(files.index(file), indexes)
        file.close()


def createNewFile():
    f = open("Untitled-" + str(len(files)) + ".txt", "w+", encoding='utf-8')
    files.append(f)
    buttons.append(FileButton(files.index(f)))
    displayText(files.index(f), indexes)
    f.close()


def hideButton():
    buttons[indexes[len(indexes)-1]].pack_forget()


def saveManual():
    buttonIndex = indexes[len(indexes)-1]
    if files[buttonIndex] != None:
        if files[buttonIndex].name[0:8] == "Untitled":
            saveNewFile()
        else:
            f = open(f"{files[buttonIndex].name}", 'r+', encoding='utf-8')
            f.write(textField.get("1.0", tk.END))
            f.close()
    else:
        pass


def saveNewFile():
    file = tk.filedialog.asksaveasfile(
        mode='w', defaultextension=".txt", initialfile="s_"+files[indexes[len(indexes)-1]].name)

    if file != None:

        oldIndex = indexes[len(indexes)-1]

        os.remove(f"{files[oldIndex].name}")
        hideButton()

        files.remove(files[oldIndex])
        files.insert(oldIndex, file)

        buttons.remove(buttons[files.index(file)])
        buttons.insert(files.index(file), FileButton(files.index(file)))

        file.write(textField.get('1.0', tk.END))
        displayText(files.index(file), indexes)
        file.close()


def closeFile(closing, index):

    if buttons[index]["bg"] == "gray":
        pass

    if buttons[index]["bg"] == "white" or closing:

        for file, button in zip(files, buttons):
            if files.index(file) == index:

                if files[index].name[0:8] == "Untitled":
                    displayText(index, indexes)
                    file = tk.filedialog.asksaveasfile(
                        mode='w', defaultextension=".txt", title=files[index].name, initialfile="s_"+files[index].name)
                    if file != None:
                        file.write(textField.get('1.0', tk.END))
                        file.close()
                        os.remove(files[index].name)
                        buttons[index].pack_forget()
                        files[index] = None
                        buttons[index] = None
                        displayText(indexes[len(indexes)-2], indexes)
                    if closing:
                        os.remove(files[index].name)
                        buttons[index].pack_forget()
                        files[index] = None
                        buttons[index] = None
                        displayText(indexes[len(indexes)-2], indexes)
                else:
                    buttons[index].pack_forget()
                    files[index] = None
                    buttons[index] = None
                    displayText(indexes[len(indexes)-2], indexes)


def autoSave():
    if files[indexes[len(indexes)-2]] != None:
        f = open(f"{files[indexes[len(indexes)-2]].name}",
                 'r+', encoding='utf-8')
        f.write(textField.get("1.0", tk.END))
        f.close()
    else:
        pass


def displayText(index, indexes):

    indexes.append(index)
    indexes = [indexes[i] for i in range(len(indexes)) if (
        i == 0) or indexes[i] != indexes[i-1]]

    for otherButton in buttons:
        if otherButton != None:
            otherButton['bg'] = "white"
            otherButton['fg'] = "gray"
        else:
            pass
    if buttons[index] != None:
        buttons[index]['bg'] = "gray"
        buttons[index]['fg'] = "white"
    else:
        pass

    autoSave()

    textField.delete('1.0', tk.END)
    if files[index] != None:
        f = open(f'{files[index].name}', encoding='utf-8')
        text = f.read()
        textField.insert('1.0', text)
        f.close()
    else:
        pass


# Shortcuts
def paste(event):
    tk.Entry.event_delete(textField, "<<Paste>>")
    tk.Entry.event_generate(textField, '<<Paste>>')
    textField.see(tk.END)


def color(event):

    if textField.tag_ranges("sel"):
        textField.tag_add("color", "sel.first", "sel.last")
        textField.tag_config("color", foreground="#8A2BE2")
    else:
        word_start = textField.index("insert-1c wordstart")
        word_end = textField.index("insert")
        textField.tag_add('color', word_start, word_end)
        textField.tag_config("color", foreground="#8A2BE2")


def textReset(event):
    if textField.tag_ranges("sel"):
        textField.tag_add("color", "sel.first", "sel.last")
        textField.tag_config("color", foreground="black")

        textField.tag_add("nadpis", "sel.first", "sel.last")
        textField.tag_config("nadpis", font=textFont)
    else:
        textField.tag_add('color', "insert-1c wordstart", "insert")
        textField.tag_config("color", foreground="black")

        textField.tag_add('nadpis', "insert linestart", "insert")
        textField.tag_config("nadpis", font=textFont)


def title(event):
    if textField.tag_ranges("sel"):
        textField.tag_add("nadpis", "sel.first", "sel.last")
        textField.tag_config("nadpis", font=titleFont)

    if not textField.tag_ranges("sel"):
        cur_cursor = textField.index("insert")
        line_start = textField.index("insert-1c linestart")
        textField.tag_add('nadpis', line_start, cur_cursor)
        textField.tag_config("nadpis", font=titleFont)


def ctrlS(event):
    saveManual()


def ctrlO(event):
    openFile()


def ctrlN(event):
    createNewFile()


def ctrlQ(event):
    for x in files:
        if x != None:
            if x.name[0:8] == "Untitled":
                closeFile(True, files.index(x))

        else:
            pass
    root.quit()


def leftFile(event):

    currentButton = indexes[len(indexes)-1]

    buttons.reverse()

    if buttons.index(buttons[currentButton])-1 >= 0:
        displayText(buttons.index(buttons[currentButton])-1, indexes)


def rightFile(event):
    currentButton = indexes[len(indexes)-1]

    buttons.reverse()

    if buttons.index(buttons[currentButton])+1 >= 0:
        displayText(buttons.index(buttons[currentButton])+1, indexes)


# Static parts

textField = TextField()

plusButton = tk.Button(buttonCanvas)
plusButton['bg'] = 'white'
plusButton['text'] = '+'
plusButton['fg'] = '#464646'
plusButton['border'] = '0'
plusButton["font"] = font.Font(family='MS Reference Sans Serif', size=20)
plusButton['command'] = createNewFile
plusButton.pack(side=tk.LEFT, fill=tk.Y)
plusButton.config(width=3)

openButton = tk.Button(buttonCanvas)
openButton['bg'] = 'white'
openButton['text'] = 'open'
openButton['fg'] = '#464646'
openButton['border'] = '0'
openButton["font"] = font.Font(family='MS Reference Sans Serif', size=15)
openButton['command'] = openFile
openButton.pack(side=tk.RIGHT, fill=tk.Y)
openButton.config(width=len(openButton['text']))


saveButton = tk.Button(buttonCanvas)
saveButton['bg'] = 'white'
saveButton['text'] = 'save'
saveButton['fg'] = '#464646'
saveButton['border'] = '0'
saveButton["font"] = font.Font(family='MS Reference Sans Serif', size=15)
saveButton['command'] = saveManual
saveButton.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
saveButton.config(width=len(saveButton['text']))


# Binds
root.bind('<Control-s>', ctrlS)
root.bind('<Control-o>', ctrlO)
root.bind('<Control-q>', ctrlQ)
root.bind('<Control-n>', ctrlN)
root.bind('<Control-Left>', leftFile)
root.bind('<Control-Right>', rightFile)
root.protocol("WM_DELETE_WINDOW", lambda: ctrlQ(""))


# Loop
createNewFile()
root.mainloop()
