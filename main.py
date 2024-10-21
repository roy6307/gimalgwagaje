# solver (module)
# main window


from tkinter import *



def mainflow():

    idx = 0

    buttonPool = list()

    mainWindow = Tk()
    mainWindow.geometry("500x400")

    for i in range(81):

        buttonPool.append(Button(mainWindow, bg="grey", text=" "))

    for i in range(9):

        for j in range(9):

            buttonPool[idx].grid(row=i, column=j)
            idx+=1

    mainWindow.mainloop()




if __name__ == "__main__":

    mainflow()
