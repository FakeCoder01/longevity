#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.txt

celery -A longevity worker --loglevel=info