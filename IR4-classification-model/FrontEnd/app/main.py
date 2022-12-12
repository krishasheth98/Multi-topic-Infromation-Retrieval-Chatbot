from flask import Flask, render_template, request
import os
import requests
import pickle
loaded_model = pickle.load(open('Naive.sav', 'rb'))
Tfidf_vect = pickle.load(open('vectorizer.pickle', 'rb'))

app = Flask(__name__)
app.static_folder = 'static'

    
@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/get")
def get_bot_response():
    string = request.args.get('msg')
    Topic = request.args.get('Topic')
    user_input = Tfidf_vect.transform([string])
    f = 0
    predictions_naive = loaded_model.predict(user_input)
    greetings = ["hello", "hey", "hi","what's up?","howdy"]
    byes = ["bye","goodbye","i am leaving","see you later","i am going"]
    if string.lower() in greetings:
        output = "Hey, How can I help you?"
        return output
    elif string.lower() in byes:
        output = "Bye, See you soon!"
        return output
    if Topic:
        print("inTopic")
        f = 1
        if (Topic == "chkEnvironment"):
            fq='Environment'
            url = 'http://34.130.18.114:8983/solr/scrape/select?&df=body&q='+string+'&facet=on&facet.field=topic&fq=topic:'+fq+'&indent=true&q.op=AND&rows=20'
        elif Topic == "chkHealthCare":
            fq='Healthcare'
            url = 'http://34.130.18.114:8983/solr/scrape/select?&df=body&q='+string+'&facet=on&facet.field=topic&fq=topic:'+fq+'&indent=true&q.op=AND&rows=20'
        elif Topic == "chkTechnology":
            fq='Technology'
            url = 'http://34.130.18.114:8983/solr/scrape/select?&df=body&q='+string+'&facet=on&facet.field=topic&fq=topic:'+fq+'&indent=true&q.op=AND&rows=20'
        elif Topic == "chkEducation":
            fq='Education'
            url = 'http://34.130.18.114:8983/solr/scrape/select?&df=body&q='+string+'&facet=on&facet.field=topic&fq=topic:'+fq+'&indent=true&q.op=AND&rows=20'
        elif Topic == "chkPolitics":
            fq='Politics'
            url = 'http://34.130.18.114:8983/solr/scrape/select?&df=body&q='+string+'&facet=on&facet.field=topic&fq=topic:'+fq+'&indent=true&q.op=AND&rows=20'
        else:
            url = "http://34.130.18.114:8983/solr/scrape/select?&df=body&q="+string+"&indent=true&q.op=AND&rows=20"

    else:
        # print("\n\n\n naive predictions",predictions_naive,"\n\n\n")
        if predictions_naive[0]==0:
            # print("reuquest reddit")

            url = "http://34.130.18.114:8983/solr/scrape/select?&df=body&q="+string+"&facet=on&facet.field=topic&indent=true&q.op=AND&rows=20"

        elif predictions_naive[0]==1:
            # print("reuquest chitchat")
            url = 'http://34.130.18.114:8983/solr/Chitchat/select?df=request&q='+string+'&indent=true&q.op=AND&rows=20'
    payload={}
    headers = {}

    print("URL - ",url)
    response = requests.request("GET", url, headers=headers, data=payload)

    tempRes = response.json()
    print("\n\n\n",tempRes, "tempREs \n\n\n")
    userText = request.args.get('msg')
    print("In bot response!")
    if predictions_naive[0]==0 or f==1:
        # print("response docs",tempRes["response"]["docs"])
        if tempRes["response"]["numFound"]>0:
            return str(tempRes["response"]["docs"][0]["body"])
        else:
            return "Sorry, I did not get you"

    elif predictions_naive[0]==1:
        # print("\n\n bot reponse",tempRes["response"]["docs"][0],"\n\n\n")
        print("response from bot")
        if tempRes["response"]["numFound"]>0:
            return str(tempRes["response"]["docs"][0]["response"])
        else:
            return "Sorry, I did not get you"
