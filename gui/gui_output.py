from tkinter import *
import sys

class CoreGUI(object):
    def __init__(self, parent):
        text_box = Text(parent, state=DISABLED)
        text_box.pack()

        output_button = Button(parent, text="Output", command=self.main)
        output_button.pack()

    def main(self):
        print("Std Output")
        raise ValueError("Std Error")

root = Tk()
CoreGUI(root)
root.mainloop()