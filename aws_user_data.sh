#!/bin/bash
# Paste into EC2 "User data". Replace YOUR-USERNAME and YOUR-REPO below.
apt update -y
apt install -y python3-pip python3-venv nginx git
cd /home/ubuntu
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git app
cd app
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python manage.py migrate
chown -R ubuntu:ubuntu /home/ubuntu/app

cat > /etc/systemd/system/todo.service <<SERVICE
[Unit]
Description=To-do app
After=network.target
[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/app
ExecStart=/home/ubuntu/app/venv/bin/gunicorn config.wsgi -b 127.0.0.1:8000
Restart=always
[Install]
WantedBy=multi-user.target
SERVICE

cat > /etc/nginx/sites-available/default <<'NGINX'
server {
    listen 80 default_server;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
NGINX

systemctl daemon-reload
systemctl enable --now todo
systemctl restart nginx
