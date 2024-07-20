from iu_subhouse.api import *


def start_dev():
    from subprocess import run
    run(['uvicorn', 'main:app', '--host=0.0.0.0', '--port=8020', '--reload'])