from tkinter import *


class ArisButtons:
	def __init__(self, master):

		topframe = Frame(master)
		topframe.pack()

		bottomframe = Frame(master)
		bottomframe.pack(side=BOTTOM)


		self.label_1 = Label(topframe, text='number 1')
		self.label_1.grid(row = 0, column = 0)
		self.label_2 = Label(topframe, text='number 2')
		self.label_2.grid(row = 1, column = 0)

		#user input
		self.entry_1 = Entry(topframe)
		self.entry_1.grid(row = 0, column = 1)
		self.entry_2 = Entry(topframe)
		self.entry_2.grid(row = 1, column = 1)

		'''
		text = Text(topframe)
		text.pack(side=BOTTOM)
		output = printMessage(self)
		text.insert(output)
		'''

		self.printButton = Button(bottomframe, 
			text='Add numbers', 
			command=self.printMessage)
		self.printButton.pack(side=LEFT)

		self.quitButton = Button(bottomframe, text='quit', command=master.quit)
		self.quitButton.pack(side=LEFT)

	def printMessage(self):
		n1 = float(self.entry_1.get())
		n2 = float(self.entry_2.get())
		return n1 + n2

root = Tk()

b = ArisButtons(root)

root.mainloop()