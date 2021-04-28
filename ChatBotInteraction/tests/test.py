import unittest
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import app

class TestApp(unittest.TestCase):
    def test_chatbot_response(self):
        response = app.getChatbotResponse("Hello")
        self.assertIsNotNone(response)

    def test_pageloads(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertIn('F',app.chatbotTraits['Active'])

    def test_commandimpl(self):
        response = app.commandimpl("logs")
        self.assertEqual(response, "chatlogs")
    
    def test_interpretMessage(self):
        response = app.interpretMessage("!fakecommand","fakeuid",[],[])
        self.assertEqual(response['response'],"Invalid Command")


