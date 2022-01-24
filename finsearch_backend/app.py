from flask import Flask, request
import query

app = Flask(__name__)

@app.route("/")
def main():
    print("hello world called")
    return "<p>Hello, World!</p>"

@app.route("/search")
def search():
    entity1 = request.args.get('entity1')
    entity2 = request.args.get('entity2')
    query_result = query.search_query(entity1, entity2)
    return query_result