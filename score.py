
import sqlite3    
from tkinter import *
from functools import partial
from tkinter import messagebox
def add_score(course_id,score_name,avg_score,my_score,db,registerGUI):
    score_name = score_name.get()
    avg_score = avg_score.get()
    my_score = my_score.get()
    data = [course_id,score_name,my_score,avg_score]
    sql = '''INSERT INTO score (course_id,score_content,myscore,average) VALUES (?,?,?,?)'''
    db.execute(sql,data)
    messagebox.showinfo('등록완료',f'[{score_name}] 성적 등록 완료!!')
    registerGUI.destroy()

def show_scorelist(course_name,course_id,db,registerGUI):
    scorelistGUI = Tk()
    scorelistGUI.title(f'수강과목 : {course_name}')
    scorelistGUI.geometry('400x400')
    msg = f"{course_name} 성적 리스트\n"
    Label(scorelistGUI,text=msg,font=('맑은 고딕',14)).pack()
    
    scores = db.execute("SELECT * FROM score WHERE course_id=:ID",{"ID":course_id})
    cnt = 0
    myscore = 0
    avgscore = 0
    for score in scores:
        msg = f"{score[2]} : 내 성적 : {score[3]} / 평균 성적 : {score[4]}"
        label_list = Label(scorelistGUI,text=msg,font=('맑은 고딕',12))
        label_list.config(anchor=CENTER)
        label_list.pack()
        cnt+=1
        myscore+=float(score[3])
        avgscore+=float(score[4])
    if cnt!=0 : 
        myscore /= cnt
        avgscore /= cnt
    msg = f"\n[ 총 성적 현황(평균) ]\n내 성적 : {myscore:.2f} / 평균 성적 : {avgscore:.2f}\n"
    Label(scorelistGUI,text=msg,font=('맑은 고딕',12)).pack()
    Button(scorelistGUI,text = "종료",width=12,font=('맑은 고딕',12),fg='white',
    bg="tomato",command=scorelistGUI.destroy).pack(side=BOTTOM,pady=10)

def handle_score(course_name,course_id,db):
    registerGUI = Tk()
    registerGUI.title(f'수강과목 : {course_name}')
    registerGUI.geometry('365x200')
    Label(registerGUI,text="\n성적 등록",font=('맑은 고딕',12)).grid(row=1,column=0)
    Label(registerGUI,text="과제 / 시험 내용",font=('맑은 고딕',10)).grid(row=2)
    score_name = Entry(registerGUI,width=15)
    score_name.grid(row=2,column=1)
    Label(registerGUI,text="내 성적",font=('맑은 고딕',10)).grid(row=3)
    my_score = Entry(registerGUI,width=15)
    my_score.grid(row=3,column=1)
    Label(registerGUI,text="평균성적",font=('맑은 고딕',10)).grid(row=4)
    avg_score = Entry(registerGUI,width=15)
    avg_score.grid(row=4,column=1)
    Button(registerGUI,text = "성적 등록",width=10,font=('맑은 고딕',12),
    fg="black",bg="skyblue",command=partial(add_score,course_id,score_name,avg_score,my_score,db,registerGUI)).grid(row=2,column=2,rowspan=3,padx=20)
    Label(registerGUI,text="\n성적 조회\n",font=('맑은 고딕',12)).grid(row=7,column=0)
    Button(registerGUI,text = "성적 조회",width=10,font=('맑은 고딕',12),
    fg="black",bg="tomato",command=partial(show_scorelist,course_name,course_id,db,registerGUI)).grid(row=7,column=2,rowspan=2,padx=20)             
            
            