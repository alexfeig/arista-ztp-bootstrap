#!/usr/bin/env bash
docker build -t af-nginx .
docker create --name="ng" -p 80:80 af-nginx
docker start ng
