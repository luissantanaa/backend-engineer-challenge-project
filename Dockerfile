FROM python:3.10-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#
WORKDIR /code


COPY ./requirements.txt /code/requirements.txt
COPY ./.env /code/.env

#
RUN pip install --no-cache-dir -r /code/requirements.txt

#
COPY ./app /code/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]