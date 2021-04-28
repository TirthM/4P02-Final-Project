import unittest
import json


class TestBot(unittest.TestCase):

    #intents = json.loads(open('brock_data_set').read())


    #Add test cases here

    #testing if chatbot delivers the appropriate response
        def test_tag1(self):
            with open('brock_data_set.json') as f:
                data = json.load(f)
            for bot in data['intents']:
                print(data['intents'][0]) # test the first tag to see if it matches the appropriate pattern and response
                tag = bot['tag']
                pattern = bot['patterns']
               # print(tag)
               # print(pattern)
                self.assertTrue(tag, pattern)

        def test_tag2(self):
            with open('brock_data_set') as f:
                data = json.load(f)
            for bot in data['intents']:
                print(data['intents'][1]) # test the second tag to see if it matches the appropriate pattern and response
                tag = bot['tag']
                pattern = bot['patterns']
                self.assertTrue(tag, pattern)

        def test_tag3(self):
            with open('brock_data_set') as f:
                data = json.load(f)
            for bot in data['intents']:
                print(data['intents'][2]) # test the third tag to see if it matches the appropriate pattern and response
                tag = bot['tag']
                pattern = bot['patterns']
               # print(tag)
                #print(pattern)
                self.assertTrue(tag, pattern)

        def test_tag4(self):
            with open('brock_data_set') as f:
                data = json.load(f)
            for bot in data['intents']:
                print(data['intents'][3]) # test the fourth tag to see if it matches the appropriate pattern and response
                tag = bot['tag']
                pattern = bot['patterns']
               # print(tag)
               # print(pattern)
                self.assertTrue(tag, pattern)

        def test_tag5(self):
            with open('brock_data_set') as f:
                data = json.load(f)
            for bot in data['intents']:
                print(data['intents'][4]) # test the fifth tag to see if it matches the appropriate pattern and response
                tag = bot['tag']
                pattern = bot['patterns']
               # print(tag)
               # print(pattern)
                self.assertTrue(tag, pattern)

        def test_tag6(self):
            with open('brock_data_set') as f:
                data = json.load(f)
            for bot in data['intents']:
                print(data['intents'][5]) 
                tag = bot['tag']
                pattern = bot['patterns']
               # print(tag)
               # print(pattern)
                self.assertTrue(tag, pattern)

        def test_tag7(self):
            with open('brock_data_set') as f:
                data = json.load(f)
            for bot in data['intents']:
                print(data['intents'][6]) 
                tag = bot['tag']
                pattern = bot['patterns']
               # print(tag)
               # print(pattern)
                self.assertTrue(tag, pattern)



        #testing messaging feature
        def test_msg(self):
            u = self.iqc.get_chosen_inline_result("test")
            self.assertIsInstance(u.chosen_inline_result.inline_message_id, str)
            u = self.iqc.get_chosen_inline_result(
            "test", inline_message_id="sessionid")
            self.assertEqual(u.chosen_inline_result.inline_message_id, "sessionid")


if __name__ == '__main__':
    unittest.main()