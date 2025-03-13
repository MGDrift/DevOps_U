FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r backend/requirements.txt
COPY . /usr/src/app/

EXPOSE 3001

CMD ["python", "src/server.py" ]