import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb
from tkinter.filedialog import askdirectory
import getpass
import os
import json
import subprocess


gow = 0
path = ""
backupPath = ""


class restoreBackupSetup(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.resizable(width=0, height=0)
        self.title("恢复设置")
        center_window(self, 350, 80)
        self.gowIntVar = tk.IntVar()
        self.restoreUI()

    def restoreUI(self):
        ttk.Label(self, text="需要恢复的备份所属的服务器：").grid(row=0, column=0, padx=0, pady=10, sticky='e')
        ttk.Radiobutton(self, text="国服", variable=self.gowIntVar, value=1).grid(row=0, column=2)
        ttk.Radiobutton(self, text="国际服", variable=self.gowIntVar, value=2).grid(row=0, column=4)
        ttk.Button(self, text="下一步", command=self.next).grid(row=10, column=2)
        ttk.Button(self, text="取消", command=self.close).grid(row=10, column=4)

    def next(self):
        global gow
        gow = self.gowIntVar.get()
        if gow == 1 or gow == 2:
            self.close()
            restoreBackupPath()
        else:
            tkmb.showerror(title="错误", message="请选择选项")

    def close(self):
        self.destroy()


class restoreBackupPath(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.resizable(width=0, height=0)
        self.title("恢复设置")
        center_window(self, 480, 130)
        self.pathString = tk.StringVar()
        self.backupPathString = tk.StringVar()
        self.PathUI()

    def PathUI(self):
        user_name = getpass.getuser()
        global path
        global backupPath

        if gow == 1:
            try:
                f = open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\cn.json", "r")
                dict1 = json.load(f)

                path = dict1["FFXIV-cn"]
                backupPath = dict1["FFXIVbackup-cn"]
                self.pathString.set(path)
                self.backupPathString.set(backupPath)
                f.close()
            except:
                tkmb.showinfo("未找到设置", "未找到设置，请手动选取目录")
                '''with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\cn.json", "r") as f:
                dict = json.load(f)
                global path
                global backupPath
                path = dict["FFXIV-cn"]
                backupPath = dict["FFXIVbackup-cn"]'''
        elif gow == 2:
            '''with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\world.json", "r") as f:
                dict = json.load(f)
            global path
            global backupPath
            path = dict["FFXIV-world"]
            backupPath = dict["FFXIVbackup-world"]'''
            try:
                f = open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\world.json", "r")
                dict1 = json.load(f)
                path = dict1["FFXIV-world"]
                backupPath = dict1["FFXIVbackup-world"]
                self.pathString.set(path)
                self.backupPathString.set(backupPath)
                f.close()
            except:
                tkmb.showinfo("未找到设置", "未找到设置，请手动选取目录")

        ttk.Label(self, text="请选择游戏目录中的“FINAL FANTASY XIV - A Realm Reborn”文件夹:").grid(row=0, column=0, columnspan=3,
                                                                                 sticky='w')
        ttk.Entry(self, textvariable=self.pathString).grid(row=1, column=0, columnspan=3, ipadx=100, padx=10,
                                                           sticky='w')
        ttk.Button(self, text="路径选择", command=self.selectPath).grid(row=1, column=3)

        ttk.Label(self, text="请选择备份所在的文件夹:").grid(row=2, column=0, columnspan=3, sticky='w')
        ttk.Entry(self, textvariable=self.backupPathString).grid(row=3, column=0, columnspan=3, ipadx=100, padx=10,
                                                           sticky='w')
        ttk.Button(self, text="路径选择", command=self.selectBackupPath).grid(row=3, column=3)

        ttk.Button(self, text="下一步", command=self.select).grid(row=10, column=2)
        ttk.Button(self, text="取消", command=self.close).grid(row=10, column=3)

    def select(self):
        global path
        global backupPath
        path = self.pathString.get().replace('/', '\\')
        backupPath = self.backupPathString.get().replace('/', '\\')
        self.close()
        selectBackup()

    def selectPath(self):
        path_ = askdirectory()
        self.pathString.set(path_)

    def selectBackupPath(self):
        path_ = askdirectory()
        self.backupPathString.set(path_)

    def close(self):
        self.destroy()


class selectBackup(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.resizable(width=0, height=0)
        self.title("恢复设置")
        center_window(self, 240, 100)
        dbtype_list = os.listdir(backupPath)
        for dbtype in dbtype_list[::]:
            if os.path.isfile(os.path.join(backupPath, dbtype)):
                dbtype_list.remove(dbtype)
        self.backupName = ttk.Combobox(self, values=dbtype_list)
        self.selectUI()

    def selectUI(self):
        ttk.Label(self, text="请选择希望恢复的备份:").grid(row=0, column=1, columnspan=3, sticky='e')
        self.backupName.grid(row=1, column=2, columnspan=4)
        ttk.Label(self, text="").grid(row=2)
        ttk.Button(self, text="确定", command=self.confirm).grid(row=10, column=2)
        ttk.Button(self, text="取消", command=self.close).grid(row=10, column=4)

    def confirm(self):
        if tkmb.askyesno("确认", "确定恢复所选备份？"):
            pathb = backupPath + "\\" + self.backupName.get() + "\\FINAL FANTASY XIV - A Realm Reborn"
            command = "xcopy /e/y/i/f/q/v/h/s/k \"" + pathb + "\" \"" + path + "\""
            if subprocess.run(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                tkmb.showinfo("成功", "恢复成功")
            self.close()

    def close(self):
        self.destroy()


def center_window(win, w, h):
    # 获取屏幕 宽、高
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))
