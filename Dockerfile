FROM python:3

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN addgroup --system app && adduser -u 1000 --system --ingroup app app
RUN chown -R app /code/djanko/airports/migrations/
USER app