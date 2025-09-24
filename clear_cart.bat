@echo off
cd /d C:\Users\Hp\Desktop\g\Ecommerce Website\ecommerce
call C:\Users\Hp\Desktop\g\Ecommerce Website\myenv\Scripts\activate.bat
python manage.py clear_cart >> cart_cleanup.log 2>&1
