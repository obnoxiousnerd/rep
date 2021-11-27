```shell-session
PIPENV_VENV_IN_PROJECT=true pipenv shell --python 3.9

npx playwright install-deps chromium

PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium

pipenv run pyinstaller --paths (pipenv --venv) --add-data ./.venv/lib/python3.9/site-packages/playwright/driver:playwright/driver --onefile cli.py
```
