@echo off

REM 检查网络连接状态
ping www.baidu.com -n 1 > nul

REM 如果ping命令返回错误级别为0，表示有网络连接
IF %errorlevel% EQU 0 (
    REM 在此处执行你的Python脚本命令，并将输出结果保存到文本文件中
    "C:\Code\Miniconda\python" "C:\CodeFile\PycharmProjects\TestProjects\LPLANDLCK_Matches\GUI.py"
) ELSE (
    REM 如果没有网络连接，可以执行其他操作或等待一段时间后重试
    echo 没有网络连接，无法执行命令。
)

REM 暂停一段时间后关闭窗口
REM timeout /t 5

exit