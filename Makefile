# Makefile

build: # собрать пакет
	poetry build


package-install: # установка пакета из ОС (запускать из корня проекта)
	python3 -m pip install --user --force-reinstall  dist/*.whl


lint: # запуск линтера (flake8)
	poetry run flake8 page_loader


test: # запуск pytest
	poetry run pytest


test-coverage: # запись покрытия для CodeClimate
	poetry run pytest --cov=page_loader --cov-report xml


local-test-coverage: # проверка покрытия тестами
	poetry run pytest --cov=page_loader