PYTHON := python3.8
ACTIVATE = . $(VENV)/bin/activate
INSTALL := pip install -Ur requirements.txt
VENV := venv
DELETE_TARGETS = $(VENV)

.PHONY : clean places/oneplace data weather/updated fsa/updated

data : fsa/updated weather/updated
	date >> data

places/oneplace:
	$(ACTIVATE); $(PYTHON) ninecat.py process-place; date >> places/oneplace

weather/updated:
	$(ACTIVATE); $(PYTHON) ninecat.py update-weather; date > weather/updated

fsa/updated:
	$(ACTIVATE); $(PYTHON) ninecat.py update-fsa; date > fsa/updated

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || $(PYTHON) -m venv $(VENV)
	$(ACTIVATE); $(INSTALL)
	touch venv/bin/activate

migrations:
	PYTHONPATH=. alembic revision --autogenerate

applymigrations:
	PYTHONPATH=. alembic upgrade head

stompmigrations:
	PYTHONPATH=. alembic stamp head

clean :
	rm -rf $(DELETE_TARGETS)
