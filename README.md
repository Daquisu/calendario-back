# calendario-back
[Calendario INOVA Ativista](https://calendariodissidente.fau.usp.br/) Backend

Backend for both, the normal calendar (which uses Instagram) and the Pantone (which uses Twitter)

Initialization:

- Log into our remote server through ssh

- Start ngrok to host the backend: cd Downloads/ ~> nohup ./ ngrok http 500 &

- Go to project folder to initialize Flask and the cronjob

- Flask: export FLASK_APP=api.py ~> nohup flask run &

- Cronjob: nohup python start_cron.py &

- To see the ngrok URL you can use the command: python ngrok_url.py
