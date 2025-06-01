# Developer Setup

## Client
```bash
pip install -r client/requirements.txt
python client/capture.py
```
Press **Ctrl+Shift+R**, draw a rectangle, release mouse — screenshot appears in `%TEMP%\alex_reader`.

## Server
```bash
docker compose build api
docker compose up api
```
Check:
```bash
curl http://localhost:8080/ping
```
