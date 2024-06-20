@echo off
waitress-serve --listen=0.0.0.0:8000 flask_server:app
