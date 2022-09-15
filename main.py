import png
import numpy as np
import tkinter as tk
from tkinter import *
import sv_ttk
from tkinter import filedialog as fd



size = "PNG Format: "
filename = 0
pic = 0
pic_Data = 0
inputpxwidth = 0
inputpxheight = 0
rows = 0
cols = 0
savedirectory = 0
def getFilename():
    global filename
    filename = fd.askopenfilename()
    if filename.endswith(".png"):
        lpath.config(text=filename)
        readPng(filename)
        lcols.place(x=20, y=150, width=200, height=30)
        lrows.place(x=190, y=150, width=200, height=30)
        bcols.place(x=50, y=180, width=150, height=30)
        brows.place(x=230, y=180, width=150, height=30)
        saveDirectoryButton.place(x=410, y=180, width=150, height=30)
        checkButton.place(x=460, y= 215, width=50, height=20)
    else:
        filename = 0
        lpath.config(text="Please select a PNG")

def saveDirectory():
    global savedirectory
    savedirectory = fd.askdirectory()

def check():
    try:
        global pic_Data, savedirectory, inputpxwidth, inputpxheight, cols, rows
        rows = int(brows.get())
        cols = int(bcols.get())
        outputpxheight = inputpxheight / rows
        outputpxwidth = inputpxwidth / cols


    except ValueError:
        print("Error")

    is_all_zero = np.all((pic_Data == 0))
    print(is_all_zero)
    if not is_all_zero and savedirectory != 0 and rows != 0 and cols != 0:
        sliceFormatButton.place(x=100, y=240, width=400, height=50)
        loutputpx.config(text="Output Size: " + str(int(outputpxwidth)) + "px x " + str(int(outputpxheight)) + "px")
    else:
        loutputpx.config(text="Something went wrong")

def getFormat(x,y):
    global inputpxheight
    global inputpxwidth
    inputpxwidth = x
    inputpxheight = y
    global size
    size = ("PNG Format: " + str(inputpxwidth) + "px x " + str(inputpxheight) + "px")
    lformat.config(text = size)

def readPng(path):
    # Einlesen des Pngs
    pic = png.Reader(path)
    # Umwandeln in PNG Objekt
    pic = pic.read_flat()
    getFormat(int(pic[0]),int(pic[1]))
    global pic_Data
    pic_Data = np.array(pic[2]).astype("int16")#vllt falsch weil 8
    print(pic_Data)




def slice(inputArr, columns, rows, inputwidth, inputheight, inputtype = "rgba"):
    if inputtype.casefold() == "rgba".casefold():
        pixel = 4
    else:
        pixel = 1
    pxheight = int(inputheight/rows)
    pxwidth = int(inputwidth/columns*pixel)
    slices = rows * columns
    junk = inputwidth * pixel * pxheight
    rowpx = inputwidth * pixel
    for x in range(slices):
        tmp = np.zeros(shape=(pxheight, pxwidth)).astype("int8")
        for y in range(len(tmp)):
            reihe = x // columns
            offset = x % columns
            iter = reihe * junk + y * rowpx + offset * pxwidth
            for z in range(len(tmp[y])):
                tmp[y][z] = inputArr[iter]
                iter += 1
        global savedirectory
        print(str(x) + " Elements saved.")
        png.from_array(tmp, "RGBA").save(str(savedirectory)+"/"+ str(x) + ".png")


# GUI TKinter
# Interface
root = tk.Tk()
root.geometry('600x300')
root.resizable(False, False)
root.title('PNG Slicer')
# dropDownMenu for choosing Sensor
# open button
open_button = tk.Button(
    root,
    text='Open a File',
    command=getFilename
)
open_button.place(x=50,y=50,width=70, height=20)

#label
select = Label(root, text="Select PNG")
select.place(x= 50, y=20, width=70, height=20)
lpath = Label(root, text="")
lpath.place(x=130, y= 50, width=450, height=20)
lformat = Label(root, text="")
lformat.place(x=130, y= 80, width=450, height=20)
#ab hier soll erstmal unsichtbar sein
lcols = Label(root, text="Spalten")
#lcols.place(x=100, y=150, width=200, height=30)
lrows = Label(root, text="Zeilen")
#lrows.place(x=300, y=150, width=200, height=30)
bcols = Entry(root)
#bcols.place(x=130, y=180, width=150, height=30)
brows = Entry(root)
#brows.place(x=330, y=180, width=150, height=30)
loutputpx = Label(root, text="")
loutputpx.place(x=100, y=210, width=300, height=30)
saveDirectoryButton = tk.Button(root, text='Select Directory to save', command=saveDirectory)
#saveDirectoryButton.place(x=500, y=180, width=50, height=30)
checkButton = tk.Button(root, text="Check", command=check)

sliceFormatButton = tk.Button(root, text='Slice!', command=lambda:slice(pic_Data, cols, rows, inputpxwidth, inputpxheight))#, command=slice()
#sliceFormatButton.place(x=100, y=240, width=400, height=50)


sv_ttk.set_theme("dark")

root.mainloop()
#slice(bild_daten, columns, rows, bild_breite, bild_höhe)
