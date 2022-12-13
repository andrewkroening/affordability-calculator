install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C,unsubscriptable-object,anomalous-backslash-in-string --extension-pkg-whitelist='pydantic' *.py ./logic/*.py

format:
	black *.py ./logic/*.py

all: install lint format
