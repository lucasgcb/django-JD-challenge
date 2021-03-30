 FROM python:3.9
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 ADD . /code/
 WORKDIR /code
 RUN pip install -r requirements.txt
 
 RUN ["chmod", "+x", "django-entrypoint.sh"]
 RUN ["chmod", "+x", "wait-for-it.sh"]
 
 EXPOSE 8000