import flask
from flask import Flask
from flask import request
import openai
import json
import datetime
import re
import pandas as pd
from flask import jsonify
import credentials

app = Flask(__name__)


kwargs = {"engine": "davinci", "temperature": 0.5,
          "max_tokens": 150, "stop": "\n\n", }
whatkwargs = {"engine": "davinci", "temperature": 0.0,
              "max_tokens": 100, "stop": "\n\n", }
howkwargs = {"engine": "davinci", "temperature": 0.0,
             "max_tokens": 100, "stop": "\n\n", }
openai.api_key = credentials.api_key


########################################################################
# The query function handles all queries being sent to GPT3.
########################################################################
def query(prompt, myKwargs, full=False):

    r = openai.Completion.create(prompt=prompt, **myKwargs)
    if not full:
        r = r["choices"][0]["text"].strip()
    # with open("{}.json".format(datetime.datetime.now().strftime("%Y%m%d%s")), "w") as fh:
    #     json.dump({"prompt": prompt, "response": r}, fh, indent=4)
    return r

########################################################################
# Route for WHY questions. The why() function has a prompt written to
# extract answers to repeated WHY questions
########################################################################
@app.route('/why')
def why():

    prompt = """
Q1: {
  Query: ['Why is epigenetics controversial?']

}
A1 : "Epigenetics is controversial because it is a new field of study"
Q2: Why?
A2 : "It is a new field of study because it is a relatively new area of research."
Q3: Why?
A3 : "It is a relatively new area of research because it was not discovered until the 1990s."
Q4: Why?
A4 : "It was not discovered until the 1990s because it was not possible to study until the 1990s."

Q1: {
  Query: ['Why did Japan bomb pearl harbor?']

}
A1 : "Japan bombed Pearl Harbor because the United States had imposed an oil embargo on Japan."
Q2: Why?
A2 : "Because Japan had invaded China."
Q3: Why?
A3 : "Because Japan wanted to expand its empire."
Q4: Why?
A4 : "Because Japan wanted to become the dominant power in Asia."

Q1: {
  Query: ['Why do mma fighters learn jui jitsu?']

}
A1 : "MMA fighters learn jui Jitsu because it is a martial art that focuses on grappling and ground fighting.
Q2 : Why?
A2 : "Because it leads to more submissions"
Q3 : Why?
A3 : "Because submissions can lead to victory"
Q4 : Why?
A4 : "Because the fighter wants to win"



Q1:{
  Query: ['XXXX']
}
"""

    question = request.args.get('question')
    prompt = re.sub(r"XXXX", question, prompt)
    response = query(prompt=prompt, myKwargs=kwargs)
    print(response)
    answerRegex = re.compile('^A. ?: \"(.*)\"', re.MULTILINE)
    answers = answerRegex.findall(response)
    print(len(answers))
    jsonResponse = jsonify(type="why", why_answers=answers)

    return jsonResponse

########################################################################
# Route for WHAT questions. The what() function has a prompt written to
# instruct GPT3 to answer WHAT? questions
# Note : In addition to the prompt, the args (temperature, response token length, etc.)
# are also customized for the type of question being asked.
########################################################################
@app.route('/what')
def what():

    prompt = """
Q: What is human life expectancy in the United States?
A: Human life expectancy in the United States is 78 years.

Q: Who was president of the United States in 1955?
A: Dwight D. Eisenhower was president of the United States in 1955.

Q: What party did he belong to?
A: He belonged to the Republican Party.

Q: Who was president of the United States before George W. Bush?
A: Bill Clinton was president of the United States before George W. Bush.

Q: Who won the World Series in 1995?
A: The Atlanta Braves won the World Series in 1995.

Q: XXXX?
"""

    question = request.args.get('question')
    prompt = re.sub(r"XXXX", question, prompt)
    response = query(prompt=prompt, myKwargs=whatkwargs)
    jsonResponse = jsonify(type="what", what_answer=response)
#    "answer3": answers[2],
#    "answer4": answers[3],

    return jsonResponse

########################################################################
# Route for HOW questions. The how() function has a prompt written to
# instruct GPT3 to answer HOW? questions
# Note : In addition to the prompt, the args (temperature, response token length, etc.)
# are also customized for the type of question being asked.
########################################################################
@app.route('/how')
def how():

    prompt = """
Q: How did they discover exoplanets?
A: They used a technique called the radial velocity method. This method is based on the fact that a planet will exert a gravitational pull on its host star. This pull will cause the star to wobble slightly. The wobble can be detected by looking at the spectrum of the star.

Q: How do we measure distance?
A: We use parallax. This is the apparent shift in the position of an object when viewed from two different positions.

Q: How do we measure speed?
A: We use the Doppler effect. This is the apparent change in the wavelength of light from a moving object.

Q: How do we sequence the human genome?
A: We use a technique called DNA sequencing. This is based on the fact that DNA is made up of four different bases: adenine, cytosine, guanine, and thymine. These bases are arranged in a specific order.

Q: How did we discover DNA?
A: We used a technique called X-ray diffraction. This is based on the fact that X-rays can be diffracted by crystals.

Q: XXXX?
"""

    question = request.args.get('question')
    prompt = re.sub(r"XXXX", question, prompt)
    response = query(prompt=prompt, myKwargs=howkwargs)
    jsonResponse = jsonify(type="how", how_answer=response)

    return jsonResponse
