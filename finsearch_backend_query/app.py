'''
Finsearch Backend Querier Main Application Start-Up Page
'''
from flask import Flask, request
from flask_cors import CORS
import requests

# Instantiate the Application
app = Flask(__name__)
app.config.from_object(__name__)

# Enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/")
def main():
    '''
    Route to check if Microservice is alive.
    '''
    return "<h1>Finsearch Backend Query</h1>"

@app.route("/query", methods=["GET", "POST"])
def query():
    '''
    Query Rest API that unpacks inputs from Finsearch Frontend and processes
    them to be fed into Finsearch Backend Embedder
    '''
    response_object = { "status": "success" }
    # query
    post_data = request.get_json()
    entity1 = post_data.get('entity1')
    entity2 = post_data.get('entity2')
    direction = post_data.get('direction')
    threshold = post_data.get('threshold')
    granular = post_data.get('granular')
    model = post_data.get('model')

    query_str = 'http://127.0.0.1:5000/search?' + '&'.join([
        f'entity1={entity1}',
        f'entity2={entity2}',
        f'direction={direction}',
        f'threshold={threshold}',
        f'granular={granular}',
        f'model={model}',
    ])

    r = requests.get(query_str)
    response_object['results'] = r.json()["0"]
    response_object['granular'] = granular
    return response_object

if __name__ == "__main__":
    app.run()
