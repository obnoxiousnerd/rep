```shell-session
PIPENV_VENV_IN_PROJECT=true pipenv shell --python 3.9

npx playwright install-deps chromium

PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium

pipenv run pyinstaller --paths (pipenv --venv) --add-data ./.venv/lib/python3.9/site-packages/playwright/driver:playwright/driver --onefile cli.py
```

```
podman run --rm -it -p 3000:80 -p 1025:25 --name smtp4dev rnwood/smtp4dev --tlsmode=StartTls --relayusername=repcli --relaypassword=12345678
```

```
podman run --rm -it -p 3306:3306 -v ~/school-mysql:/var/lib/mysql mysql
```