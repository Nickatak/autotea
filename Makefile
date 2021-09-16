.PHONY: lint
lint:
	pipenv run black ./
.PHONY: test
test:
	pipenv run pytest tests/