# Makefile

install: # выполнить установку зависимостей
	poetry install


build: # собрать пакет
	poetry build


package-install: # установка пакета из ОС (запускать из корня проекта)
	python3 -m pip install --user --force-reinstall  dist/*.whl


lint: # запуск линтера (flake8)
	poetry run flake8 page_loader ;\
	poetry run flake8 tests


test: # запуск pytest
	poetry run pytest


test-coverage: # запись покрытия для CodeClimate
	poetry run pytest --cov=page_loader --cov-report xml


local-test-coverage: # проверка покрытия тестами
	poetry run pytest --cov=page_loader


coverage-report: # запись покрытия в html-формате
	poetry run pytest --cov=page_loader --cov-report html


isort: # запуск isort
	poetry run isort page_loader ;\
	poetry run isort tests


black: # запуск black
	poetry run black page_loader ;\
	poetry run black tests