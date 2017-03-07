#!/usr/bin/env bash

docker build -t ztp-nginx .
docker create --name="ztp-nginx" -p 80:80 ztp-nginx
docker start ztp-nginx
