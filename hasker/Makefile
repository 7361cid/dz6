SHELL=/bin/bash
prod:
	sudo apt install -y python3-pip
	sudo apt install -y python3-venv
	python3 -m venv env
	source env/bin/activate
	pip3 install -r requirements.txt
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py loaddata fixtures/dump.json
	python3 manage.py runserver
