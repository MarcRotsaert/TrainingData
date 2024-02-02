container="polar_django"
version="0.1"
container_image="${container}:${version}"
echo "${container_image}"

docker network create polar_network
docker network connect polar_network polardb
docker run --rm -idt -d --name "${container}" -p 8000:8000 --network polar_network "${container_image}"
sleep 10
python -m webbrowser -t "http://127.0.0.1:8000"
