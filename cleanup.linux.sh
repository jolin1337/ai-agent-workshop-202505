#!/bin/bash

uv cache clean
rm -r "$(uv python dir)"
rm -r "$(uv tool dir)"
rm $HOME\.local\bin\uv.exe
rm $HOME\.local\bin\uvx.exe

sudo rm -v /usr/local/bin/ollama
sudo rm -rv /usr/local/lib/ollama

sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm -v /etc/systemd/system/ollama.service
sudo systemctl daemon-reload

sudo userdel ollama
sudo groupdel ollama

sudo rm -rv /usr/share/ollama

docker compose down
