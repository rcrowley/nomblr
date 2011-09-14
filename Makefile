all:

coverage:
	yes | python manage.py clear_index
	python manage.py test -s --with-coverage --cover-package=nomblr
	yes | python manage.py rebuild_index

createdb:
	mysql -uroot -e"CREATE DATABASE IF NOT EXISTS nomblr CHARACTER SET utf8;"

destroydb:
	mysql -uroot -e"DROP DATABASE IF EXISTS nomblr;"

reindex:
	yes | python manage.py rebuild_index

run: runserver

runserver:
	python manage.py runserver 0.0.0.0:8000

schema:
	python manage.py build_solr_schema >schema.xml

syncdb:
	python manage.py syncdb

test:
	mv fixtures/initial_data.json.test-only fixtures/initial_data.json || true
	yes | python manage.py clear_index
	python manage.py test -s
	yes | python manage.py rebuild_index
	mv fixtures/initial_data.json fixtures/initial_data.json.test-only

.PHONY: all coverage createdb destroydb reindex run runserver schema syncdb test
