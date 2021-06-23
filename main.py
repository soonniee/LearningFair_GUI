import sqlite3
import os
from table import create_table
from assignment import handle_assignment
from attendance import handle_attendance
from score import handle_score
from tkinter import *
from functools import partial
def add_course(course_name,registerGUI,mainGUI):
    name = course_name.get()
    data = [name]
    sql = '''INSERT INTO course (course_name) VALUES (?)'''
    db.execute(sql,data)
    registerGUI.destroy()
    mainGUI.destroy()
    gui_main()
def gui_register(mainGUI):
    registerGUI = Tk()
    registerGUI.title('수강과목 등록')
    registerGUI.geometry('300x100')
    Label(registerGUI,text="수강과목 등록",font=('맑은 고딕',12)).grid(row=1,column=0)
    Label(registerGUI,text="수강과목",font=('맑은 고딕',12)).grid(row=2)
    course_name = Entry(registerGUI,width=15)
    course_name.grid(row=2,column=1)
    Button(registerGUI,text = "등록",width=7,font=('맑은 고딕',10),bg="lightgreen",command=partial(add_course,course_name,registerGUI,mainGUI)).grid(row=2,column=2,padx=10)
    # Button(registerGUI,text = "종료",width=7,font=('맑은 고딕',12),bg="tomato",command=registerGUI.destroy).grid(row=1,column=3)
def selected_lookup(listbox,lookupGUI,choice):
    course_id = listbox.curselection()
    course_name = listbox.get(course_id)
    course_id = course_id[0]+1
    lookupGUI.destroy()
    if choice == 1:handle_assignment(course_name,course_id,db)
    elif choice == 2: handle_attendance(course_name,course_id,db)
    else : handle_score(course_name,course_id,db)

def gui_lookup(courses,mainGUI):
    lookupGUI = Tk()
    lookupGUI.title('수강과목 조회')
    lookupGUI.geometry('400x300')
    Label(lookupGUI,text="수강과목 선택 리스트",font=('맑은 고딕',13)).pack()
    listbox = Listbox(lookupGUI, width=100, height=10, font=('맑은 고딕',12),selectmode=SINGLE)
    for idx,course in enumerate(courses):
        listbox.insert(idx, course[1])
        listbox.pack()
    Button(lookupGUI,text = "과제 등록/조회",width=12,font=('맑은 고딕',12),fg='white',bg="black",command=partial(selected_lookup,listbox,lookupGUI,1)).pack(side=LEFT,padx=5)
    Button(lookupGUI,text = "출결 등록/조회",width=12,font=('맑은 고딕',12),fg='white',bg="black",command=partial(selected_lookup,listbox,lookupGUI,2)).pack(side=LEFT,padx=5)
    Button(lookupGUI,text = "성적 등록/조회",width=12,font=('맑은 고딕',12),fg='white',bg="black",command=partial(selected_lookup,listbox,lookupGUI,3)).pack(side=LEFT,padx=5)
    
def gui_main():
    mainGUI = Tk()
    mainGUI.title('아이캠퍼스 수강과목 관리 프로그램')
    photo = PhotoImage(file='icampus.png')
    label_img = Label(mainGUI,image=photo)

    msg = "[ 수강과목 리스트 ]"
    label_list = Label(mainGUI,text=msg,font=('맑은 고딕',14))
    courses = db.execute("SELECT * FROM course").fetchall()
    label_img.pack()
    label_list.pack()
    for course in courses:
        msg = f"{course[1]}"
        label_list = Label(mainGUI,text=msg,font=('맑은 고딕',13,'bold'))
        # label_list.config(anchor=CENTER)
        label_list.pack()
    Button(mainGUI,text = "새 수강과목 등록",fg="black",bg="lightgreen",width=18,font=('맑은 고딕',13),command= partial(gui_register,mainGUI)).pack(side=LEFT)
    Button(mainGUI,text = "기존 수강과목 조회",fg="black",bg="skyblue",width=18,font=('맑은 고딕',13),command = lambda :gui_lookup(courses,mainGUI)).pack(side=LEFT)
    Button(mainGUI,text = "종료",width=13,font=('맑은 고딕',13),fg="black",bg="tomato",command=mainGUI.quit).pack(side=LEFT)
    mainGUI.mainloop()

if __name__ == '__main__':
    db = create_table("LF.db")
    gui_main()
    # main()