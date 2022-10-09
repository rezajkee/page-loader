[![Actions Status](https://github.com/rezajkee/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/rezajkee/python-project-lvl3/actions)
[![lint and test](https://github.com/rezajkee/python-project-lvl3/actions/workflows/lint%20and%20test.yml/badge.svg)](https://github.com/rezajkee/python-project-lvl3/actions/workflows/lint%20and%20test.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/36e50bc2d794e01b319f/maintainability)](https://codeclimate.com/github/rezajkee/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/36e50bc2d794e01b319f/test_coverage)](https://codeclimate.com/github/rezajkee/python-project-lvl3/test_coverage)

## Page loader

##### Третий учебный проект Hexlet

Данная утилита командной строки скачивает страницу и её локальные ресурсы из сети  
и кладет в указанную **существующую** директорию (по умолчанию в директорию запуска программы).  
По результату работы утилиты мы получаем html-страницу со ссылками на скачанные ресурсы.
```bash
usage: page-loader [-h] [-out OUTPUT] url_to_download

Page loader

positional arguments:
  url_to_download

optional arguments:
  -h, --help            show this help message and exit
  -out OUTPUT, --output OUTPUT
                        set path to the existing directory (current directory by default)
```

##### Пример работы пакета:
[![asciicast](https://asciinema.org/a/2pj1dRlYpfXI8dGkjDmehpL7I.svg)](https://asciinema.org/a/2pj1dRlYpfXI8dGkjDmehpL7I)

##### Для установки пакета с GitHub с помощью pip используйте
```bash
$ pip install git+https://github.com/rezajkee/python-project-lvl3.git
```

##### Для установки зависимостей используйте
```bash
$ make install
```