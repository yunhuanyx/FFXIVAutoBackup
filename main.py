import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmb
import createTask
import restoreBackup
import ctypes
import sys
import subprocess


class startInterface(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.setupUI()

    def setupUI(self):
        ttk.Label(self, text="").grid(row=0, column=1)
        #ttk.Label(self, text="").grid(row=0, column=2)
        ttk.Label(self, text="").grid(row=1, column=0)
        ttk.Button(root, text="创建计划", command=self.createT).grid(row=1, column=1, pady=15, padx=5)
        ttk.Button(root, text="从备份中恢复设置", command=self.restore).grid(row=1, column=3, pady=15, padx=5)
        ttk.Button(root, text="删除计划", command=self.deleteT).grid(row=1, column=5, pady=15, padx=5)
        ttk.Label(self, text="").grid(row=1, column=6)
        ttk.Label(self, text="").grid(row=2)

    def createT(self):
        createTask.createTaskSetUp()

    def deleteT(self):
        deleteTaskchoose()

    def restore(self):
        restoreBackup.restoreBackupSetup()


class deleteTaskchoose(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.resizable(width=0, height=0)
        self.title("删除计划")
        center_window(self, 350, 80)
        self.gowIntVar = tk.IntVar()
        self.deleteUI()

    def deleteUI(self):
        ttk.Label(self, text="需要删除的计划所属的服务器：").grid(row=0, column=0, padx=0, pady=10, sticky='e')
        ttk.Radiobutton(self, text="国服", variable=self.gowIntVar, value=1).grid(row=0, column=2)
        ttk.Radiobutton(self, text="国际服", variable=self.gowIntVar, value=2).grid(row=0, column=4)
        ttk.Button(self, text="确认", command=self.delete).grid(row=10, column=2)
        ttk.Button(self, text="取消", command=self.close).grid(row=10, column=4)

    def delete(self):
        if self.gowIntVar.get() == 1:
            taskName = "ff14backup-cn"
            if tkmb.askyesno("警告", message="确定删除计划？"):
                if subprocess.run("schtasks /delete /tn " + taskName + " /f", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode:
                    tkmb.showerror("错误", "所选服务器没有备份计划")
                else:
                    tkmb.showinfo("删除成功", "删除成功")
                    self.close()

        elif self.gowIntVar.get() == 2:
            taskName = "ffxivbackup-world"
            if tkmb.askyesno("警告", message="确定删除计划？"):
                if subprocess.run("schtasks /delete /tn " + taskName + " /f", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode:
                    tkmb.showerror("错误", "所选服务器没有备份计划")
                else:
                    tkmb.showinfo("删除成功", "删除成功")
                    self.close()
        else:
            tkmb.showerror(title="错误", message="请选择选项")

    def close(self):
        self.destroy()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def center_window(win, w, h):
    # 获取屏幕 宽、高
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))


def center_window_root(win, w, h):
    # 获取屏幕 宽、高
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws/2) - (w/2)
    y = (hs/2.5) - (h)
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))


if __name__ == "__main__":
    if is_admin():
        root = tk.Tk()
        root.title("FFXIVAutoBackup")
        root.resizable(width=0, height=0)
        center_window_root(root, 330, 60)
        startInterface(root).grid()
        root.mainloop()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 0)
        sys.exit(0)

