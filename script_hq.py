import os
import glob
import sys
sys.path.insert(0, 'Desktop')
import hq
from timeit import default_timer


x=0
file_path = ""
while x==0: #Waits until the screenshot that ends in .png appears then saves the filename
    for file in os.listdir("Desktop"):
        if file.endswith(".png"):
            print(os.path.join("Desktop", file))
            file_path = os.path.join("Desktop", file)
            x+=1

            
start = default_timer()
            
question, answer1, answer2, answer3 = hq.detect_text(file_path) #This collects the image text using google vision api

hq.compute(question, answer1, answer2, answer3) #Search and compute answers
duration = default_timer() - start
print("Duration of program is " + str(duration) + " seconds") 

os.remove(file_path)

