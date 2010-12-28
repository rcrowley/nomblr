all:

coverage:
	python manage.py test -s --with-coverage --cover-package=nomblr

createdb:
	mysql -uroot -e"CREATE DATABASE IF NOT EXISTS nomblr CHARACTER SET utf8;"

destroydb:
	mysql -uroot -e"DROP DATABASE IF EXISTS nomblr;"

reindex:
	python manage.py rebuild_index

run: runserver

runserver:
	python manage.py runserver 0.0.0.0:8000

schema:
	python manage.py build_solr_schema | sudo tee /etc/solr/conf/schema.xml >/dev/null

syncdb: createdb
	mv fixtures/initial_data.json fixtures/initial_data.json.sav || true
	python manage.py syncdb
	mv fixtures/initial_data.json.sav fixtures/initial_data.json

test:
	python manage.py test -s

.PHONY: all coverage createdb destroydb reindex run runserver schema syncdb test
