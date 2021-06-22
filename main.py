from py2neo import Graph, Node, Relationship, NodeMatcher
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from py2neo.client import json

app = Flask(__name__)
CORS(app, support_credentials=True)

# Verbindung zur Datenbank erstellen
try:
    graph = Graph('bolt://localhost:7687', auth=('neo4j', 'secret'))
    print('SUCCESS: Connected to the Neo4j Database.')
except Exception as e:
    print('ERROR: Could not connect to the Neo4j Database. See console for details.')
    raise SystemExit(e)

# Wird bei Registrierung aufgerufen um User in Neo4j anzulegen
@app.route('/create', methods=['POST'])
def create():
    if not request.json:
        abort(400)
    name = request.json.get("name")
    a = Node('Person', name=name)
    graph.create(a)

    return jsonify({'created': True, 'name': name})

# Fügt eine neue Relationship hinzu, Person kann sich nicht selbst folgen
@app.route('/follow', methods=['POST'])
def follow():
    if not request.json:
        abort(400)
    name = request.json.get("name")
    followName = request.json.get("followName")

    if name == followName:
        return jsonify({'follows' : False})
    else:
       graph.run("MATCH (a:Person {name: $name}),(b:Person {name: $followName})MERGE (a)-[r:FOLLOWS]->(b)", name=name,
              followName=followName).data()

    return jsonify({'follows': True})

# Entfernt Relationship zwischen zwei Usern
@app.route('/unfollow', methods=['POST'])
def unfollow():
    if not request.json:
        abort(400)
    name = request.json.get("name")
    unfollowName = request.json.get("unfollowName")

    if name == unfollowName:
        return jsonify({'unfollow' : False})
    else:
        graph.run("MATCH(a:Person {name:$name})-[r:FOLLOWS]->(b:Person {name:$unfollowName}) DELETE r", name=name,
              unfollowName=unfollowName).data()

    return jsonify({'unfollow': True})

# Liefert eine Liste der gefolgten Personen zurück
@app.route('/getfollowed', methods=['GET'])
def getfollowed():
    if not request.json:
        abort(400)
    name = request.json.get("name")

    t = graph.run("MATCH(a: Person{name: $name})-[r: FOLLOWS]->(FOLGT)RETURN FOLGT", name=name).data()

    return jsonify(t)

# Startet die Applikation
if __name__ == '__main__':
    app.run(debug=True, port=5010)

