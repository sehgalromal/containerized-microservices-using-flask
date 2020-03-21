from pymongo import MongoClient 
from flask import Flask, request, url_for, jsonify 
import requests

app = Flask(__name__)

class MongoDB:
    @staticmethod 
    def establish_connection():
        client = MongoClient("mongodb://admin:test123@18.207.217.163:27017/English_Book_Records?authSource=admin")
        return client

conn = MongoDB() 
client = conn.establish_connection() 
database = client["English_Book_Records"]
gen_collection = database["Records"]

counter = 1 
@app.route("/catalogue/<keyword>", methods=["POST", "GET"])
def verify_keyword(keyword):
    if request.method == "POST":
        keyword = request.get_json()['keyword']
    global counter 
    title_authors = [] 
    for x in gen_collection.find({}):
        for y in (x["records"]):
            if keyword in (y[0].split(" ")) or keyword in (y[1].split(" ")):
                f = open("successful_results.txt","a")
                f.writelines(f"\n{counter}, {y[0]}, {y[1]}")
                title_authors.append((y[0], y[1]))
                f.close()
                counter += 1
    print(title_authors)
    return jsonify({
        "title": [x[0] for x in title_authors],
        "author":  [x[1] for x in title_authors] 
    }) 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5200, debug=True)