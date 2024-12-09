# solver (module)
# main window

# require ttkthemes

from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import tkinter.messagebox as msgbox
import cju # from https://github.com/roy6307/cju-oc
import sqlite3
import math



mainWindow = ThemedTk(theme='winnative')
mainWindow.geometry("640x360")
mainWindow.title("CJU helper")

"""
    widgetPool["E_id"] = E_id
    widgetPool["E_pw"] = E_pw
    widgetPool["T_Tree"] = T_Tree
    widgetPool["L_Status"] = L_Status
    widgetPool["P_rate"] = P_rate
    widgetPool["B_login"] = B_login
    widgetPool["P_bar"] = P_bar
    widgetPool["Login_Frame"] = Login_Frame
    widgetPool["List_Frame"] = List_Frame
    widgetPool["List_SubFrame"] = List_SubFrame
    widgetPool["Status_Frame"] = Status_Frame
    widgetPool["Detail_Frame"] = Detail_Frame

"""
widgetPool = {}

classList = []

def runrunrun(reset=False):

    widgetPool["List_Frame"].pack_forget()
    widgetPool["Login_Frame"].pack_forget()
    widgetPool["List_SubFrame"].pack_forget()
    widgetPool["Status_Frame"].pack_forget()
    widgetPool["Detail_Frame"].pack()

    return
    
    print(widgetPool["T_Tree"].get_children())
    
    for i in widgetPool["T_Tree"].get_children():
        
        j = widgetPool["T_Tree"].item(i, option="values")

        if j[2] == "O":

            #widgetPool["L_Status"].config(text="HIT!")
            
            target = classList[int(i)]
            
            if reset:
                details = cju.setSpecificClassDetail(target[1], option=True)
            else:
                details = cju.setSpecificClassDetail(target[1])

            for i in details:
                
                #print(i)
                
                if reset:
                    cju.reset(i, updateProgress)
                    
                else:
                    cju.run(i, updateProgress)
        
        

def updateProgress(current, end, txt):
    
    widgetPool["L_Status"].config(text=txt)
    widgetPool["P_rate"].set((current/end)*100)

def treeSelection(event):

    item = widgetPool["T_Tree"].focus()
    print(widgetPool["T_Tree"].item(item, option="values"))
    
    v1 = widgetPool["T_Tree"].item(item, option="values")

    if item != "":
                
        if v1[-1] != "O":

            v2 = (v1[0], v1[1], "O")
            widgetPool["T_Tree"].item(item, option=None, values=v2)

        else:

            v2 = (v1[0], v1[1], "")
            widgetPool["T_Tree"].item(item, option=None, values=v2)

def loginEvent(event, id="", pw=""):

    if widgetPool["B_login"]["state"] == "disabled":

        return
    
    res = cju.init(id, pw)

    if res == -1:

        msgbox.showerror("Error", "id/pw가 비어있습니다.")

    elif res == -2:

        msgbox.showerror("Error", "로그인에 실패하였습니다.")

    elif res == 0:

        widgetPool["B_login"]["state"] = "disabled"
        widgetPool["E_id"]["state"] = "disabled"
        widgetPool["E_pw"]["state"] = "disabled"

        widgetPool["L_Status"].config(text="Successfully logged in")
        widgetPool["P_rate"].set(100)

        l = cju.getClasses()

        for i in range(len(l)):
            
            classList.append(l[i])
            widgetPool["T_Tree"].insert('', 'end', text=i, value=(str(i), l[i][0], ""), iid=str(i))


