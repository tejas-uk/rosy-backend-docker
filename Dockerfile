FROM python:latest

# Install dependencies
# host.docker.internal is a special hostname that resolves to the host machine -> localhost
# curl -X POST -d {"message": "Hello, Tej!"} -H "Content-Type: application/json" http://host.docker.internal:8000/api/chat
RUN apt-get update && apt-get install -y curl

# Create a virtual environment
# To isolate our python app from sytem level python
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache -r /tmp/requirements.txt

COPY ./src .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]