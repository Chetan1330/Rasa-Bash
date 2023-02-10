FROM rasa/rasa-sdk
WORKDIR /app
COPY requirements.txt requirements.txt
USER root
RUN pip install --upgrade pip
RUN pip install --verbose -r requirements.txt
EXPOSE 5055
