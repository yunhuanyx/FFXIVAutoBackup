chcp 65001
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::myhope为保存备份的文件夹，不要在此文件夹中添加其他文件
set myhope="F:\Downloads\ff14\新建文件夹"

:: num为希望保存的备份个数
set num=2

::下文的用户名请替换成你自己的用户名

::请将 D:\最终幻想XIV\game\My Games\FINAL FANTASY XIV - A Realm Reborn 修改为你游戏目录中的此文件夹所在路径
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
set date=%date:~3,4%%date:~8,2%%date:~11,2%
if "%time:~0,2%" lss "10" (set time=0%time:~1,1%%time:~3,2%%time:~6,2%) else (set time=%time:~0,2%%time:~3,2%%time:~6,2%)
xcopy /e/y/i/f/q/v/h/s/k/exclude:C:\Users\用户名\Documents\FFXIVAutoBackup\exclude.txt "D:\最终幻想XIV\game\My Games\FINAL FANTASY XIV - A Realm Reborn" "%myhope%\%date%-%time%\FINAL FANTASY XIV - A Realm Reborn"
for /f "skip=%num%" %%i in ('dir /b /tc /o-d %myhope%') do rd /s /q %myhope%\%%i
exit