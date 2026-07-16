@echo off
schtasks /CREATE /SC ONSTART /TN "TelegramBotPoller" /TR "powershell.exe -NoProfile -ExecutionPolicy Bypass -File \"C:\Users\Admin\Documents\site\telegram-bot-poller.ps1\"" /RL HIGHEST /F
schtasks /RUN /TN "TelegramBotPoller"
echo Done.
pause
