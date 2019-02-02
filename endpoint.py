from flask import Flask,jsonify
import requests
import simplejson
import json

app = Flask(__name__)

# https://www.cbc.ca/aggregate_api/v1/swagger-ui.html#!/Authors/listAuthors

'''
Example of training data
https://www.cbc.ca/json/cmlink/{} where {} is the content id

 sessionId  contentId  eventId
0  user-000000   1.478290        0
1  user-000000   1.478271        1
2  user-000000   1.478296        2
3  user-000001   1.478358        0
4  user-000001   1.478358        1

- contendID:


- export FLASK_APP=endpoint.py
- flask run

1) Get ALL news, be able to pass in the CATEGORY of news (any other paramaters work)
2)

https://stackoverflow.com/questions/12934699/selecting-fields-from-json-output
'''



@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


@app.route('/authors')
def get_authors():
     data = request.get_json('https://www.cbc.ca/aggregate_api/v1/authors')
     name = data['name']
     return name

@app.route('/author')
def get_author():
    uri = "https://www.cbc.ca/aggregate_api/v1/authors"

    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
       return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    name = data[0]['name']# <-- The display name
    bio = data[0]['bio']# <-- The reputation

    return str(data[0])

@app.route('/author')
def get_author():
    uri = "https://www.cbc.ca/aggregate_api/v1/authors"

    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
       return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    name = data[0]['name']# <-- The display name
    bio = data[0]['bio']# <-- The reputation

    return str(data[0])

@app.route('/names')
def get_names():
    response = requests.get('https://www.cbc.ca/aggregate_api/v1/authors')
    names = json.loads(response.text)
    return names[0]["name"]


if __name__ == '__main__':
    app.run()
