@echo off
rem SSL renewal script for Windows

rem Log start time
(echo [%date% %time%] Starting SSL certificate renewal) >> renew_ssl.log

rem Run Certbot renewal (ensure Certbot is installed and in PATH)
certbot renew --post-hook "net stop FlaskApp && net start FlaskApp"

if %errorlevel% neq 0 (
    (echo [%date% %time%] Renewal failed) >> renew_ssl.log
) else (
    (echo [%date% %time%] Renewal succeeded) >> renew_ssl.log
)
