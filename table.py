import sqlite3

def create_table(db_file):
    conn = sqlite3.connect(db_file, isolation_level=None)
    c = conn.cursor()
    sql_create_course_table = '''CREATE TABLE IF NOT EXISTS course(
    id integer PRIMARY KEY AUTOINCREMENT,
    course_name text NOT NULL)'''
    sql_create_assignment_table ='''CREATE TABLE IF NOT EXISTS assignment(
            id integer PRIMARY KEY AUTOINCREMENT,
            course_id integer NOT NULL,
            ass_content text NOT NULL,
            ass_due text NOT NULL,
            ass_complete integer DEFAULT 0,
            FOREIGN KEY(course_id)
            REFERENCES course(id))'''

    sql_create_attendance_table = '''CREATE TABLE IF NOT EXISTS attendance(
            id integer PRIMARY KEY AUTOINCREMENT,
            course_id integer NOT NULL,
            att_content text NOT NULL,
            att_due text NOT NULL,
            att_complete integer DEFAULT 0,
            FOREIGN KEY(course_id)
            REFERENCES course(id))'''
    sql_create_score_table = '''CREATE TABLE IF NOT EXISTS score(
            id integer PRIMARY KEY AUTOINCREMENT,
            course_id integer NOT NULL,
            score_content text NOT NULL,
            myscore integer NOT NULL,
            average integer NOT NULL,
            FOREIGN KEY(course_id)
            REFERENCES course(id))'''
    c.execute(sql_create_course_table)
    c.execute(sql_create_assignment_table)
    c.execute(sql_create_attendance_table)
    c.execute(sql_create_score_table)
    return c
