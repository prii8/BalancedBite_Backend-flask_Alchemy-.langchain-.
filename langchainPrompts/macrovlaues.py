from flask import Flask
from dotenv import load_dotenv
from langchain import LLMChain
from langchain import OpenAI, PromptTemplate
from dotenv import load_dotenv
from flask import request
import os



# API_KEY=os.environ.get('OPENAI_KEY')
API_KEY="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"


def macrovalues(age,weight,height,gender,activityLevel,goal):

    prompt_template="""

    A {g} whose weight is {w} kg , height is {h} cm ,is  {a} years old,
    activity level is {act} has a goal to {goal}. provide the calorie,fats,
    carbs,protein intake to acheive the goal . the output should be in json
    format i.e in key and value
    pair and it should only have four keys that are carbs,fats,protein,
    calorie and type of value should be number.

    """
    my_prompt=PromptTemplate(template=prompt_template,input_variables=["a","g","w","h","act","goal"])

    llm=OpenAI(temperature=0,model="text-davinci-003",openai_api_key=API_KEY)

    chain=LLMChain(llm=llm,prompt=my_prompt)

    output=chain.run({"a":age,"w":weight,"g":gender,"h":height,"act":activityLevel,"goal":goal})


    return output




