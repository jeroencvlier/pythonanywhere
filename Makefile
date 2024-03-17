# run a make pytest adn ignore deprecated warnings

.PHONY: test
test:
	poetry run pytest -v -W ignore::DeprecationWarning