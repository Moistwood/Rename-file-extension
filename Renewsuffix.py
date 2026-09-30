
import os
from tkinter import Tk, Label, Entry, Button, Text, END, filedialog, messagebox


# 大写改小写
def diminish(s):
    res = ""
    for c in s:
        if ord(c) >= 65 and ord(c) <= 90:
            c = chr(ord(c) + 32)
        res = res + c
    return res


# 选文件夹
def choose():
    p = filedialog.askdirectory()
    if p != "":
        entry.delete(0, END)
        entry.insert(0, p)

#运行日志
def log(s):
    txt.insert(END, s + "\n")
    txt.see(END)
    root.update()      


def start():
    folder = entry.get()
    oldsuffix = diminish(entry_old.get())
    newsuffix = entry_new.get()

    if folder == "":
        messagebox.showinfo("tips", "先选一个文件夹")
        return
    if not os.path.exists(folder):
        log("找不到文件夹" )
        return
    if oldsuffix == "" or newsuffix == "":
        messagebox.showinfo("后缀不能空着")
        return

    all = []
    for dir_path, dir_names, file_names in os.walk(folder):
        for f in file_names:
            all.append(os.path.join(dir_path, f))

    need = []
    for old in all:
        if diminish(old).endswith(oldsuffix):
            need.append(old)

    if len(need) == 0:
        log("没找到要改的文件")
        return

    ans = messagebox.askyesno("找到 " + str(len(need)) + " 个文件，改吗？")
    if not ans:
        return

    co = 0
    for i in range(len(need)):
        old_path = need[i]
        d = os.path.dirname(old_path)
        old = os.path.basename(old_path)

        #切片改名
        new = old[:len(old) - len(oldsuffix)] + newsuffix
        new_path = os.path.join(d, new)

        try:
            os.rename(old_path, new_path)
        except Exception as e:
            log("这个没改成：" + old + "  " + str(e))
            continue

        log("改好了：" + old + " -> " + new)
        co = co + 1

    log("搞定！一共改了 " + str(co) + " 个文件")


root = Tk()
root.title("批量改后缀")
root.geometry("460x420")

Label(root, text="文件夹").grid(row=0, column=0, padx=8, pady=8, sticky="e")
entry = Entry(root, width=32)
entry.grid(row=0, column=1, padx=4, pady=8)
Button(root, text="浏览", width=6, command=choose).grid(row=0, column=2, padx=8, pady=8)

Label(root, text="原后缀").grid(row=1, column=0, padx=8, pady=4, sticky="e")
entry_old = Entry(root, width=32)
entry_old.insert(0, ".txt")
entry_old.grid(row=1, column=1, padx=4, pady=4, sticky="w")

Label(root, text="新后缀").grid(row=2, column=0, padx=8, pady=4, sticky="e")
entry_new = Entry(root, width=32)
entry_new.insert(0, ".md")
entry_new.grid(row=2, column=1, padx=4, pady=4, sticky="w")

Button(root, text="开始改名", width=12, command=start).grid(row=3, column=0, columnspan=3, pady=10)

txt = Text(root, height=12)
txt.grid(row=4, column=0, columnspan=3, padx=8, pady=8, sticky="nsew")

root.mainloop()
