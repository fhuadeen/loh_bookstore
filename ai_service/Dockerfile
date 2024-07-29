FROM python:3.8.1-slim-buster

# Update the package lists and install Git
RUN apt-get update -y && \
    apt-get install -y git

WORKDIR /code

# layer cache requirments; it doesn't rebuild for every change in the code 
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

EXPOSE 5005

ENV FLASK_APP=api/app.py

RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]
