import sqlite3
import datetime
import re      
from tkinter import *
from tkinter import messagebox
from functools import partial
def input_check(course_id,att_due,att_name,db,registerGUI):
    date_re = re.compile('^\d{4}.(0[1-9]|1[012]).(0[1-9]|[12][0-9]|3[01]) (0[0-9]|1[0-9]|2[0-4]):([0-5][0-9]):([0-5][0-9])')
    due = att_due.get()
    m = date_re.match(due)
    if not m : 
        messagebox.showerror('입력오류','알맞지 않은 입력 형식입니다!!')
    else :
        att_name=att_name.get()
        data = [course_id,att_name,due,0]
        sql = '''INSERT INTO attendance (course_id,att_content,att_due,att_complete) VALUES (?,?,?,?)'''
        db.execute(sql,data)
        messagebox.showinfo('등록완료',f'[{att_name}] 출결 등록 완료!!')
        registerGUI.destroy()
def selected_att(db,listbox,attlistGUI):
    for att_id in listbox.curselection():
        att_name = listbox.get(att_id)
        print(att_id,att_name)
        db.execute("UPDATE attendance SET att_complete=? WHERE id=?",(1,att_id+1))
    attlistGUI.destroy()
def show_attlist(course_name,course_id,db):
    attlistGUI = Tk()
    attlistGUI.title(f'수강과목 : {course_name}')
    attlistGUI.geometry('400x400')
    msg = f"{course_name} 출결 리스트"
    Label(attlistGUI,text=msg,font=('맑은 고딕',14)).pack()
    now = datetime.datetime.now()
    late = []
    listbox = Listbox(attlistGUI, width=100, height=10,font=('맑은 고딕',11), selectmode=SINGLE)
    attendances = db.execute("SELECT * FROM attendance WHERE course_id='%d'" %course_id)
    
    for att in attendances:
        due_date = datetime.datetime.strptime(att[3],'%Y.%m.%d %H:%M:%S')
        if(att[4] == 0 and now > due_date):
            db.execute("UPDATE attendance SET att_complete=? WHERE id=?",(2,att[0]))
        if att[4] == 0: 
            msg = f"{att[0]} : {att[2]} / {att[3]} / 진행중"
        elif att[4] == 1 : 
            msg = f"{att[0]} : {att[2]} / {att[3]} / 출결 완료"
        else : 
            late.append(att[0])
            msg = f"{att[0]} : {att[2]} / {att[3]} / 지각 처리"
        listbox.insert(att[0], msg)
        listbox.pack()
    Button(attlistGUI,text = "출결완료",width=18,font=('맑은 고딕',12),fg='black',
    bg="skyblue",command=partial(selected_att,db,listbox,attlistGUI)).pack(side=LEFT,padx=15)
    Button(attlistGUI,text = "종료",width=18,font=('맑은 고딕',12),fg='black',
    bg="tomato",command=attlistGUI.destroy).pack(side=LEFT,padx=15)


    # att_id = int(input("\n[ 제출 완료 등록할 출결(번호) / 없을시(0) ] : "))
    # if att_id == 0: break
    # else : 
    #     if att_id in late : print("\n이미 지각 처리된 출결입니다!!")
    #     else : db.execute("UPDATE attendance SET att_complete=? WHERE id=?",(1,att_id))
def handle_attendance(course_name,course_id,db):
    registerGUI = Tk()
    registerGUI.title(f'수강과목 : {course_name}')
    registerGUI.geometry('375x200')
    Label(registerGUI,text="\n출결 등록",font=('맑은 고딕',12)).grid(row=1,column=0)
    Label(registerGUI,text="출결",font=('맑은 고딕',10)).grid(row=2)
    att_name = Entry(registerGUI,width=15)
    att_name.grid(row=2,column=1)
    Label(registerGUI,text="제출기한",font=('맑은 고딕',10)).grid(row=3)
    Label(registerGUI,text="(YYYY.MM.DD HH:MM:SS)",font=('맑은 고딕',8)).grid(row=4)
    att_due = Entry(registerGUI,width=15)
    att_due.grid(row=3,column=1)
    Button(registerGUI,text = "출결 등록",width=10,font=('맑은 고딕',12),
    fg="black",bg="skyblue",command=partial(input_check,course_id,att_due,att_name,db,registerGUI)).grid(row=2,column=2,rowspan=2,padx=20)
    Label(registerGUI,text="\n출결 조회\n",font=('맑은 고딕',12)).grid(row=7,column=0)
    Button(registerGUI,text = "출결 조회",width=10,font=('맑은 고딕',12),
    fg="black",bg="tomato",command=partial(show_attlist,course_name,course_id,db)).grid(row=7,column=2,rowspan=2,padx=20)       
            
            