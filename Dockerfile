FROM python:3.9.8-alpine

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./petapp /petishh
WORKDIR /petishh
COPY . .

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]

# ENV ./ .workon

