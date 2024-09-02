
set -e

poetry install --no--root
poetry run flask --app flaksr.app db upgrade
poetry run gunicorn flaskr.wsgi:app
