import os
import win32com.client
import speech_recognition as sr
import webbrowser
import datetime
import openai
from config import apikey
import random


chatStr = ""
speaker = win32com.client.Dispatch("SAPI.SpVoice")

def chat(query):
    global chatStr
    # print(chatStr)
    openai.api_key = apikey
    chatStr += f"Bhavishya: {query}\n Eno: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    speaker.Speak(response["choices"][0]["text"])
    chatStr += f'{response["choices"][0]["text"]}\n'
    return response["choices"][0]["text"]

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for prompt : {prompt} \n **********************************\n\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{prompt[0:30]}.txt", "w") as f:
        f.write(text)
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
       r.pause_threshold = 0.6
       audio = r.listen(source)
       try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
       except Exception as e:
           return "Some error occureed, sorry form eno"

speaker.Speak("Hi I am Eno How can i help You")
while 1:
    print("Listening....")
    query = takecommand()
    sites = [["youtube", "https://www.youtube.com"],
            ["instagram", "https://www.instagram.com"],
            ["google", "https://www.google.com"],
            ["wikipedia", "https://www.wikipedia.org"],
            ]
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            speaker.Speak(f"Opening {site[0]} Sir...")
            webbrowser.open(site[1])
    if "open Music in Youtube".lower() in query.lower():
        speaker.Speak("Opening Music in Youtube")
        webbrowser.open("https://www.youtube.com/watch?v=OEcdsUxIsVw")
    elif "play music" in query:
        music = "/Users/bhavi/Downloads/watr-away-140590.mp3"
        speaker.Speak("Playing Music Sir")
        os.system(music)
    elif "open news in Youtube".lower() in query.lower():
        speaker.Speak("Opening News in Youtube sir")
        webbrowser.open("https://www.youtube.com/watch?v=Nq2wYlWFucg")
    elif "time" in query:
        strfTime = datetime.datetime.now().strftime(f"%H, bajkar, %M")
        speaker.Speak(f"sir time is {strfTime}")
    elif "using gpt".lower() in query.lower():
        ai(prompt=query)
    elif "quit".lower() in query.lower():
        exit()
    elif "eno reset chat".lower() in query.lower():
        chatStr = ''
    else:
        chat(query);
