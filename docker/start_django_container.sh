container="polar_django"
version="0.1"
container_image="${container}:${version}"
echo "${container_image}"

docker run --rm -idt -p 8080:8080 --name "${container}" "${container_image}"
sleep 10
python3 -m webbrowser -t "http://127.0.0.1:8000/algoritm"
