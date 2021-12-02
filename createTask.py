import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb
from tkinter.filedialog import askdirectory
import getpass
import os
import json
import subprocess


gow = 0
backupNum = 0
path = ""
hopepath = ""
whennum = 0
when = ("每天", "每周", "每月", "计算机启动时", "用户登录时")
whenParameter = ["DAILY", "WEEKLY", "MONTHLY", "ONSTART", "ONLOGON"]
days = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
daysParameter = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
days_check = []
months = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
monthsParameter = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
months_check = []
#mday_check = []
monthNum = ["第一个", "第二个", "第三个", "第四个", "最后一个"]
monthNumParameter = ["FIRST", "SECOND", "THIRD", "FOURTH", "LAST"]
#mnum_check = []
#mw_check = []


class createTaskSetUp(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("创建新计划")
        self.resizable(width=0, height=0)
        center_window(self, 305, 120)
        self.gowIntVar = tk.IntVar()
        vcmd = (self.register(validate), '%P')
        self.backupNum = ttk.Entry(self, width=5, validate='key', validatecommand=vcmd)
        self.setupUI()

    def setupUI(self):
        ttk.Label(self, text="需要备份的服务器：").grid(row=0, column=0, padx=0, pady=10, sticky='e')
        ttk.Radiobutton(self, text="国服", variable=self.gowIntVar, value=1).grid(row=0, column=2)
        ttk.Radiobutton(self, text="国际服", variable=self.gowIntVar, value=2).grid(row=0, column=4)
        ttk.Label(self, text="需要保存的备份个数：").grid(row=1, column=0, padx=0, pady=10, sticky='e')
        self.backupNum.grid(row=1, column=2)
        self.gowIntVar.set(gow)
        #self.backupNum.
        ttk.Button(self, text="下一步", command=self.path).grid(row=10, column=2)
        ttk.Button(self, text="取消", command=self.close).grid(row=10, column=4)

    def path(self):
        global gow
        gow = self.gowIntVar.get()
        global backupNum

        if gow == 0:
            tkmb.showerror(title="错误", message="请选择服务器")
        elif gow == 1 or gow == 2:
            try:
                backupNum = int(self.backupNum.get())
                if backupNum == 0:
                    tkmb.showerror(title="错误", message="备份个数不能为0")
                else:
                    self.destroy()
                    createTaskPath()
            except ValueError:
                tkmb.showerror(title="错误", message="请输入需要保存的备份个数")

    def close(self):
        self.destroy()


class createTaskPath(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("创建新计划")
        self.resizable(width=0, height=0)
        center_window(self, 520, 220)
        self.pathString = tk.StringVar()
        self.hopePathString = tk.StringVar()
        self.pathUI()

    def pathUI(self):
        ttk.Label(self, text="请选择“FINAL FANTASY XIV - A Realm Reborn”文件夹:").grid(row=0, column=0, columnspan=3, sticky='w')
        ttk.Label(self, text="例：D:\\最终幻想XIV\\game\\My Games\\FINAL FANTASY XIV - A Realm Reborn").grid(row=2, column=0, columnspan=4, sticky='w')
        ttk.Label(self, text="国际服为：C:\\Users\\用户名\\Documents\\My Games\\FINAL FANTASY XIV - A Realm Reborn").grid(row=3, column=0, columnspan=4, sticky='w')

        self.pathString.set(path)
        self.hopePathString.set(hopepath)

        if gow == 2:
            user_name = getpass.getuser()
            self.pathString.set("C:\\Users\\" + user_name + "\\Documents\\My Games\\FINAL FANTASY XIV - A Realm Reborn")

        ttk.Entry(self, textvariable=self.pathString).grid(row=1, column=0, columnspan=3, ipadx=100, padx=10, sticky='w')
        ttk.Button(self, text="路径选择", command=self.selectPath).grid(row=1, column=3)
        ttk.Label(self, text="").grid(row=4, column=0)
        ttk.Label(self, text="希望备份保存在(请选择空文件夹):").grid(row=5, column=0, columnspan=3, sticky='w')
        ttk.Entry(self, textvariable=self.hopePathString).grid(row=6, column=0, columnspan=3, ipadx=100, padx=10, sticky='w')
        ttk.Button(self, text="路径选择", command=self.selectHopePath).grid(row=6, column=3)
        ttk.Label(self, text="").grid(row=7, column=0)
        ttk.Button(self, text="上一步", command=self.backsetup).grid(row=10, column=1)
        ttk.Button(self, text="下一步", command=self.cycle).grid(row=10, column=2)
        ttk.Button(self, text="取消", command=self.close).grid(row=10, column=3)

    def backsetup(self):
        self.destroy()
        createTaskSetUp()

    def selectPath(self):
        path_ = askdirectory()
        self.pathString.set(path_)

    def selectHopePath(self):
        path_ = askdirectory()
        self.hopePathString.set(path_)

    def cycle(self):
        if self.pathString.get() == "" or self.hopePathString.get() == "":
            tkmb.showerror(title="错误", message="请选择文件夹")
        else:
            global path
            path = self.pathString.get().replace("/", "\\")
            global hopepath
            hopepath = self.hopePathString.get().replace("/", "\\")
            self.destroy()
            createTaskCycle()

    def close(self):
        self.destroy()


class createTaskCycle(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("创建新计划")
        center_window(self, 305, 260)
        self.hIntVar = tk.IntVar()
        self.resizable(width=0, height=0)
        self.cycleUI()

    def cycleUI(self):
        ttk.Label(self, text="希望任务何时开始？").grid(row=0, column=1, pady=10, sticky='w')
        i = 1
        for t in when:
            ttk.Radiobutton(self, text=t, variable=self.hIntVar, value=i).grid(row=i, column=1, pady=5, sticky='w')
            i += 1
        self.hIntVar.set(whennum)
        ttk.Button(self, text="上一步", command=self.backpath).grid(row=10, column=0, padx=5)
        ttk.Button(self, text="下一步", command=self.frequency).grid(row=10, column=1, padx=5)
        ttk.Button(self, text="取消", command=self.close).grid(row=10, column=2, padx=5)

    def backpath(self):
        self.destroy()
        createTaskPath()

    def frequency(self):
        global whennum
        whennum = self.hIntVar.get()

        user_name = getpass.getuser()
        backupBat = """chcp 65001
set myhope=\"""" + hopepath + "\"" + """
set num=""" + str(backupNum) + """
set date=%date:~3,4%%date:~8,2%%date:~11,2%
if "%time:~0,2%" lss "10" (set time=0%time:~1,1%%time:~3,2%%time:~6,2%) else (set time=%time:~0,2%%time:~3,2%%time:~6,2%)
xcopy /e/y/i/f/q/v/h/s/k/exclude:""" + "C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\" + """exclude.txt \"""" + path + """\" \"%myhope%\\%date%-%time%\\FINAL FANTASY XIV - A Realm Reborn\"
for /f \"skip=%num%\" %%i in ('dir /b /tc /o-d %myhope%') do rd /s /q %myhope%\\%%i
exit
"""

        if not os.path.isdir("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup"):
            os.makedirs("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup")

        if gow == 1:
            dict = {"FFXIV-cn": path, "FFXIVbackup-cn": hopepath}
            with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\cn.json", 'w') as fd:
                json.dump(dict, fd, ensure_ascii=False)
        elif gow == 2:
            dict = {"FFXIV-world": path, "FFXIVbackup-world": hopepath}
            with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\world.json", 'w') as fd:
                json.dump(dict, fd, ensure_ascii=False)

        with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\exclude.txt", "w") as ex:
            ex.write("""\\log\\
\\screenshots\\""")
            ex.close()
        if whennum == 0:
            tkmb.showerror(title="错误", message="请选择选项")
        elif whennum == 4 or whennum == 5:
            if tkmb.askyesnocancel("确认", message="确定按所选选项执行？"):
                if gow == 1:
                    batName = "ff14backup-cn"
                elif gow == 2:
                    batName = "ffxivbackup-world"

                with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\" + batName + ".bat", "w",
                          encoding="UTF-8") as f:
                    f.write(backupBat)
                    f.close()
                with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\" + batName + ".vbs", "w",
                          encoding="UTF-8") as hw:
                    hw.write("""set ws=WScript.CreateObject(\"WScript.Shell\")
ws.Run \"""" + "C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\" + batName + ".bat\",0")
                    hw.close()

                subprocess.run("schtasks /delete /tn " + batName + " /f", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                backupTask = "schtasks /create /tn " + batName + " /tr " \
                             + "C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\" + batName + ".vbs /sc " \
                             + whenParameter[whennum - 1]

                if subprocess.run(backupTask, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                    tkmb.showinfo("完成", "创建任务计划成功")
                    self.close()
                else:
                    tkmb.showerror("错误", "创建任务计划失败，请重试")

        else:
            self.close()
            createTaskFrequency()

    def close(self):
        self.destroy()


class createTaskFrequency(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("创建新计划")
        self.resizable(width=0, height=0)
        center_window(self, 850, 240)
        vcmd = (self.register(validate), '%P')
        self.everynday = ttk.Entry(self, width=5, validate='key', validatecommand=vcmd)
        self.everynweek = ttk.Entry(self, width=5, validate='key', validatecommand=vcmd)
        self.flagd = 0
        self.flagw = 0
        self.md = ttk.Frame(self)
        self.mw = ttk.Frame(self)
        self.v = tk.IntVar()
        self.mdayIntVar = tk.IntVar()
        self.mnumIntVar = tk.IntVar()
        self.dayIntVar = tk.IntVar()
        self.tian = ttk.Radiobutton(self, text="天:", variable=self.v, command=self.mond, value=1)
        self.zai = ttk.Radiobutton(self, text="在:", variable=self.v, command=self.monw, value=2)
        self.frequencyUI()

    def frequencyUI(self):
        if whennum == 1:
            #ttk.Label(self, text="每隔").grid(row=0, column=0, sticky='e', pady=10)
            #self.everynday.grid(row=0, column=1, pady=10)
            #ttk.Label(self, text="天发生一次").grid(row=0, column=2, sticky='w', pady=10)
            ttk.Label(self, text="每隔").place(x=350, y=100)
            self.everynday.place(x=400, y=100)
            ttk.Label(self, text="天发生一次").place(x=450, y=100)
        elif whennum == 2:
            #ttk.Label(self, text="每隔").grid(row=0, column=0, sticky='e', pady=10)
            #self.everynweek.grid(row=0, column=1)
            #ttk.Label(self, text="周：").grid(row=0, column=2, sticky='w', pady=10)
            ttk.Label(self, text="每隔").place(x=350, y=20)
            self.everynweek.place(x=400, y=20)
            ttk.Label(self, text="周：").place(x=450, y=20)
            global days_check
            for day in days:
                days_check.append(tk.IntVar())
                if len(days_check) <= 4:
                    #ttk.Checkbutton(self, text=day, variable=days_check[-1]).grid(row=1, column=len(days_check)-1, padx=5, pady=5)
                    ttk.Checkbutton(self, text=day, variable=days_check[-1]).place(x=260+(len(days_check)-1)*100, y=50)
                else:
                    #ttk.Checkbutton(self, text=day, variable=days_check[-1]).grid(row=2, column=len(days_check)-5, padx=5, pady=5)
                    ttk.Checkbutton(self, text=day, variable=days_check[-1]).place(x=260+(len(days_check)-5)*100, y=80)
        elif whennum == 3:
            ttk.Label(self, text="月:").grid(row=0, column=0, sticky='e')
            global months_check
            for month in months:
                months_check.append(tk.IntVar())
                if len(months_check) <= 6:
                    ttk.Checkbutton(self, text=month, variable=months_check[-1]).grid(row=1, column=len(months_check)-1, padx=2, pady=2, sticky='w')
                else:
                    ttk.Checkbutton(self, text=month, variable=months_check[-1]).grid(row=2, column=len(months_check)-7, padx=2, pady=2, sticky='w')

            self.tian.grid(row=3, column=0, sticky='e')
            self.zai.grid(row=7, column=0, sticky='e')

        #ttk.Button(self, text="上一步", command=self.backcycle).grid(row=10, column=12)
        #ttk.Button(self, text="完成", command=self.finish).grid(row=10, column=13)
        #ttk.Button(self, text="取消", command=self.close).grid(row=10, column=14)
        ttk.Button(self, text="上一步", command=self.backcycle).place(y=200, x=550)
        ttk.Button(self, text="完成", command=self.finish).place(y=200, x=650)
        ttk.Button(self, text="取消", command=self.close).place(y=200, x=750)

    def mond(self):
        self.mw.grid_forget()
        self.md.grid(row=4, columnspan=11)
        if self.flagd == 0:
            #global mday_check
            for i in range(1, 32):
                #mday_check.append(tk.IntVar())
                if i <= 10:
                    ttk.Radiobutton(self.md, text=i, variable=self.mdayIntVar, value=i).grid(row=4, column=i - 1, padx=8, pady=3, sticky='w')
                elif i <= 20:
                    ttk.Radiobutton(self.md, text=i, variable=self.mdayIntVar, value=i).grid(row=5, column=i - 11, padx=8, pady=3, sticky='w')
                elif i:
                    ttk.Radiobutton(self.md, text=i, variable=self.mdayIntVar, value=i).grid(row=6, column=i - 21, padx=8, pady=3, sticky='w')
            self.flagd = 1

    def monw(self):
        self.md.grid_forget()
        self.mw.grid(row=8, columnspan=7)
        if self.flagw == 0:
            #global mnum_check
            i = 1
            for mnum in monthNum:
                #mnum_check.append(tk.IntVar())
                ttk.Radiobutton(self.mw, text=mnum, variable=self.mnumIntVar, value=i).grid(row=8, column=i-1, padx=8, pady=3, sticky='w')
            #global days_check
                i += 1
            i = 1
            for day in days:
                #days_check.append(tk.IntVar())
                ttk.Radiobutton(self.mw, text=day, variable=self.dayIntVar, value=i).grid(row=9, column=i-1, padx=8, pady=3, sticky='w')
                i += 1

            self.flagw = 1

    def backcycle(self):
        self.close()
        createTaskCycle()

    def finish(self):
        user_name = getpass.getuser()
        backupBat = """chcp 65001
set myhope=\"""" + hopepath + "\"" + """
set num=""" + str(backupNum) + """
set date=%date:~3,4%%date:~8,2%%date:~11,2%
if "%time:~0,2%" lss "10" (set time=0%time:~1,1%%time:~3,2%%time:~6,2%) else (set time=%time:~0,2%%time:~3,2%%time:~6,2%)
xcopy /e/y/i/f/q/v/h/s/k/exclude:""" + "C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\" + """exclude.txt \"""" + path + """\" \"%myhope%\\%date%-%time%\\FINAL FANTASY XIV - A Realm Reborn\"
for /f \"skip=%num%\" %%i in ('dir /b /tc /o-d %myhope%') do rd /s /q %myhope%\\%%i
exit
"""
        if not os.path.isdir("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup"):
            os.makedirs("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup")

        with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\exclude.txt", "w") as ex:
            ex.write("""\\log\\
\\screenshots\\""")
            ex.close()

        if gow == 1:
            dict = {"FFXIV-cn": path, "FFXIVbackup-cn": hopepath}
            with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\cn.json", 'w') as fd:
                json.dump(dict, fd, ensure_ascii=False)
        elif gow == 2:
            dict = {"FFXIV-world": path, "FFXIVbackup-world": hopepath}
            with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\world.json", 'w') as fd:
                json.dump(dict, fd, ensure_ascii=False)

        if whennum == 1:
            if self.everynday.get() == '':
                tkmb.showerror(title="错误", message="请填写空位")
            else:
                if tkmb.askyesnocancel("确认", message="确定按所选选项执行？"):
                    if gow == 1:
                        batName = "ff14backup-cn"
                    elif gow == 2:
                        batName = "ffxivbackup-world"

                    with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\"+batName+".bat", "w",
                          encoding="UTF-8") as f:
                        f.write(backupBat)
                        f.close()
                    with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\"+batName+".vbs", "w",
                          encoding="UTF-8") as hw:
                        hw.write("""set ws=WScript.CreateObject(\"WScript.Shell\")
ws.Run \""""+"C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\"+batName+".bat\",0")
                        hw.close()

                    #os.system("schtasks /delete /tn " + batName + " /f")
                    subprocess.run("schtasks /delete /tn " + batName + " /f", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
                    backupTask = "schtasks /create /tn " + batName + " /tr " \
                                 + "C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\" + batName + ".vbs /sc "\
                                 + whenParameter[whennum - 1] + " /mo " + self.everynday.get()
                    if subprocess.run(backupTask, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                        tkmb.showinfo("完成", "创建任务计划成功")
                        self.close()
                    else:
                        tkmb.showerror("错误", "创建任务计划失败，请重试")

        elif whennum == 2:
            if self.everynweek.get() == '' or (traverse(days_check) is False):
                tkmb.showerror(title="错误", message="请填写空位或选择选项")
            else:
                if tkmb.askyesnocancel("确认", message="确定按所选选项执行？"):
                    if gow == 1:
                        batName = "ff14backup-cn"
                    elif gow == 2:
                        batName = "ffxivbackup-world"

                    with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\"+batName+".bat", "w",
                          encoding="UTF-8") as f:
                        f.write(backupBat)
                        f.close()
                    with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\"+batName+".vbs", "w",
                          encoding="UTF-8") as hw:
                        hw.write("""set ws=WScript.CreateObject(\"WScript.Shell\")
ws.Run \""""+"C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\"+batName+".bat\",0")
                        hw.close()

                    daysStr = ""
                    for i in range(0, len(days_check)):
                        if days_check[i].get() == 1:
                            daysStr += daysParameter[i] + ","
                    daysStr = daysStr[:-1]

                    #os.system("schtasks /delete /tn " + batName + " /f")
                    subprocess.run("schtasks /delete /tn " + batName + " /f", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
                    backupTask = "schtasks /create /tn " + batName + " /tr " \
                                 + "C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\" + batName + ".vbs /sc "\
                                 + whenParameter[whennum - 1] + " /mo " + self.everynweek.get() + " /d " + daysStr

                    if subprocess.run(backupTask, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                        tkmb.showinfo("完成", "创建任务计划成功")
                        self.close()
                    else:
                        tkmb.showerror("错误", "创建任务计划失败，请重试")

        elif whennum == 3:
            if not traverse(months_check):
                tkmb.showerror(title="错误", message="请选择选项")
            elif self.v.get() == 1:
                if self.mdayIntVar.get() < 1 or self.mdayIntVar.get() > 31:
                    tkmb.showerror(title="错误", message="请选择选项")
                else:
                    if tkmb.askyesnocancel("确认", message="确定按所选选项执行？"):
                        if gow == 1:
                            batName = "ff14backup-cn"
                        elif gow == 2:
                            batName = "ffxivbackup-world"

                        with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\"+batName+".bat", "w",
                            encoding="UTF-8") as f:
                            f.write(backupBat)
                            f.close()
                        with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\"+batName+".vbs", "w",
                            encoding="UTF-8") as hw:
                            hw.write("""set ws=WScript.CreateObject(\"WScript.Shell\")
ws.Run \""""+"C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\"+batName+".bat\",0")
                            hw.close()

                        monthsStr = ""
                        for i in range(0, len(months_check)):
                            if months_check[i].get() == 1:
                                monthsStr += monthsParameter[i] + ","
                        monthsStr = monthsStr[:-1]

                        '''dayStr = ""
                    for i in range(0, len(mday_check)):
                        if mday_check[i].get() == 1:
                            dayStr += str(i+1) + ","
                    dayStr = dayStr[:-1]
                    print(dayStr)'''

                        #os.system("schtasks /delete /tn " + batName + " /f")
                        subprocess.run("schtasks /delete /tn " + batName + " /f", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
                        backupTask = "schtasks /create /tn " + batName + " /tr " \
                                    + "C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\" + batName + ".vbs /sc "\
                                    + whenParameter[whennum - 1] + " /m " + monthsStr + " /d " + str(self.mdayIntVar.get())

                        if subprocess.run(backupTask, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                            tkmb.showinfo("完成", "创建任务计划成功")
                            self.close()
                        else:
                            tkmb.showerror("错误", "创建任务计划失败，请重试")

            elif self.v.get() == 2:
                if self.mnumIntVar.get() < 1 or self.mnumIntVar.get() > 5 or self.dayIntVar.get() < 1 or self.dayIntVar.get() > 7:
                    tkmb.showerror(title="错误", message="请选择选项")
                else:
                    if tkmb.askyesnocancel("确认", message="确定按所选选项执行？"):
                        if gow == 1:
                            batName = "ff14backup-cn"
                        elif gow == 2:
                            batName = "ffxivbackup-world"

                        with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\"+batName+".bat", "w",
                            encoding="UTF-8") as f:
                            f.write(backupBat)
                            f.close()
                        with open("C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\"+batName+".vbs", "w",
                            encoding="UTF-8") as hw:
                            hw.write("""set ws=WScript.CreateObject(\"WScript.Shell\")
ws.Run \""""+"C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\"+batName+".bat\",0")
                            hw.close()

                        monthsStr = ""
                        for i in range(0, len(months_check)):
                            if months_check[i].get() == 1:
                                monthsStr += monthsParameter[i] + ","
                        monthsStr = monthsStr[:-1]


                        '''dayStr = ""
                    for i in range(0, len(mday_check)):
                        if mday_check[i].get() == 1:
                            dayStr += str(i+1) + ","
                    dayStr = dayStr[:-1]
                    print(dayStr)'''

                        #os.system("schtasks /delete /tn " + batName + " /f")
                        subprocess.run("schtasks /delete /tn " + batName + " /f", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
                        backupTask = "schtasks /create /tn " + batName + " /tr " \
                                    + "C:\\Users\\" + user_name + "\\Documents\\FFXIVAutoBackup\\" + batName + ".vbs /sc "\
                                    + whenParameter[whennum - 1] + " /m " + monthsStr \
                                    + " /d " + daysParameter[self.dayIntVar.get()-1] \
                                    + " /mo " + monthNumParameter[self.mnumIntVar.get()-1]

                        if subprocess.run(backupTask, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                            tkmb.showinfo("完成", "创建任务计划成功")
                            self.close()
                        else:
                            tkmb.showerror("错误", "创建任务计划失败，请重试")

            else:
                tkmb.showerror(title="错误", message="请选择选项")

    def close(self):
        self.destroy()
        global days_check
        days_check.clear()
        global months_check
        months_check.clear()
        #global mday_check
        #mday_check.clear()
        #global mnum_check
        #mnum_check.clear()
        #global mw_check
        #mw_check.clear()


def validate(content):
    if content.isdigit() or content == "":
        return True
    else:
        return False


def traverse(nlist):
    for i in nlist:
        if i.get() == 1:
            return True
    return False


def center_window(win, w, h):
    # 获取屏幕 宽、高
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))
