from services import app
import unittest 
import requests 
from datetime import datetime
import json 

class FlaskDockerContainerTest(unittest.TestCase):
    test_case_document = [] 
    # Check if Home/index page is setup properly 
    # TEST-CASE-1
    def test_index(self):
        home_page_test = app.test_client(self)
        response = home_page_test.get('/', content_type="/html/text")
        self.assertEqual(response.status_code, 200)
        f = open("test_case_document.txt", "a")
        f.writelines("\n{}, {}, {}, {}".format(self.id(),str(datetime.now()), "Test Case For Main Search Keyword Page", "Pass"))
        f.close() 
    # Check if the search query is returned after the query is submitted 
    # TEST-CASE-2
    def test_search(self):
        search_page_test = app.test_client(self)
        keyword = 'Emily'
        response = search_page_test.get("/home/" + keyword, content_type="/html/text")
        self.assertEqual(response.status_code, 200)
        f = open("test_case_document.txt", "a")
        f.writelines("\n{}, {}, {}, {}".format(self.id(),str(datetime.now()), "Check if the query is returning properly after submission", "Pass"))
        f.close() 

    # check if the records are retrieved successfully for a specific keyword 
    # TEST-CASE-3
    def test_records(self):
        show_records_test = app.test_client(self)
        keyword = 'Emily'
        response = show_records_test.get("/home/records/" + keyword, content_type="/html/text")
        self.assertEqual(response.status_code, 200)
        f = open("test_case_document.txt", "a")
        f.writelines("\n{}, {}, {}, {}".format(self.id(),str(datetime.now()), "Check if records are retrieving successfully for a specific keyword", "Pass"))
        f.close() 
    
    # check if the notes are retrieved successfully for an associated keyword 
    # TEST-CASE-4
    def test_notes(self):
        show_notes_test = app.test_client(self)
        keyword = 'Emily'
        response = show_notes_test.get("/home/notes/results/" + keyword, content_type="/html/text")
        self.assertEqual(response.status_code, 200)
        f = open("test_case_document.txt", "a")
        f.writelines("\n{}, {}, {}, {}".format(self.id(),str(datetime.now()), "Check if notes are retrieved successfully with an associated keyword", "Pass"))
        f.close() 

    # check if the query is correctly sent to search log microservice 
    # TEST-CASE-5
    def test_post_search_query(self):
        keyword = 'Emily' 
        response = requests.post("http://localhost:5001/search_log/" + keyword, json = {"keyword": keyword })
        result = response.json()
        self.assertEqual(result['searched_keyword'], keyword)
        f = open("test_case_document.txt", "a")
        f.writelines("\n{}, {}, {}, {}".format(self.id(),str(datetime.now()), "Check if query is submitted to Search Log Microservice", "Pass"))
        f.close() 

    # check if the query is correctly sent to catalogue microservice and respsonse is fetched successfully 
    # TEST-CASE-6
    def test_send_query_catalogue(self):
        keyword = 'Emily'
        response = requests.post("http://localhost:5200/catalogue/" + keyword, json = {"keyword": keyword })
        result = response.json() 
        self.assertTrue(result)
        f = open("test_case_document.txt", "a")
        f.writelines("\n{}, {}, {}, {}".format(self.id(),str(datetime.now()), "Check if query is submitted to Search Log Microservice", "Pass"))
        f.close() 

    # check if the query is correctly sending notes with an associated keyword to notes microservice 
    # TEST-CASE-7
    def test_send_query_notes(self):
        keyword = 'Emily'
        note = "hi i am author!!"
        response = requests.post("http://localhost:5300/notes/" + keyword, json = {
        "note": note,
        "keyword": keyword
        })
        result = response.json() 
        self.assertTrue(result)
        f = open("test_case_document.txt", "a")
        f.writelines("\n{}, {}, {}, {}".format(self.id(),str(datetime.now()), "Check if notes are submitted to note microservice", "Pass"))
        f.close() 


if __name__ == "__main__":
    unittest.main() 