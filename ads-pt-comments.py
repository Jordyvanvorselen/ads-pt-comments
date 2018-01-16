import json
import requests
from flask import Flask, Response, request, abort

print("Setting up comment API...")


def get_amount_of_mentions(word):
    comment_response = requests.post('http://192.168.27.170/graphql', json={'query': '''
    {
        comments(filter: "%s", options: "i") {
            id
        }
    }
    ''' % (word)})

    comments = json.loads(comment_response.text)["data"]["comments"]
    return len(comments)


def get_content_of_mentions(word):
    comment_response = requests.post('http://192.168.27.170/graphql', json={'query': '''
    {
        comments(filter: "%s", options: "i") {
            content
        }
    }
    ''' % (word)})

    return json.loads(comment_response.text)["data"]["comments"]


def get_timestamp_of_mentions(word):
    comment_response = requests.post('http://192.168.27.170/graphql', json={'query': '''
    {
        comments(filter: "%s", options: "i") {
            timestamp
        }
    }
    ''' % (word)})

    return json.loads(comment_response.text)["data"]["comments"]


def filter_mentions_by_dates(mentions, start_date, end_date):
    final_mentions = []
    for mention in mentions:
        if int(mention["timestamp"]) > int(start_date) and int(mention["timestamp"]) < int(end_date):
            final_mentions.append(mention)
    return len(final_mentions)


app = Flask(__name__)


@app.route('/mentionsamount', methods=['POST'])
def mentions_amount():
    if not request.args.get('word'):
        abort(400)
    word = request.args.get('word')
    return Response(json.dumps(get_amount_of_mentions(word)), mimetype='application/json')


@app.route('/mentionscontent', methods=['POST'])
def mentions_content():
    if not request.args.get('word'):
        abort(400)
    word = request.args.get('word')
    return Response(json.dumps(get_content_of_mentions(word)), mimetype='application/json')


@app.route('/mentionsdates', methods=['POST'])
def mentions_dates():
    if not request.args.get('word'):
        abort(400)
    word = request.args.get('word')
    start_date = request.args.get('startdate')
    end_date = request.args.get('enddate')
    return Response(json.dumps(filter_mentions_by_dates(get_timestamp_of_mentions(word), start_date, end_date)), mimetype='application/json')


print("Comment API has succesfully started.")
app.run(host="0.0.0.0", port=5001)
