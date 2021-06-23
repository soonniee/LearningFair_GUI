import sqlite3
import datetime
import re      
from tkinter import *
from tkinter import messagebox
from functools import partial
def input_check(course_id,ass_due,ass_name,db,registerGUI):
    date_re = re.compile('^\d{4}.(0[1-9]|1[012]).(0[1-9]|[12][0-9]|3[01]) (0[0-9]|1[0-9]|2[0-4]):([0-5][0-9]):([0-5][0-9])')
    due = ass_due.get()
    m = date_re.match(due)
    if not m : 
        messagebox.showerror('입력오류','알맞지 않은 입력 형식입니다!!')
    else :
        ass_name=ass_name.get()
        data = [course_id,ass_name,due,0]
        sql = '''INSERT INTO assignment (course_id,ass_content,ass_due,ass_complete) VALUES (?,?,?,?)'''
        db.execute(sql,data)
        messagebox.showinfo('등록완료',f'[{ass_name}] 과제 등록 완료!!')
        registerGUI.destroy()
def selected_ass(db,listbox,asslistGUI):
    for ass_id in listbox.curselection():
        ass_name = listbox.get(ass_id)
        print(ass_id,ass_name)
        db.execute("UPDATE assignment SET ass_complete=? WHERE id=?",(1,ass_id+1))
    asslistGUI.destroy()
def show_asslist(course_name,course_id,db):
    asslistGUI = Tk()
    asslistGUI.title(f'수강과목 : {course_name}')
    asslistGUI.geometry('400x400')
    msg = f"{course_name} 과제 리스트"
    Label(asslistGUI,text=msg,font=('맑은 고딕',14)).pack()
    now = datetime.datetime.now()
    late = []
    listbox = Listbox(asslistGUI, width=100, height=10,font=('맑은 고딕',11),selectmode=SINGLE)
    assignments = db.execute("SELECT * FROM assignment WHERE course_id='%d'" %course_id)
    
    for ass in assignments:
        due_date = datetime.datetime.strptime(ass[3],'%Y.%m.%d %H:%M:%S')
        if(ass[4] == 0 and now > due_date):
            db.execute("UPDATE assignment SET ass_complete=? WHERE id=?",(2,ass[0]))
        if ass[4] == 0: 
            msg = f"{ass[0]} : {ass[2]} / {ass[3]} / 진행중"
        elif ass[4] == 1 : 
            msg = f"{ass[0]} : {ass[2]} / {ass[3]} / 제출 완료"
        else : 
            late.append(ass[0])
            msg = f"{ass[0]} : {ass[2]} / {ass[3]} / 지각 처리"
        listbox.insert(ass[0], msg)
        listbox.pack()
    Button(asslistGUI,text = "제출완료",width=18,font=('맑은 고딕',12),fg='black',
    bg="skyblue",command=partial(selected_ass,db,listbox,asslistGUI)).pack(side=LEFT,padx=15)
    Button(asslistGUI,text = "종료",width=18,font=('맑은 고딕',12),fg='black',
    bg="tomato",command=asslistGUI.destroy).pack(side=LEFT,padx=15)


    # ass_id = int(input("\n[ 제출 완료 등록할 과제(번호) / 없을시(0) ] : "))
    # if ass_id == 0: break
    # else : 
    #     if ass_id in late : print("\n이미 지각 처리된 과제입니다!!")
    #     else : db.execute("UPDATE assignment SET ass_complete=? WHERE id=?",(1,ass_id))
def handle_assignment(course_name,course_id,db):
    registerGUI = Tk()
    registerGUI.title(f'수강과목 : {course_name}')
    registerGUI.geometry('375x200')
    Label(registerGUI,text="\n과제 등록",font=('맑은 고딕',12)).grid(row=1,column=0)
    Label(registerGUI,text="과제",font=('맑은 고딕',10)).grid(row=2)
    ass_name = Entry(registerGUI,width=15)
    ass_name.grid(row=2,column=1)
    Label(registerGUI,text="제출기한",font=('맑은 고딕',10)).grid(row=3)
    Label(registerGUI,text="(YYYY.MM.DD HH:MM:SS)",font=('맑은 고딕',8)).grid(row=4)
    ass_due = Entry(registerGUI,width=15)
    ass_due.grid(row=3,column=1)
    Button(registerGUI,text = "과제 등록",width=10,font=('맑은 고딕',12),
    fg="black",bg="skyblue",command=partial(input_check,course_id,ass_due,ass_name,db,registerGUI)).grid(row=2,column=2,rowspan=2,padx=20)
    Label(registerGUI,text="\n과제 조회\n",font=('맑은 고딕',12)).grid(row=7,column=0)
    Button(registerGUI,text = "과제 조회",width=10,font=('맑은 고딕',12),
    fg="black",bg="tomato",command=partial(show_asslist,course_name,course_id,db)).grid(row=7,column=2,rowspan=2,padx=20)
    