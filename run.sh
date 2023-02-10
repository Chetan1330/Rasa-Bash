#!/usr/bin/python3

python3 -m venv venv
activate(){
	. ./venv/bin/activate
}
activate

pip install -r requirements.txt

rasa run actions

rasa run -m models --enable-api --cors “*” --endpoints endpoints.yml --credentials credentials.yml --debug -p 5006
