#!/usr/bin/env bash

repo="polar"
name="polar"
version="0.1"

target_img="${repo}/${name}:${version}"
 
docker container -rm polar-analyzer

printf "Run image %s\n" "${target_image}"
docker container run -it -d --name polar-analyzer "${target_img}"