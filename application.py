from flask import Flask,jsonify
import requests
import json
#import pickle
#import numpy as np
#from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

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
        date = data[x]['publishedAt'] # <-- Published Date

        information = {}
        information['sourceId'] = id
        information['title'] = title
        information['description'] = description
        information['image'] = image
        information['publishTime'] = date
        arr.append(information)

    return jsonify(arr)

@app.route('/news/<sourceId>')
def get_news(sourceId):
    id = str(sourceId)
    uri = "https://www.cbc.ca/json/cmlink/" + id

    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
       return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    information = {}
    information['body'] = data['body']# <-- The display name
    information['title'] = data['headline']# <-- The reputation
    information['image'] = data['headlineimage']['originalimage']['fileurl'] # <-- Display Image
    information['date'] = data['epoch']['pubdate'] # <-- Published Date
    try:
        information['author'] = data['author']['bio']['name'] # <-- Author
        information['authorImage'] = data['author']['bio']['photo']['derivatives']['square_140']['fileurl'] # <-- Author Image
    except:
        print("no author")

    return jsonify(information)
'''
@app.route('/user/')
def post_user():
    with open("cbcModel.pk","rb") as cbc:
        cbc = pickle.load(cbc)

    #ID = 1.4597093
    ID = cbc[2][4]
    print(ID)

    #First, find best cluster
    pos = np.inf
    for idx, artID in enumerate(cbc[2]):
        if artID == ID:
            pos = idx
            break

    vector = cbc[0][pos].todense()

    bestSim = -np.inf
    bestCentroidPosition = -np.inf

    for idx, centroid in enumerate(cbc[1]):
        sim = cosine_similarity(centroid.reshape(1,-1), vector)
        if sim > bestSim:
            bestSim = sim
            bestCentroidPosition = idx

    itemsInSameCluster = []

    for idx, pos in enumerate(cbc[3]):
        if pos == bestCentroidPosition:
            itemsInSameCluster.append(idx)

    vectorsToCompare = []
    for i in itemsInSameCluster:
        vectorsToCompare.append((cbc[0][i], i))

    similarities = [(cosine_similarity(vectorsToCompare[i][0], vector),vectorsToCompare[i][1])
                             for i in range(len(vectorsToCompare))]
    similarities = sorted(similarities, reverse=True)[:5]

    bestRecommendationIds = []
    indices = [similarities[i][1] for i in range(len(similarities))]

    for i in indices:
        bestRecommendationIds.append(cbc[2][i])
    return jsonify(bestRecommendationIds)
'''
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
