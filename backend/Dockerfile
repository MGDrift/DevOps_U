FROM python:3

WORKDIR /usr/src/app/backend

# Copiar archivos necesarios
COPY requirements.txt ./
COPY src/ ./src/  

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 3001

# Ejecutar el servidor
CMD ["python", "./src/server.py"]
