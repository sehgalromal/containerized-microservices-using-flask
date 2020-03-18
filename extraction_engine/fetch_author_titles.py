import re 
import os 
from pymongo import MongoClient 
import time 

class MongoDB:
    @staticmethod 
    def establish_connection():
        client = MongoClient("mongodb://admin:test123@34.205.74.123:27017/English_Book_Records?authSource=admin")
        return client

def generate_title_authors(filename):
    with open(filename, encoding= "utf-8") as file:
        lines = [] 
        index = 0
        text = file.readlines()
        count = 0 
        for line in text:
            if "TITLE and AUTHOR" in line:
                index = count
            lines.append(line)
            count += 1

    lines = lines[index: ]
    it = iter(lines)

    pattern = re.compile("([A-Za-z0-9\s]+)\s?, by\s?([A-Za-z\s]+)")
    sents = list(zip(it, it))

    titles_authors = [] 
    for sent in sents:
        if not ' [Language: French]\n' == sent[1] or ' [Language: German]\n' == sent[1] or ' [Language: Latin]\n' == sent[1] or ' [Language: Spanish]\n' == sent[1] or ' [Languages: Latin and German]\n' == sent[1]:
            sent = " ".join(sent)
            sent = re.sub("\n","",sent)
            sent = re.sub(" +"," ",sent)
            if sent[0] == " ":   
                sent = sent[1: ] 
                if pattern.search(sent):
                    titles_authors.append((pattern.search(sent).group(1), pattern.search(sent).group(2)))
            else:
                if pattern.search(sent):
                    titles_authors.append((pattern.search(sent).group(1),pattern.search(sent).group(2)))
    return titles_authors

list_files = list(range(1996, 2021))
documents = os.listdir('G:\MACS_DEGREE\Term-2\Cloud-Computing\Assignments\Assignment-3\Gutenberg_Dataset')

con = MongoDB()
client = con.establish_connection();
database = client["English_Book_Records"]
gen_collection = database["Records"]

counter = 1995
for document in documents:
    doc_path = "G://MACS_DEGREE//Term-2//Cloud-Computing//Assignments//Assignment-3//Gutenberg_Dataset//" + document 
    file_process = generate_title_authors(doc_path)
    data = {"_id": counter+1, "file_name": document, "start_time": time.time() } 
    gen_collection.insert_one(data)
    gen_collection.update_one({"_id": counter+1 }, { "$set" : {"records": file_process }})
    data = { "_id": counter+1, "end_time": file_process }
    gen_collection.update_one({"_id": counter+1 }, {"$set" : {"end_time": time.time()} })
    counter += 1
    time.sleep(5)
