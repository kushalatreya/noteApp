#!.venv/bin/python
from flask import Flask, jsonify, abort, make_response, request
# to create flask application named app
app = Flask(__name__)
notes = [
    {
        'id': 1,
        'title': u'Title One',
        'description': u'I am studying Python, its fun.',
        'show': False

    },
    {
        'id': 2,
        'title': u'Raining',
        'description': u'It was raining today, it was fun.',
        'show': False
    }
]
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/noteApp/api/v1.0/notes' , methods = ["GET"]) # it defines route, version 1 api #get #reads
def get_notes():
    return jsonify ({"notes": notes })

@app.route('/noteApp/api/v1.0/notes/<int:note_id>', methods = ["GET"]) #
def get_note(note_id):
    note = [note for note in notes if note['id'] == note_id]
    if len(note) == 0:
        abort(404)
    return jsonify({'note': note[0]})

@app.route("/noteApp/api/v1.0/notes" , methods=["POST"]) #writes
def create_note():
    if not request.json or not "title" in request.json: #validation
        abort(400)
    note = {
        "id": notes[-1]["id"] + 1, #latest note (-1 shows the last/latest element)
        "title": request.json["title"],
        "description": request.json.get("description", ""), #maybe empty, shows if there is something to show
        "show": True
    }
    notes.append(note)
    return jsonify({"note": note}), 201

@app.route("/noteApp/api/v1.0/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    note = [note for note in notes if note ["id"] == note_id]
    if len(note) == 0:
        abort(404)
    if "title" in request.json and type(request.json["title"]) != unicode:
        abort(400)
    if "description" in request.json and type(request.json["description"]) != unicode:
        abort(400)
    if "show" in request.json and type(request.json["show"]) != unicode:
        abort(400)
    note[0]["title"] = request.json.get("title",note[0]["title"])
    note[0]["description"] = request.json.get("description",note[0]["description"])
    note[0]["show"] = request.json.get("show",note[0]["show"])
    return jsonify({"note":note[0]})

@app.route("/noteApp/api/v1.0/notes/<int:note_id>",methods=["DELETE"])
def delete_note(note_id):
    note = [note for note in notes if note ["id"] == note_id]
    if len(note) == 0:
        abort(404)
    #print("not value", note) #checking
    notes.remove(note[0])
    return jsonify({"result": True})

if __name__ == '__main__': # calls main method ()
    app.run(debug=True) # running the application
