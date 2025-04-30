
#FROM python:3

#WORKDIR /usr/src/app
#COPY requirements.txt ./

#RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
#COPY . /usr/src/app/

#EXPOSE 3001

#CMD ["python", "src/server.py" ]

# This Dockerfile is used to create a Docker image for the backend of the application.

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
