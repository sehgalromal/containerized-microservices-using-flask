from flask import Flask, render_template, request, redirect, url_for 
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cloud-5409-assignment-docker-containers'


class SubmitKeyword(FlaskForm):
    keyword_field = StringField('Search Keyword', render_kw={"placeholder": "Search by any keyword"})

class SubmitNotes(FlaskForm):
    notes_field = TextAreaField('Add Notes associated with the submitted keyword')
    submit_notes = SubmitField("Submit Notes")


@app.route("/", methods=["GET", "POST"])
def index():
    form1 = SubmitKeyword()
    if request.method == "POST":
        keyword = request.form["keyword_field"]
        #if the user has submitted the keyword, then that keyword will be submitted to search log 
        requests.post("http://localhost:5001/search_log/" + keyword, json = {"keyword": keyword })
        return redirect(url_for('process_search', keyword = keyword))
    return render_template('home.html', form1 = form1)

@app.route("/home/<keyword>", methods=["POST", "GET"])
def process_search(keyword):
    submitted_form = True 
    if request.method == "POST":
        return redirect(url_for('show_records', keyword = keyword))
        
    return render_template('home.html', keys = keyword, submitted = submitted_form)


@app.route("/home/records/<keyword>", methods=["POST", "GET"])
def show_records(keyword):
    show_notes = True 
    catalogue_url = "http://localhost:5200/catalogue/" + keyword
    response_keyword_catalog = requests.get(catalogue_url).json() 
    counter = 0 
    first_5_records = [] 
    for title, author in zip(response_keyword_catalog['title'],response_keyword_catalog["author"]):
        if counter == 5:
            break;
        first_5_records.append((title, author))
        counter += 1
    return render_template('home.html',result = first_5_records,  keys = request.args.get('keyword'), show_notes = show_notes)


@app.route("/home/notes/<keyword>", methods=["POST", "GET"])
def add_notes(keyword):
    success = True 
    notes = request.args.get('enter-notes')
    requests.post("http://localhost:5300/notes/" + keyword, json = {
        "note": notes,
        "keyword": keyword
    })
    return render_template('home.html', keyword = keyword, notes = notes, success = success)

@app.route("/home/notes/results/<keyword>", methods=["POST", "GET"])
def retrieve_notes(keyword):
    notes = requests.get("http://localhost:5300/notes/" + keyword).json()
    print(notes)
    return render_template('home.html', keyword = keyword, notes = notes)

if __name__ == "__main__":
    app.run(port=5000, debug=True)