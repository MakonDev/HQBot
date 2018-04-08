# HQBot
Two bots that can receive a screenshot of a given HQ or CashShow question, and return answers with their respective probabilities of being correct, given the amount of occurrences in the first 10 google search results. Google Cloud Natural Language API and Google Cloud Optical Character Recognition API both used. Answers are subject to being incorrect, and should not be used on a live game, only for research purposes, as it violates the HQ and CashShow terms of service. 

Steps!

1) Mirror your iPhone or whatever onto your screen using quicktime

2) Now that the screen is mirrored, make sure the script and base .py file for whichever game you're playing are both on the desktop, because the script is looking for any .png file on your desktop since as soon as you take one, it appears as a .png file on the desktop. Due to this, make sure you remove any .png files from your desktop before running this because once the output is printed in the terminal, then the script deletes the actual image so that when you run the script for the next question, you don't have to manually delete the screenshot, rather it does it for you and all you have to do is run the script again... That being said, in step two, make sure you run the script_(insert game).py within the terminal BEFORE you take a screenshot every time, because if it's running, the second you take the screenshot, it'll recognize the .png file on your desktop and set everything in motion, maximizing answer time. It'll work if you don't take the screenshot first of course, but definitely advantageous to run it first. Assuming now your screen is mirrored and your script is running in the terminal waiting for a .png file...

3) take a screenshot (CMD + Shift + 4 on Mac) and as soon as the question pops up on the mirrored screen, select the question and answers so that they are the ONLY part of the screenshot.

4) Read the output in the terminal!
To understand what the terminal prints out, it will first print the screenshot filename on your desktop, then the question it's about to google search. The following 10 lines are the answer that appears the most in each of the top 10 google search pages. Immediately following that is the total probability over all 10 pages, based on appearance in the hypertext of those 10 pages. If there's a tie, or inconclusive answer, there's a last ditch search that looks for key words and performs a Boolean google search, but it only does this is in the case that no conclusive answer can be found.

5) Rinse and repeat! Since the program deletes the screenshot, all you have to do is run the script again in the terminal, and when the following question appears, screenshot it in the correct way!
