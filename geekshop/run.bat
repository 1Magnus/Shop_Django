@ECHO OFF
start cmd.exe /C "python manage.py runserver && cd F:\Project\geekshop\geekshop && F:"
start "C:\Program Files\Google\Chrome\Application\chrome.exe" "http://127.0.0.1:8000/"