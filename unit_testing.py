from services import app
import unittest 
import json 

class FlaskDockerContainerTest(unittest.TestCase):
    # Check if Home/index page is setup properly 
    def test_index(self):
        home_page_test = app.test_client(self)
        response = home_page_test.get('/', content_type="/html/text")
        self.assertEqual(response.status_code, 200)

    # Check if the search query is returned after the query is submitted 
    def test_search(self):
        search_page_test = app.test_client(self)
        keyword = 'Emily'
        response = search_page_test.get("/home/" + keyword, content_type="/html/text")
        self.assertEqual(response.status_code, 200)

    # check if the records are retrieved successfully for a specific keyword 
    def test_records(self):
        show_records_test = app.test_client(self)
        keyword = 'Emily'
        response = show_records_test.get("/home/records/" + keyword, content_type="/html/text")
        self.assertEqual(response.status_code, 200)
    
    # check if the notes are retrieved successfully for an associated keyword 
    def test_notes(self):
        show_notes_test = app.test_client(self)
        keyword = 'Emily'
        response = show_notes_test.get("/home/notes/results/" + keyword, content_type="/html/text")
        self.assertEqual(response.status_code, 200)


    

if __name__ == "__main__":
    unittest.main() 