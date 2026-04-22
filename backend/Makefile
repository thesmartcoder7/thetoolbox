run:
	@python3 manage.py runserver 0.0.0.0:8000

migrations:
	@python manage.py makemigrations && python manage.py migrate

superuser:
	@python manage.py createsuperuser

checklist:
	@python manage.py check --deploy

active:
	@chmod +x activate.py && ./activate.py

requirements:
	@pip freeze > requirements.txt

dependencies:
	@pip install -r requirements.txt
