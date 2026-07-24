from flask import Flask, g, render_template, request, jsonify
import sqlite3

DATABASE = 'database.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#add comment
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/")
def home():
    #home page
    sql = """
            SELECT Type.TypeID, Makers.Name, Type.Born, Type.Image
            FROM Type
            JOIN Makers ON Makers.MakersID=Type.MakersID;"""
    results = query_db(sql)
    return render_template("home.html", results=results)

@app.route("/piano/<int:id>")
def piano(id):
    #just one Name base on the id
    sql = """SELECT * FROM Type
    JOIN Makers ON Makers.MakersID=Type.MakersID
    WHERE Type.TypeID = ?;"""
    result = query_db(sql, (id,),True)
    print(result)
    return render_template("piano.html", result=result)

@app.route('/history')  
def history_page():       
    return render_template('history.html')

@app.route('/elements')  
def elements_page():       
    return render_template('elements.html')


PIANO_MAP = {
    "A": ["Spinet Piano", "Console Piano", "Upright Piano"],
    "B": ["Console Piano", "Upright Piano", "Petite Grand"],
    "C": ["Baby Grand Piano", "Medium Grand Piano", "Parlor Grand / Ballroom Grand"],
    "D": ["Square Grand Piano", "Organ Piano", "Player Piano"]
}

def diagnose_piano(answers):
    score = {"A": 0, "B": 0, "C": 0, "D": 0}
    for ans in answers:
        score[ans] += 1

    sorted_types = sorted(score.items(), key=lambda x: x[1], reverse=True)

    recommendations = []
    for item in sorted_types[:3]:
        type_letter = item[0]
        recommendations.append({
            "type": type_letter,
            "pianos": PIANO_MAP[type_letter]
        })

    return recommendations

@app.route("/diagnosis", methods=["POST"])
@app.route("/diagnosis_page", methods=["POST"])
def diagnosis_page():
    payload = request.get_json(silent=True) or {}
    answers = payload.get("answers", [])
    result = diagnose_piano(answers)
    return jsonify(result)


#def get_name(id):
   # db = get_db()
    #cursor = db.cursor()
    #sql = "SELECT * FROM Name WHERE id = ?;"
    #cursor.execute(sql, (id,))
    #result = cursor.fetchone()
    #return str(result)


if __name__ == "__main__":
    app.run(debug=True)

