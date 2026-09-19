TaskFlow - kibhabe chalabe (Windows PowerShell)

1) Project folder e jao:
     cd "E:\Django Project\TaskFlow"

2) Notun virtual environment banao (purono venv ta delete kore dite paro) ebong activate koro:
     python -m venv venv
     venv\Scripts\activate

3) Django ar baki package install koro:
     pip install -r requirements.txt

4) Database ready koro (notun migration nei, tobu safe):
     python manage.py migrate

5) Server chalao:
     python manage.py runserver

6) Browser e kholo: http://127.0.0.1:8000/
   Login na thakle auto login page e niye jabe.

Kichu lagle:
   python manage.py createsuperuser     (admin: /admin/)
   python manage.py test                (15 ta test)
