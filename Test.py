import pyperclip
from tkinter import *
import pymysql


host = ''
user = ''
pwd = ''
dbName = ''


def onGoTable():

    db = pymysql.connect(host,
                         user, pwd, dbName)

    try:
        t.delete(0.0, END)
        newVar = pyperclip.paste()
        tableName = ''
        for c in newVar:
            if c.isupper():
                tableName = str(tableName) + '_' + str(c)
            else:
                tableName = str(tableName) + str(c)
        print(tableName)
        t.insert(END, "查询的表名为" + tableName + "\n")
        sql = "show create table " + tableName
        cursor = db.cursor()
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchone()

        if len(results) > 0:
            data = results[1]
            t.insert(END, data)
        else:
            t.insert(END, "查询无记录")
    except Exception as e:
        t.insert(END, "查询出错，错误信息为："+ str(e))
    finally:
        db.close()

def onGoName():

    db = pymysql.connect(host,
                         user, pwd, dbName)

    try:
        t.delete(0.0, END)
        key = ''
        newVar = pyperclip.paste()
        for c in newVar:
            if c.isupper():
                if key == '':
                    key = key + c.lower()
                else:
                    key = str(key) + '_' + str(c.lower())
            else:
                key = str(key) + str(c)
        t.insert(END, "查询的字段为"+ key + "\n")
        sql = "select table_name,column_comment from information_schema.columns where column_name = '%s'" % (key)
        cursor = db.cursor()
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        data = ''
        if len(results) > 0:
            for res in results:
                data = data + "表名为 ： " + res[0] + " ; 字段含义 ：" + res[1] + "\n"
            t.insert(END, data)
        else:
            t.insert(END, "查询无记录")
    except Exception as e:
        t.insert(END, "查询出错，错误信息为：" + str(e))
    finally:
        db.close()

if __name__ == '__main__':

        f = open("db.txt")
        host = (f.readline().split("="))[1].strip("\n")
        user = (f.readline().split("="))[1].strip("\n")
        pwd = (f.readline().split("="))[1].strip("\n")
        dbName = (f.readline().split("="))[1].strip("\n")
        f.close()
        root = Tk()
        t = Text(root,width=120,height=50)
        t.pack()
        goBtn = Button(text="表名!", command=onGoTable)
        goBtn1 = Button(text="字段名!", command=onGoName)
        goBtn.pack()
        goBtn1.pack()
        root.mainloop()
