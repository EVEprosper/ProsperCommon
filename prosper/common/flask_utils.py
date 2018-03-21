"""flask_utils: general purpose Flask helpers for Docker/Debug"""
from os import path, environ

def make_gunicorn_config(
        _gunicorn_config_path='',
):
    """makes gunicorn.conf file for launching in docker

    Notes:
        https://sebest.github.io/post/protips-using-gunicorn-inside-a-docker-image/
        renders gunicorn.config (python) file in running dir
        looks for GUNICORN_{option} in environment vars
    Args:
        _gunicorn_config_path (str): TEST HOOK, path to dump file

    """
    gunicorn_py = '''"""AUTOGENERATED BY: prosper.common.flask_utils:gunicorn_config
Based off: https://sebest.github.io/post/protips-using-gunicorn-inside-a-docker-image/
"""
from os import environ

for key, value in environ.items():
    if key.startswith('GUNICORN_'):
        gunicorn_key = key.split('_', 1)[1].lower()
        locals()[gunicorn_key] = value

'''

    gunicorn_file = 'gunicorn.conf'
    if _gunicorn_config_path:
        gunicorn_file = _gunicorn_config_path

    with open(gunicorn_file, 'w') as gunicorn_cfg:
        gunicorn_cfg.write(gunicorn_py)