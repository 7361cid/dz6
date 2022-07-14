SHELL=/bin/bash
prod:
	sudo apt install -y python3-pip
	sudo apt install -y python3-venv
	python3 -m venv env
	source env/bin/activate
	pip3 install -r requirements.txt
	export SECRET_KEY=django-insecure-@xi)m(s3f-s%dfh0#18%48e$$a%q_xn1#%z@4q8cq#cxne4-lk
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 -Xutf8 manage.py loaddata fixtures/dump.json
	python3 manage.py runserver
