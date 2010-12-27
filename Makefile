all:

coverage:
	mv nomblr.index nomblr.index.sav || true
	python manage.py test -s --with-coverage --cover-package=nomblr
	rm -rf nomblr.index
	mv nomblr.index.sav nomblr.index || true

syncdb:
	rm -rf nomblr.db nomblr.index
	mv fixtures/initial_data.json fixtures/initial_data.json.sav
	python manage.py syncdb
	mv fixtures/initial_data.json.sav fixtures/initial_data.json

test:
	mv nomblr.index nomblr.index.sav || true
	python manage.py test -s
	rm -rf nomblr.index
	mv nomblr.index.sav nomblr.index || true

.PHONY: all coverage syncdb test
