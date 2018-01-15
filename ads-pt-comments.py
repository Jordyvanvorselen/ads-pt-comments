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


if (__name__ == '__main__'):
    app.run(port=5000)
    print("Comment API has succesfully started.")
