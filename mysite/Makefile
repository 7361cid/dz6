SHELL=bin/bash
prod:
    sudo apt install -y python3-pip
    sudo apt install -y python3-venv
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
