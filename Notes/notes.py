from flask import Flask, jsonify, request
import requests 
import json 

app = Flask(__name__)

counter = 1 
@app.route("/notes/<keyword>", methods = ["GET", "POST"])
def process_user_notes(keyword):
    if request.method == "POST":
        global counter 
        postedData = request.get_json()
        f = open('saved_notes.txt', 'a')
        f.writelines("\n{},{},{}".format(counter, postedData['keyword'], postedData['note']))
        f.close()
        counter += 1
        return jsonify(postedData)
    records = [] 
    f = open('saved_notes.txt', 'r')
    lines = f.readlines()[1: ]
    for line in lines:
        k = line.split(",")[1]
        note = line.split(",")[2].strip("\n")
        if keyword == k:
            records.append((k, note))
    f.close()
    return jsonify({ "notes": records }) 


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5300, debug=True)