def mainflow():

    

    Login_Frame = Frame(mainWindow, relief="solid")
    List_Frame = Frame(mainWindow, relief="solid")
    List_SubFrame = Frame(List_Frame, relief="solid", bg="grey")
    Status_Frame = Frame(mainWindow, relief="solid")
    Detail_Frame = Frame(mainWindow, relief="solid")

    # Login Frame
    # ------------------------------------------------------------------------------------

    E_id = Entry(Login_Frame)
    E_pw = Entry(Login_Frame, show="*")

    L_id = Label(Login_Frame, text="학번")
    L_pw = Label(Login_Frame, text="비밀번호")

    B_login = Button(Login_Frame, text="로그인")

    B_login.bind("<Button-1>", lambda event: loginEvent(event, E_id.get(), E_pw.get()))

    L_id.grid(column=0, row=0, ipadx=10, pady=5)
    E_id.grid(column=1, row=0, ipady=4)

    L_pw.grid(column=0, row=1, ipadx=10, pady=12)
    E_pw.grid(column=1, row=1, ipady=4)

    B_login.grid(column=1, row=2, sticky="EW")

    # ------------------------------------------------------------------------------------



    # List Frame (Class List), and sub frame
    # ------------------------------------------------------------------------------------

    #L_Class = Label(List_Frame, text="목록")

    T_Tree = ttk.Treeview(List_SubFrame, columns=["idx", "name", "selected"], displaycolumns=["idx", "name", "selected"])

    T_Tree.column("idx", width=50, anchor="center")
    T_Tree.heading("idx", text="번호", anchor="center")
    
    T_Tree.column("name", width=200, anchor="center")
    T_Tree.heading("name", text="강의", anchor="center")

    T_Tree.column("selected", width=50, anchor="center")
    T_Tree.heading("selected", text="선택됨", anchor="center")

    T_Tree["show"] = "headings"

    L_Tip = Label(List_Frame, text="사이버 강의만 선택해주세요")

    T_Tree.bind("<ButtonRelease-1>", treeSelection)
    
    B_run = Button(List_Frame, text="run", command=runrunrun)
    
    #B_run.bind("<Button-1>", runrunrun)
    
    #B_reset = Button(List_Frame, text="RESET", command=lambda: runrunrun(reset=True))
    
    #B_reset.bind("<Button-1>", command=lambda: runrunrun(reset=True))

    T_Tree.pack()
    L_Tip.pack(side="top", ipady="3")
    B_run.pack(side="bottom", ipady=7)
    #B_reset.pack(side="bottom", ipady="7")

    # ------------------------------------------------------------------------------------


    
    # Status Frame
    # ------------------------------------------------------------------------------------

    L_Status = Label(Status_Frame, text="Please login")

    P_rate = IntVar()
    P_rate.set(0)
    P_bar = ttk.Progressbar(Status_Frame, variable=P_rate, length=300)

    L_Status.pack()
    P_bar.pack()

    # ------------------------------------------------------------------------------------



    # Menu frame
    # ------------------------------------------------------------------------------------

    #M_Frame = Menu(mainWindow)

    # ------------------------------------------------------------------------------------



    # Detail Frame
    # ------------------------------------------------------------------------------------

    T_Detail = ttk.Treeview(Detail_Frame, columns=["idx", "date", "selected"], displaycolumns=["idx", "date", "selected"])

    T_Detail.column("idx", width=50, anchor="center")
    T_Detail.heading("idx", text="번호", anchor="center")
    
    T_Detail.column("date", width=200, anchor="center")
    T_Detail.heading("date", text="주차", anchor="center")

    T_Detail.column("selected", width=50, anchor="center")
    T_Detail.heading("selected", text="선택됨", anchor="center")

    T_Detail["show"] = "headings"

    T_Detail.bind("<ButtonRelease-1>", treeSelection)

    T_Detail.pack()

    # ------------------------------------------------------------------------------------



    Status_Frame.pack(side="bottom", pady=10)
    Login_Frame.pack(side="left")
    List_Frame.pack(side="right", padx=10)
    List_SubFrame.pack(expand=True, fill="both")
    

    widgetPool["E_id"] = E_id
    widgetPool["E_pw"] = E_pw
    widgetPool["T_Tree"] = T_Tree
    widgetPool["L_Status"] = L_Status
    widgetPool["P_rate"] = P_rate
    widgetPool["B_login"] = B_login
    widgetPool["P_bar"] = P_bar
    widgetPool["Login_Frame"] = Login_Frame
    widgetPool["List_Frame"] = List_Frame
    widgetPool["List_SubFrame"] = List_SubFrame
    widgetPool["Status_Frame"] = Status_Frame
    widgetPool["Detail_Frame"] = Detail_Frame

    mainWindow.mainloop()




if __name__ == "__main__":

    mainflow()
