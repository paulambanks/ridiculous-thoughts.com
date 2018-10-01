#!/usr/bin/env sh
set -ex
readonly ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

python3 "${ROOT}/src/manage.py" makemigrations accounts
python3 "${ROOT}/src/manage.py" migrate accounts
python3 "${ROOT}/src/manage.py" makemigrations website
python3 "${ROOT}/src/manage.py" migrate website
python3 "${ROOT}/src/manage.py" makemigrations
python3 "${ROOT}/src/manage.py" migrate
python3 "${ROOT}/src/manage.py" collectstatic --noinput