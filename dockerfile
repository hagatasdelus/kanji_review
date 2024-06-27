FROM python:3.11.1-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV FLASK_APP=setup.py
ENV FLASK_RUN_HOST=0.0.0.0

ENTRYPOINT [ "/entrypoint.sh" ]
