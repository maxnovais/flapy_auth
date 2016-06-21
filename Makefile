SHELL=/bin/bash
.DEFAULT_GOAL=unit

clean:
	@find . -iname '*.py[co]' -delete
	@find . -name '__pycache__' -prune | xargs rm -rf # clean __pycache__ dirs build by py.test

coverage:
	PYTHONPATH=. py.test tests/unit --cov-report=html --cov=elflapy $(ARGS)

unit:
	PYTHONPATH=. py.test tests/unit $(ARGS)
