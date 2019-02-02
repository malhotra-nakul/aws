from flask import Flask,jsonify
import requests
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
'''

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


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
    image = data[0]['imageLarge'] # <-- Large Display Image

    information = {}
    information['name'] = name
    information['bio'] = bio
    information['imageLarge'] = image

    return jsonify({'authors':information})

@app.route('/category')
def get_category():
    return requests.get('https://www.cbc.ca/aggregate_api/v1/categories').content

@app.route('/items/<value>')
def get_items(value):
    uri = "https://www.cbc.ca/aggregate_api/v1/items?type=story&includeCount=true"

    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
       return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    arr = []

    for x in range(int(value)):
        id = data[x]['sourceId']# <-- The source Id
        title = data[x]['title']# <-- The display title
        description = data[x]['description']# <-- The reputation
        image = data[x]['typeAttributes']['imageLarge'] # <-- Large Display Image
        date = data[x]['readablePublishedAt'] # <-- Published Date

        information = {}
        information['sourceId'] = id
        information['title'] = title
        information['description'] = description
        information['imageLarge'] = image
        information['publishDate'] = date
        arr.append(information)

    return jsonify({'items':arr})

'''
@app.route('/user/<userid>')
def get_user(userid):
    #insert results from clustering
    return stories
'''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
