FROM python:3

WORKDIR /usr/src/app/backend
COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY . /usr/src/app/

EXPOSE 3001

CMD ["python", "src/server.py" ]