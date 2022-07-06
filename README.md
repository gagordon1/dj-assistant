# dj-assistant
Assists in downloading and processing music for DJ use

#Running on server:


Observe running processes:
ps x
to end a process use "kill {PID}"

run new process:
gunicorn --workers=4 --bind=0.0.0.0 --timeout=180 --log-level=error app:app
