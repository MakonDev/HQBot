import argparse
import io
import os
from googleapiclient.discovery import build
from google.cloud import vision
from google.cloud import language
from google.cloud.vision import types
import requests


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/Nicksadler/Desktop/TriviaApp-e7b7bf1db265.json"


def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    #print('Texts: ', len(texts))

    
    for i in range(1):
        word = '\n{}'.format(texts[i].description) #formats json results
        words = word.split("\n")
        words.pop(-1)
        words.pop(0)
        #print(word)
        
        #formulate question & save it
        question = ""
        next_index = 0 #Indicates which index the answers will come from in words after question conclusion
        for i in range(1):
            if "?" in words[i]:
                question = words[i]
                next_index = 1
            else:
                word_next = words[i+1]
                if "?" in word_next:
                    question = words[i]+" "+words[i+1]
                    next_index = 2
                else:
                    word_next_next = words[i+2]
                    if "?" in word_next_next:
                        question = words[i]+" "+words[i+1]+" "+words[i+2]
                        next_index = 3
                    else:
                        word_next_next_next = words[i+3]
                        if "?" in word_next_next_next:
                            question = words[i]+" "+words[i+1]+" "+words[i+2]+" "+words[i+3]
                            next_index = 4
        #print(question)
        answer1 = words[i+next_index]
        answer2 = words[i+next_index+1]
        answer3 = words[i+next_index+2]
        #print(answer1)
        #print(answer2)
        #print(answer3)
        
    return question, answer1, answer2, answer3


'''
#Now to actually google search these...

'''


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def compute(question, answer1, answer2, answer3):
    my_api_key = "AIzaSyAq13qg7qzUEtRYMyt-zihs1f1KGadh6-k"
    my_cse_id = "011985618827618215433:031zfpitbiq"
    boolean_q = question
    print(boolean_q)
    results = google_search(
        boolean_q, my_api_key, my_cse_id, num=10, filter="1")

    total_hits = 0
    ans1_hits = 0
    ans2_hits = 0
    ans3_hits = 0
    
    i=0
    for result in results:
        local1 = 0
        local2 = 0
        local3 = 0
        snippet = result['snippet'].lower().replace("...", " ")
        for line in snippet.split("."):
            if answer1.lower() in line:
                ans1_hits+=1
                local1+=1
                total_hits+=1
            if answer2.lower() in line:
                ans2_hits+=1
                local2+=2
                total_hits+=1
            if answer3.lower() in line:
                ans3_hits+=1
                local3+=1
                total_hits+=1
        i+=1
        if local1 == 0 and local2 == 0 and local3 == 0:
            print("No hits")
        else:
            if local1 == local2 and local1!=0:
                print(answer1+ " AND "+answer2)
            elif local2 == local3 and local2!=0:
                print(answer2+ " AND "+answer3)
            elif local1 == local3 and local1!=0:
                print(answer1+ " AND "+answer3)
            elif local1 == local2 and local2 == local3 and local1!=0:
                print("3 way tie")
            else:
                if local1>local2 and local1>local3:
                    print(answer1)
                elif local2>local3 and local2>local1:
                    print(answer2)
                elif local3>local2 and local3>local1:
                    print(answer3)

    #Compute probabilities for each answer based on occurences as a proportion of total hits for all answers
    if total_hits != 0:
        if "not".lower() in question.lower():
            print("Not detected")
            a1_p = 1-(ans1_hits/total_hits)
            a2_p = 1-(ans2_hits/total_hits)
            a3_p = 1-(ans3_hits/total_hits)
        else:
            a1_p = (ans1_hits/total_hits)
            a2_p = (ans2_hits/total_hits)
            a3_p = (ans3_hits/total_hits)

        #print probabilities for each
        print("Probability " + answer1 + " is correct: ", str(a1_p*100) + "%")
        print("Probability " + answer2 + " is correct: ", str(a2_p*100) + "%")    
        print("Probability " + answer3 + " is correct: ", str(a3_p*100) + "%")
        if (a1_p != 0 and a2_p != 0) or (a1_p != 0 and a3_p != 0) or (a2_p != 0 and a3_p != 0):
            if a1_p == a2_p or a1_p == a3_p or a2_p == a3_p:
                print("Taking a final shot...")
                last_shot(question, answer1, answer2, answer3)
    else:
        print("No hits...good luck!")
        print("Taking a final shot...")
        last_shot(question, answer1, answer2, answer3)
        return
        
def last_shot(question, answer1, answer2, answer3):
    my_api_key = "AIzaSyAq13qg7qzUEtRYMyt-zihs1f1KGadh6-k"
    my_cse_id = "011985618827618215433:031zfpitbiq"
    service = build("language", "v1")
    service_request = service.documents().analyzeEntities(
        body={
            'document': {
                'type': 'PLAIN_TEXT',
                'content': question
            },
            "encodingType":"UTF8"
        })

    response = service_request.execute()
    entity_string = ""
    for mention in response['entities']:
        entity_string = entity_string + " " + mention['name'] + " " + mention['type']       
    boolean_q1 = entity_string + " OR " + answer1+" OR " + answer2 + " OR " + answer3
    print(boolean_q1)
    results = google_search(
        boolean_q1, my_api_key, my_cse_id, num=10, filter="1")

    total_hits1 = 0
    ans1_hits1 = 0
    ans2_hits1 = 0
    ans3_hits1 = 0

    #i=0
    for result in results:
        #pprint.pprint(result)
        '''
        if i<3:
            r1 = requests.get(result['link'])
            if answer1.lower() in r1.text.lower():
                ans1_hits1+=1
                total_hits1+=1
            if answer2.lower() in r1.text.lower():
                ans2_hits1+=1
                total_hits1+=1
            if answer3.lower() in r1.text.lower():
                ans3_hits1+=1
                total_hits1+=1
        '''
        if answer1.lower() in result['snippet'].lower():
            ans1_hits1+=1
            total_hits1+=1
        if answer2.lower() in result['snippet'].lower():
            ans2_hits1+=1
            total_hits1+=1
        if answer3.lower() in result['snippet'].lower():
            ans3_hits1+=1
            total_hits1+=1
        #i+=1

    #Compute probabilities for each answer based on occurences as a proportion of total hits for all answers
    if total_hits1 != 0:
        if "not".lower() in question.lower():
            print("'Not' detected")
            a1_p1 = 1-(ans1_hits1/total_hits1)
            a2_p1 = 1-(ans2_hits1/total_hits1)
            a3_p1 = 1-(ans3_hits1/total_hits1)
        else:
            a1_p1 = (ans1_hits1/total_hits1)
            a2_p1 = (ans2_hits1/total_hits1)
            a3_p1 = (ans3_hits1/total_hits1)

        #print probabilities for each
        print("Probability " + answer1 + " is correct: ", str(a1_p1*100) + "%")
        print("Probability " + answer2 + " is correct: ", str(a2_p1*100) + "%")    
        print("Probability " + answer3 + " is correct: ", str(a3_p1*100) + "%")
    else:
        print("No hits...good luck!")
    return