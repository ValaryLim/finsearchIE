from flask import Flask, request
from flask_cors import CORS
import query

BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/")
def main():
    print("hello world called")
    return "<p>Hello, World!</p>"

@app.route("/search", methods=["GET", "POST"])
def search():
    response_object = { "status": "success" }
    # query
    post_data = request.get_json()
    print(post_data)
    entity1 = post_data.get('entity1')
    entity2 = post_data.get('entity2')
    direction = post_data.get('direction')
    threshold = post_data.get('threshold')
    granular = post_data.get('granular')
    search_results = query.search_query(e1=entity1, e2=entity2, granular=True, dir=direction, threshold=threshold)
    # update response
    response_object['results'] = search_results
    return response_object


if __name__ == "__main__":
    app.run(debug=True)