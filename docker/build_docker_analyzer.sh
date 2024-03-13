#!/usr/bin/env bash
ln -s docker/Dockerfile_analyzer .

repo="polar"
name="analyzer"
version="0.1"

target_img="${repo}/${name}:${version}"

printf "Build image %s\n" "${target_image}"

docker build --no-cache -f Dockerfile_analyzer -t ${target_img} --build-arg BASE_CONTAINER=${target_img} .
docker tag "${target_img}" "${repo}/${name}:${version}"

printf "Tag %s as version number \n" "${repo}/${name}:${version}"
docker tag ${target_img} "${repo}/${name}:${version}"

docker images | grep ${name}
