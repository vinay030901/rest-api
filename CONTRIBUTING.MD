# CONTTRIBUTING

## How to run the dockerfile locally

docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"

how I was running the dockerfile for continuous development
docker run -dp 5000:5000 -w /app -v /app -v "/c/users/pc/desktop/resume buidling/rest api:/app" rest-apis-flask-python