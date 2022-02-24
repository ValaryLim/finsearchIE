from flask import Flask, request
import query

print("FINSEARCH BACKEND LOADED...")

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS

@app.route("/")
def main():
    return "<h1>Finsearch Backend Embedding</h1>"

@app.route("/search")
def search():
    entity1 = request.args.get('entity1')
    entity2 = request.args.get('entity2')
    direction = bool(request.args.get('direction'))
    threshold = float(request.args.get('threshold'))
    granular = bool(request.args.get('granular'))
    model = request.args.get('model')
    print(entity1, entity2, direction, threshold, granular, model)

    print("search query called")
    search_results = query.search_query(
        e1=entity1, e2=entity2, granular=granular, dir=direction, threshold=threshold, model=model
    )
    print("search results returned")
    print(search_results)
    return {
        0:search_results,
        }


if __name__ == "__main__":
    app.run(debug=True, port=5000)