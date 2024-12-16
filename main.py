# solver (module)
# main window

# require ttkthemes

from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import tkinter.messagebox as msgbox
import cju # from https://github.com/roy6307/cju-oc
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import os



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

executor = ThreadPoolExecutor(max_workers=1)

treeSelect = True

tasks = []



def merge():

    executor.shutdown()
    #os.remove("ts/chunklist.m3u8")

    updateProgress(1, 1, "Download completed...!")

    fn = next(os.walk("./ts"), (None, None, []))[2]

    mv = open("ts/vd.ts", "ab")

    for i in range(len(fn)):

        f = open(f"ts/media_{i}.ts", "rb")
        t = f.read()
        q = len(t)
        
        updateProgress(i + 1, len(fn), f"Merging media_{i}.ts into vd.ts ({q})")

        mv.write(t)

        f.close()

        os.remove(f"ts/media_{i}.ts")

    mv.close()
    


def check_tasks():

    global tasks

    done_count = sum(1 for t in tasks if t.done())
    
    if done_count == len(tasks):
        
        merge()

    else:

        mainWindow.after(100, check_tasks)



def summarization():

    # F I N A L 

    global treeSelect
    global tasks

    widgetPool["B_Sum"]["state"] = "disabled"
    treeSelect = False

    updateProgress(0, 1, "Downloading files")
    
    print(widgetPool["T_Detail"].get_children())
    
    for i in widgetPool["T_Detail"].get_children():
        
        j = widgetPool["T_Detail"].item(i, option="values")

        if j[2] == "O":
            
            tasks.append(executor.submit(cju.dlStream, j[0], updateProgress))

    check_tasks()



def queryClassDetail():

    widgetPool["List_Frame"].pack_forget()
    widgetPool["Login_Frame"].pack_forget()
    widgetPool["List_SubFrame"].pack_forget()
    widgetPool["Detail_Frame"].pack()

    updateProgress(0, 1, "Querying...")
    
    print(widgetPool["T_Tree"].get_children())
    
    for i in widgetPool["T_Tree"].get_children():
        
        j = widgetPool["T_Tree"].item(i, option="values")

        if j[2] == "O":

            #widgetPool["L_Status"].config(text="HIT!")
            
            target = classList[int(i)]

            details = cju.setSpecificClassDetail(target[1])

            updateProgress(1, 1, "Done...!")

            for i in details:
                
                widgetPool["T_Detail"].insert('', 'end', text=i[1], value=(i[1], i[0], ""), iid=i[1])
        
        

def updateProgress(current: int, end: int, txt: str):
    
    widgetPool["L_Status"].config(text=txt)
    widgetPool["P_rate"].set((current/end)*100)



def treeSelection(event, F: str):

    if F == "T_Detail" and treeSelect == False:

        return

    item = widgetPool[F].focus()
    print(widgetPool[F].item(item, option="values"))
    
    v1 = widgetPool[F].item(item, option="values")

    if item != "":
                
        if v1[-1] != "O":

            v2 = (v1[0], v1[1], "O")
            widgetPool[F].item(item, option=None, values=v2)

        else:

            v2 = (v1[0], v1[1], "")
            widgetPool[F].item(item, option=None, values=v2)



def loginEvent(event, id: str = "", pw: str = ""):

    if widgetPool["B_login"]["state"] == "disabled":

        return
    
    updateProgress(0, 1, "Loggin in...")
    
    res = cju.init(id, pw)

    if res == -1:

        msgbox.showerror("Error", "id/pw가 비어있습니다.")
        updateProgress(0, 1, "Empty id/pw")

    elif res == -2:

        msgbox.showerror("Error", "로그인에 실패하였습니다.")
        updateProgress(0, 1, "Login failure")

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

    L_Tip1 = Label(List_Frame, text="사이버 강의 하나만 선택해주세요")

    T_Tree.bind("<ButtonRelease-1>", lambda e: treeSelection(e, "T_Tree"))
    
    B_run = Button(List_Frame, text="정보 가져오기", command=queryClassDetail)

    T_Tree.pack()
    L_Tip1.pack(side="top", ipady="3")
    B_run.pack(side="bottom", ipady="7")

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



    # Detail Frame
    # ------------------------------------------------------------------------------------

    T_Detail = ttk.Treeview(Detail_Frame, columns=["id", "title", "selected"], displaycolumns=["id", "title", "selected"])

    T_Detail.column("#0", width=0, stretch=NO)

    T_Detail.column("id", width=50, anchor="center")
    T_Detail.heading("id", text="id", anchor="center")
    
    T_Detail.column("title", width=400, anchor="center")
    T_Detail.heading("title", text="제목", anchor="center")

    T_Detail.column("selected", width=50, anchor="center")
    T_Detail.heading("selected", text="선택됨", anchor="center")

    T_Detail["show"] = "headings"

    T_Detail.bind("<ButtonRelease-1>", lambda e: treeSelection(e, "T_Detail"))

    L_Tip2 = Label(Detail_Frame, text="요약할 강의를 선택해주세요")

    B_Sum = Button(Detail_Frame, text="요약하기", command=summarization)

    L_Tip2.pack(side="top", ipady="3")
    B_Sum.pack(side="bottom", ipady="7")
    T_Detail.pack()

    # ------------------------------------------------------------------------------------



    Status_Frame.pack(side="bottom", pady=10)
    Login_Frame.pack(side="left")
    List_Frame.pack(side="right", padx=10)
    List_SubFrame.pack(expand=True, fill="both")
    

    widgetPool["E_id"] = E_id
    widgetPool["E_pw"] = E_pw
    widgetPool["T_Tree"] = T_Tree
    widgetPool["T_Detail"] = T_Detail
    widgetPool["L_Status"] = L_Status
    widgetPool["P_rate"] = P_rate
    widgetPool["B_login"] = B_login
    widgetPool["B_Sum"] = B_Sum
    widgetPool["P_bar"] = P_bar
    widgetPool["Login_Frame"] = Login_Frame
    widgetPool["List_Frame"] = List_Frame
    widgetPool["List_SubFrame"] = List_SubFrame
    widgetPool["Status_Frame"] = Status_Frame
    widgetPool["Detail_Frame"] = Detail_Frame

    mainWindow.mainloop()




if __name__ == "__main__":

    mainflow()
