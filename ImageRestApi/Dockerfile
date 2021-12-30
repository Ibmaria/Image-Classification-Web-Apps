FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements_docker.txt
COPY . .
CMD [ "python", "app_docker.py" ]