from flask import Flask, request, jsonify 
import time 
import json 
import requests 

app = Flask(__name__)

start = time.clock()
request_id = 1
@app.route("/search_log/<keyword>", methods = ["POST"])
def store_keyword(keyword):
    global request_id
    keyword = request.get_json()["keyword"]
    request_time = time.clock() - start
    f = open("search.log", "a")
    f.writelines(f"\n{request_id},{request_time} ms,{keyword}")
    f.close()
    request_id += 1
    
    # post request to Catalogue 
    requests.post("http://localhost:5200/catalogue/" + keyword, json = {"keyword": keyword })

    # perform word count 
    f = open("search.log", "r")
    lines = f.readlines()[1: ]
    lines.remove("\n")
    wordDict = {}
    for line in lines:
        word = line.split(",")[2].strip("\n")
        if word not in wordDict:
            wordDict[word] = 0 
        wordDict[word] += 1
    f = open("frequency_count.json", "w")
    json.dump({ "Word_Frequency_List": wordDict }, f)
    f.close()



    return json.dumps({"searched_keyword": keyword })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5001,debug=True)
