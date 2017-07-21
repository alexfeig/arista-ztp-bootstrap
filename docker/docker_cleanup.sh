#!/usr/bin/env bash

docker kill ztp-nginx
docker rm ztp-nginx
docker image rm ztp-nginx
