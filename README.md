# FFXIVAutoBackup
基于批处理文件和Windows任务计划的ff14自动备份设置文件程序

---
实现了**创建计划**、**删除计划**、**从备份结果中恢复设置到游戏设置文件**的功能

**支持FF14国服和国际服**


支持**Windows10 64位**，32位环境**未测试**，可能支持**Windows7**和**Windows11**（**均未测试**）

---
自动备份实现基于Windows任务计划。在不更换电脑和不重装系统的情况下，只需运行程序完成创建计划即可自动备份。
创建计划后可删除本程序，不影响备份的进行。删除程序后如需删除计划，可自行启动任务计划程序进行删除。


备份结果不包括截图文件，如需备份截图文件，请在创建计划后前往 **“C:\Users\用户名\Documents\FFXIVAutoBackup\exclude.txt”** 文件。
删除**exclude.txt**中的“**\\screenshots\\**”即可备份截图文件。

---
请勿随意修改 “C:\Users\用户名\Documents\FFXIVAutoBackup” 中**除“exclude.txt”之外**的文件，否则可能出现bug。


如有批处理文件和Windows任务计划程序使用经验，可前往 [FFXIVAutoBackup](https://github.com/yunhuanyx/FFXIVAutoBackup) 下载bat模板自行进行设置。

