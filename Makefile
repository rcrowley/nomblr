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
	python manage.py build_solr_schema | sudo tee /etc/solr/conf/schema.xml >/dev/null

syncdb: createdb
	mv fixtures/initial_data.json fixtures/initial_data.json.sav || true
	python manage.py syncdb
	mv fixtures/initial_data.json.sav fixtures/initial_data.json

test:
	yes | python manage.py clear_index
	python manage.py test -s
	yes | python manage.py rebuild_index

.PHONY: all coverage createdb destroydb reindex run runserver schema syncdb test
