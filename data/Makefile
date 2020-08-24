PYTHON := python3.8
ACTIVATE = . $(VENV)/bin/activate
INSTALL := pip install -Ur requirements.txt
VENV := venv
DELETE_TARGETS = $(VENV)

.PHONY : clean

data : fsa/updated

fsa/updated:
	$(ACTIVATE); $(PYTHON) ninecat.py update-fsa; date > fsa_updated

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || $(PYTHON) -m venv $(VENV)
	$(ACTIVATE); $(INSTALL)
	touch venv/bin/activate

clean :
	rm -rf $(DELETE_TARGETS)
