#!flask/bin/python
## Flask Serice to make an API


from flask import Flask, jsonify, make_response, abort, request
from codecomb import get_query_results
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/codecomb', methods=['GET'])
def get_search_results():
    print ("Routed to get search results")
    print (request)
    if not request.args:
        print ("Abortingg...")
        abort(400)

    query = request.args.get('query', "")
    print (query)

    topn = 20 ## FIXME we can take this from the request itself ?
    results = get_query_results(query, topn)

    return make_response(results, 200)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)