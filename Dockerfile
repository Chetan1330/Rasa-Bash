FROM rasa/rasa:3.1.0
USER root
WORKDIR '/app'
COPY . /app


COPY ./data /app/data
RUN pip install --upgrade pip --no-cache-dir
RUN  rasa train
VOLUME /app
VOLUME /app/data
VOLUME /app/models
CMD ["run","-m","/app/models","--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints.yml", "--log-file", "out.log", "--debug"]