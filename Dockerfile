FROM python:3.12.3-slim

WORKDIR /var/www/docx

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y software-properties-common wget gnupg && \
    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    add-apt-repository 'deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main' && \
    apt-get update && \
    apt-get install -y libreoffice && \
    apt-get clean

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
