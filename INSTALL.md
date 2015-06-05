mkvirtualenv glean
python manage.py syncdb --migrate
python manage.py runserver
