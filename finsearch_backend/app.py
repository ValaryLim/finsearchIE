from flask import Flask, request
from flask_cors import CORS
import query

print("FINSEARCH BACKEND LOADED...")

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
    entity1 = post_data.get('entity1')
    entity2 = post_data.get('entity2')
    direction = post_data.get('direction')
    threshold = post_data.get('threshold')
    granular = post_data.get('granular')
    model = post_data.get('model')
    search_results = query.search_query(
        e1=entity1, e2=entity2, granular=granular, dir=direction, threshold=threshold, model=model
    )
    # update response
    response_object['results'] = search_results
    response_object['granular'] = granular
    return response_object


if __name__ == "__main__":
    app.run(debug=True)