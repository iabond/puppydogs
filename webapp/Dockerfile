FROM python:3.7-alpine
COPY . /src
WORKDIR /src

#Uncomment just the next 2 lines to run your application in Docker container
#EXPOSE 8000
#CMD python myserver.py 8080

#Uncomment just the next line when you want to deploy your container on Heroku
CMD python myserver.py $PORT
