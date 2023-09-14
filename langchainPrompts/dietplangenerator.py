from flask import Flask
from langchain import LLMChain
from langchain import OpenAI, PromptTemplate
from dotenv import load_dotenv
from flask import request
import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType,Tool
from langchain import  SerpAPIWrapper
from langchain.chat_models import ChatOpenAI



# API_KEY=os.environ.get('OPENAI_KEY')
API_KEY="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"
SERPAPI_KEY="d79d39f24ee3bb4d26243f3bb6b114e7e6c0f49ed7e3b622ff4995144e4a7541"

def mealplan(g,w,h,a,act,goal,allergies,veg,cuisine,meals):
    prompt_template="""
    You are a helpful nutritionist and a dietitian ,your job is to provide diet plan .make sure person daily
    requirement of carbs,fats,protein and calorie is fullfilled ,and make sure that diet plan  consists of the number of meals
    as provided if it is 3 only provide breakfast,lunch and dinner ,if 4 provide one more meal named snack1 and if 5 provide add 
    one more in output that is snack2,also diet should help person to achieve their goal.not only that you care about person budget 
    constraints too,so you provide the person three option for each meal ,the first one will be budget friendly that costs under 100 rupees,
    second should range between 100 -200 rupees and Third can cost between 200 - 400 ,but keep in mind that the marconutrients of all three
    should be similar approximately.one thing you should take care of is if the person wants to loose wait don't include anything in the diet
    that can result in increase of weight the diet should consists of less carbs ,fats but more of protein ,just keep a check of these things
    (for example chole Bhature,allo parantha).


    Following is the detail about the person:-
    A {g} whose weight is {w} kg , height is {h} cm ,is  {a} years old,
    activity level is {act} has a goal to {goal}.is alergic to {allergies},eats only {veg} food and prefered cuisine type is {cuisine},
    the person perfers to  eat {meals}  per day.provide a diet plan for one day to achieve the above mentioned goal .
    REMEMBER these point while generating output.
    1.The output must be in json format i.e key value pair.
    2.The Three keys are Breakfast,Lunch,Dinner.
    3.The type of value will be a string it will have the name of the dish that should be eaten.
    4.Make sure each meal wheather Breakfast ,lunch or anything should just have only one dish not more than that.
    5.provide averge cost  of making the dish in rupees . that also in json format ,type of cost value will be a number.
    following is example output ,make sure that the json is in this format and also  key should be in lowercase only.
    example output:"""+r"""
    [
    "Breakfast":["option1":
                ["dish":"name",
                "cost":80],
                "option2":
                ["dish":"name",
                "cost":80],
                "option3":
                ["dish":"name",
                "cost":80]
                ],
    "Lunch":["option1":
                ["dish":"name",
                "cost":80],
                "option2":
                ["dish":"name",
                "cost":80],
                "option3":
                ["dish":"name",
                "cost":80]
                ],

    "Dinner":["option1":
                ["dish":"name",
                "cost":80],
                "option2":
                ["dish":"name",
                "cost":80],
                "option3":
                ["dish":"name",
                "cost":80]
                ],

    ]
    """
    
    
     

    my_prompt=PromptTemplate(template=prompt_template,input_variables=["g","w","h","a","act","goal","allergies","veg","cuisine","meals"])
    

    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=API_KEY,cache=False)

    chain=LLMChain(llm=llm,prompt=my_prompt,verbose=True)
    
    
    output=chain.run({"g":g,"w":w,"h":h,"a":a,"act":act,"goal":goal,"allergies":allergies,"veg":veg,"cuisine":cuisine,"meals":meals})

    return output



def Macromealplan(g,fats,calorie,protein,carbs,goal,allergies,veg,cuisine,meals):
    """This function provides the mealplan or dietplan taking macronutrients like carbs,protien,fatsand calorie as input"""


    prompt_template="""

    You are a helpful nutritionist and a dietitian ,your job is to provide diet plan .You will be provide daily marconutrients requirement of person ,your job is to make sure person diet paln such that
    requirement of carbs,fats,protein and calorie is fullfilled.  make sure that diet plan  consists of the number of meals as provided ,
    if it is 3 only provide breakfast,lunch and dinner ,if 4 provide one more meal named snack1 and if 5 provide add one more in output 
    that is snack2,also diet should help person to achieve their goal,now also take note of person daily requirement of protein,carbs,fats
    and calories by that I mean ,sum of calories,carbs,protein and fats of each meal should be equal to their respective target requirements that will be provide to you.not only that you care about person budget 
    constraints too,so you provide the person three option for each meal ,the first one will be budget friendly that costs under 100 rupees,
    second should range between 100 -200 rupees and Third can cost between 200 - 400 ,but keep in mind that the marconutrients of all three
    should be similar approximately.one thing you should take care of is if the person wants to loose wait don't include anything in the diet
    that can result in increase of weight the diet should consists of less carbs ,fats but more of protein ,just keep a check of these things
    (for example chole Bhature,allo parantha).

    Following is the detail about the person:-
    A {g} daily requirement of carbs is {carbs} g,protein is {protein} g,calorie is {calorie} Kcal and fats is {fats}.
    Their goal is to {goal},is alergic to {allergies},eats only {veg} food and prefered cuisine type is {cuisine},
    the person perfers to  eat {meals}  per day .provide a diet plan for one day so that person can fulfill their daily requirements  .
    REMEMBER these point while generating output.
    1.The output must be in json format i.e key value pair.
    2.The Three keys are Breakfast,Lunch,Dinner.
    3.The type of value will be a string it will have the name of the dish that should be eaten.
    4.Make sure each meal wheather Breakfast ,lunch or anything should just have only one dish not more than that.
    5.provide averge cost  of making the dish in rupees . that also in json format ,type of cost value will be a number.
    6.provide the carbs , protein, colorie ,fats of each meal.
    following is example output ,make sure that the json is in this format and also  key should be in lowercase only.
    example output: 
    [
    "Breakfast":["option1":
                ["dish":"name",
                "cost":80],
                "option2":
                ["dish":"name",
                "cost":80],
                "option3":
                ["dish":"name",
                "cost":80]
                ],
    "Lunch":["option1":
                ["dish":"name",
                "cost":80],
                "option2":
                ["dish":"name",
                "cost":80],
                "option3":
                ["dish":"name",
                "cost":80]
                ],

    "Dinner":["option1":
                ["dish":"name",
                "cost":80],
                "option2":
                ["dish":"name",
                "cost":80],
                "option3":
                ["dish":"name",
                "cost":80]
                ],

    ]
    """
    
    
    
     

    my_prompt=PromptTemplate(template=prompt_template,input_variables=["g","fats","calorie","protein","carbs","goal","allergies","veg","cuisine","meals"])
    

    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=API_KEY,cache=False)

    chain=LLMChain(llm=llm,prompt=my_prompt,verbose=True)
    
    
    output=chain.run({"g":g,"fats":fats,"calorie":calorie,"protein":protein,"carbs":carbs,"goal":goal,"allergies":allergies,"veg":veg,"cuisine":cuisine,"meals":meals})

    return output


def MealswapBudget(price,carbs,protein,fats,calorie,allergies,veg,cuisine,dish):
    """  Can be used when want to get a meal within certain budget keeping the macronutrients almost same."""
   
    search = SerpAPIWrapper(serpapi_api_key=SERPAPI_KEY)
    tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to get dish name that is under certain budget limit and dish should have same carbs,protein,fats and calorie as provided")
    ]
    
    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=API_KEY)
    
    query2="Suggest a dish that  approximately cost"+price+"rupees and  nutritional value per serving should be somewhat same as dish "+dish+"if you don't get same nutritional value "
    
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True)
    output=agent.run(query2)

    return output



def Breakfastplan(g,fats,calorie,protein,carbs,goal,allergies,veg,cuisine,meals):
    """This function provides the breakfast taking macronutrients like carbs,protien,fatsand calorie as input"""


    prompt_template="""
    You are a nutritionist and a dietitian ,your job is to provide diet plan accoriding to user cuisine type ,include all variety of 
    foods that are possible from their cuisine and don't just suggest common food like poha ,omelette etc ,you can include them but only sometimes ,so that it easy and fun for them to achieve goal .
    You will be suggesting healthy and nutritious Breakfast for the person .you will be provided with person daily macronutrient requirement, allgeries ,cuisine type they prefer and 
    other detail ,as you are a nutritionist you will take all this information into consideration while suggest the best breakfast option 
    for them.
    Also you will provide them 3 option for their breakfast , option1 will be budget friendly that is its price can be under 100 rupees,
    option2 can have price  100 to 200 rupees and option3 can cost anything over 220 rupees ,in option3 you can suggest
    those dishes in which the cost of ingredient used is high.
      .the output that you will provide will consist of dish ,  cost , carbs, protein,calorie
    and fats.

    Following is the detail about the person:-
    A {g} daily requirement of carbs is {carbs} g,protein is {protein} g,calorie is {calorie} Kcal and fats is {fats}.
    Their goal is to {goal},is alergic to {allergies},eats only {veg} food and prefered cuisine type is {cuisine},and have {meals} number 
    of meals per day.suggest breakfast according to the cuisine type for the day so that person can fulfill their goal .
    REMEMBER these point while generating output.
    1.The output must be in json format i.e key value pair.
    2.The type of value will be a string it will have the name of the dish that should be eaten.
    3.Make sure each option should just have only one dish not more than that.
    4.provide averge cost  of making the dish in rupees . that also in json format ,type of cost value will be a number.
    5.provide carbs,protein,calorie and fats of the dish without units(kcal or gms) . that also in json format ,type of there value will be a number .
    
    following is example output ,make sure that the json is in this format and also  key should be in lowercase only.
    that should strictly in json format ,no list or anything else.
    example output: 
    [
    "breakfast":["option1":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option2":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option3":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5]
                ]


    ]
    """
    
    
    
    
     

    my_prompt=PromptTemplate(template=prompt_template,input_variables=["g","fats","calorie","protein","carbs","goal","allergies","veg","cuisine","meals"])
    

    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=API_KEY,cache=False)

    chain=LLMChain(llm=llm,prompt=my_prompt,verbose=True)
    
    
    output=chain.run({"g":g,"fats":fats,"calorie":calorie,"protein":protein,"carbs":carbs,"goal":goal,"allergies":allergies,"veg":veg,"cuisine":cuisine,"meals":meals})

    return output




def Lunchplan(g,fats,calorie,protein,carbs,goal,allergies,veg,cuisine,meals):
    """This function provides the breakfast taking macronutrients like carbs,protien,fatsand calorie as input"""

    prompt_template="""
    You are a nutritionist and a dietitian ,your job is to suggest lunch accoriding to user cuisine type ,include all variety of 
    foods that are possible from their cuisine ,so that it easy and fun for them to achieve weight goal .
    You will be suggesting healthy and nutritious Lunch for the person .you will be provided with person daily macronutrient requirement, allgeries ,cuisine type they prefer and 
    other detail ,as you are a nutritionist you will take all this information into consideration while suggest the best Lunch option 
    for them.also if person wants to loose wait don't suggest things that can lead to increase in weight like parantha,butter chicken
    or dish that should not be eaten while reducing weight.
    Also you will provide them 3 option for their Dinner , option1 will be budget friendly that is its price can be under 100 rupees,
    option2 can have price  100 to 200 rupees and option3 can cost anything over 220 rupees ,in option3 you can suggest
    those dishes in which the cost of ingredient used is high.
      .the output that you will provide will consist of dish ,  cost , carbs, protein,calorie
    and fats.

    Following is the detail about the person:-
    A {g} daily requirement of carbs is {carbs} g,protein is {protein} g,calorie is {calorie} Kcal and fats is {fats}.
    Their goal is to {goal},is alergic to {allergies},eats only {veg} food and prefered cuisine type is {cuisine},and have {meals} number 
    of meals per day.suggest breakfast according to the cuisine type for the day so that person can fulfill their goal .
    REMEMBER these point while generating output.
    1.The output must be in json format i.e key value pair.
    2.The type of value will be a string it will have the name of the dish that should be eaten.
    3.Make sure each option should just have only one dish not more than that.
    4.provide averge cost  of making the dish in rupees . that also in json format ,type of cost value will be a number.
    5.provide carbs,protein,calorie and fats of the dish without units(kcal or gms) . that also in json format ,type of there value will be a number .
    
    following is example output ,make sure that the json is in this format and also  key should be in lowercase only.
    that should strictly in json format ,no list or anything else.
    example output: 
    [
    "lunch":["option1":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option2":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option3":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5]
                ]


    ]
    """
    
    
    
    
     

    my_prompt=PromptTemplate(template=prompt_template,input_variables=["g","fats","calorie","protein","carbs","goal","allergies","veg","cuisine","meals"])
    

    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=API_KEY,cache=False)

    chain=LLMChain(llm=llm,prompt=my_prompt,verbose=True)
    
    
    output=chain.run({"g":g,"fats":fats,"calorie":calorie,"protein":protein,"carbs":carbs,"goal":goal,"allergies":allergies,"veg":veg,"cuisine":cuisine,"meals":meals})

    return output






def Dinnerplan(g,fats,calorie,protein,carbs,goal,allergies,veg,cuisine,meals):
    """This function provides the breakfast taking macronutrients like carbs,protien,fatsand calorie as input"""


    prompt_template="""
    You are a nutritionist and a dietitian ,your job is to provide Dinner accoriding to user cuisine type ,include all variety of 
    foods that are possible from their cuisine ,so that it easy and fun for them to achieve goal .
    You will be suggesting healthy and nutritious Dinner for the person .you will be provided with person daily macronutrient requirement, allgeries ,cuisine type they prefer and 
    other detail ,as you are a nutritionist you will take all this information into consideration while suggest the best Dinner option 
    for them.also if person wants to loose wait don't suggest things that can lead to increase in weight like parantha,butter chicken
    or dish that should not be eaten at nights.
    Also you will provide them 3 option for their Dinner , option1 will be budget friendly that is its price can be under 100 rupees,
    option2 can have price  100 to 200 rupees and option3 can cost anything over 220 rupees ,in option3 you can suggest
    those dishes in which the cost of ingredient used is high.
      .the output that you will provide will consist of dish ,  cost , carbs, protein,calorie
    and fats.

    Following is the detail about the person:-
    A {g} daily requirement of carbs is {carbs} g,protein is {protein} g,calorie is {calorie} Kcal and fats is {fats}.
    Their goal is to {goal},is alergic to {allergies},eats only {veg} food and prefered cuisine type is {cuisine},and have {meals} number 
    of meals per day.suggest breakfast according to the cuisine type for the day so that person can fulfill their goal .
    REMEMBER these point while generating output.
    1.The output must be in json format i.e key value pair.
    2.The type of value will be a string it will have the name of the dish that should be eaten.
    3.Make sure each option should just have only one dish not more than that.
    4.provide averge cost  of making the dish in rupees . that also in json format ,type of cost value will be a number.
    5.provide carbs,protein,calorie and fats of the dish without units(kcal or gms) . that also in json format ,type of there value will be a number .
    
    following is example output ,make sure that the json is in this format and also  key should be in lowercase only.
    that should strictly in json format ,no list or anything else.
    example output: 
    [
    "dinner":["option1":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option2":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option3":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5]
                ]


    ]
    """
    
    
    
    
     

    my_prompt=PromptTemplate(template=prompt_template,input_variables=["g","fats","calorie","protein","carbs","goal","allergies","veg","cuisine","meals"])
    

    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=API_KEY,cache=False)

    chain=LLMChain(llm=llm,prompt=my_prompt,verbose=True)
    
    
    output=chain.run({"g":g,"fats":fats,"calorie":calorie,"protein":protein,"carbs":carbs,"goal":goal,"allergies":allergies,"veg":veg,"cuisine":cuisine,"meals":meals})

    return output




def Elevensesplan(g,fats,calorie,protein,carbs,goal,allergies,veg,cuisine,meals):
    """This function provides the breakfast taking macronutrients like carbs,protien,fatsand calorie as input"""


    prompt_template="""
    You are a nutritionist and a dietitian ,you will be provided with person daily macronutrient requirement, allgeries ,cuisine type they prefer and 
    other detail . your job is to suggest snack that person can have between breakfast and lunch ,snacks can't be a proper meal,
    For  snacks you can suggest things like  smoothie  of mango or anything else,shakes,salad,cereal,apple  etc and can try to suggest
    such kind of things from their cuisine type.
    You will be suggesting healthy and nutritious snack for the person .as you are a nutritionist you will take all this information of the person into 
    consideration while suggesting the best snack option 
    for them.also if person wants to loose weight don't suggest things that can lead to increase in weight.
    Also you will provide them 3 option for their Snack , option1 will be budget friendly that is its price can be under 80 rupees,
    option2 can have price  100 to 150 rupees and option3 can cost anything over 170 rupees ,in option3 you can suggest
    those snak in which the cost of ingredient used is high and nutrition value is worth the money.
    try to include beverage in one of the option.
      .the output that you will provide will consist of dish ,  cost , carbs, protein,calorie
    and fats.

    Following is the detail about the person:-
    A {g} daily requirement of carbs is {carbs} g,protein is {protein} g,calorie is {calorie} Kcal and fats is {fats}.
    Their goal is to {goal},is alergic to {allergies},eats only {veg} food and prefered cuisine type is {cuisine},and have {meals} number 
    of meals per day.suggest snack according to the person detail for the day so that person can fulfill their goal .
    REMEMBER these point while generating output.
    1.The output must be in json format i.e key value pair.
    2.The type of value will be a string it will have the name of the dish that should be eaten.
    3.Make sure each option should just have only one dish not more than that.
    4.provide averge cost  of making the dish in rupees . that also in json format ,type of cost value will be a number.
    5.provide carbs,protein,calorie and fats of the dish without units(kcal or gms) . that also in json format ,type of there value will be a number .
    
    following is example output ,make sure that the json is in this format and also  key should be in lowercase only.
    that should strictly in json format ,no list or anything else.
    example output: 
    [
    "morningsnack":["option1":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option2":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option3":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5]
                ]


    ]
    """
    
    
    
    
     

    my_prompt=PromptTemplate(template=prompt_template,input_variables=["g","fats","calorie","protein","carbs","goal","allergies","veg","cuisine","meals"])
    

    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=API_KEY,cache=False)

    chain=LLMChain(llm=llm,prompt=my_prompt,verbose=True)
    
    
    output=chain.run({"g":g,"fats":fats,"calorie":calorie,"protein":protein,"carbs":carbs,"goal":goal,"allergies":allergies,"veg":veg,"cuisine":cuisine,"meals":meals})

    return output








def Eveningsnackplan(g,fats,calorie,protein,carbs,goal,allergies,veg,cuisine,meals):
    """This function provides the breakfast taking macronutrients like carbs,protien,fatsand calorie as input"""


    prompt_template="""
   You are a nutritionist and a dietitian ,you will be provided with person daily macronutrient requirement, allgeries ,cuisine type they prefer and 
    other detail . your job is to suggest snack that person can have between lunch and dinner ,snacks can't be a proper meal,
    For  snacks you can suggest things like  smoothie  of mango or anything else,shakes,salad,cereal,apple  etc and can try to suggest
    such kind of things from their cuisine type.
    You will be suggesting healthy and nutritious snack for the person .as you are a nutritionist you will take all this information of the person into 
    consideration while suggesting the best snack option 
    for them.also if person wants to loose weight don't suggest things that can lead to increase in weight.
    Also you will provide them 3 option for their Snack , option1 will be budget friendly that is its price can be under 80 rupees,
    option2 can have price  100 to 150 rupees and option3 can cost anything around 170 rupees ,in option3 you can suggest
    those snak in which the cost of ingredient used is high and nutrition value is worth the money.
    try to include beverage in one of the option.
      .the output that you will provide will consist of dish ,  cost , carbs, protein,calorie
    and fats.

    Following is the detail about the person:-
    A {g} daily requirement of carbs is {carbs} g,protein is {protein} g,calorie is {calorie} Kcal and fats is {fats}.
    Their goal is to {goal},is alergic to {allergies},eats only {veg} food and prefered cuisine type is {cuisine},and have {meals} number 
    of meals per day.suggest snack according to the person detail for the day so that person can fulfill their goal .
    REMEMBER these point while generating output.
    1.The output must be in json format i.e key value pair.
    2.The type of value will be a string it will have the name of the dish that should be eaten.
    3.Make sure each option should just have only one dish not more than that.
    4.provide averge cost  of making the dish in rupees . that also in json format ,type of cost value will be a number.
    5.provide carbs,protein,calorie and fats of the dish without units(kcal or gms) . that also in json format ,type of there value will be a number .
    
    following is example output ,make sure that the json is in this format and also  key should be in lowercase only.
    that should strictly in json format ,no list or anything else.
    example output: 
    [
    "eveningsnack":["option1":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option2":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option3":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5]
                ]


    ]
    """
    
    
    
    
     

    my_prompt=PromptTemplate(template=prompt_template,input_variables=["g","fats","calorie","protein","carbs","goal","allergies","veg","cuisine","meals"])
    

    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=API_KEY,cache=False)

    chain=LLMChain(llm=llm,prompt=my_prompt,verbose=True)
    
    
    output=chain.run({"g":g,"fats":fats,"calorie":calorie,"protein":protein,"carbs":carbs,"goal":goal,"allergies":allergies,"veg":veg,"cuisine":cuisine,"meals":meals})

    return output



def MacroBreakfastplan(g,fats,calorie,protein,carbs,goal,allergies,veg,cuisine):
    """This function provides the breakfast taking macronutrients like carbs,protien,fatsand calorie as input"""


    prompt_template="""
    You are a nutritionist and a dietitian ,your job is to  suggest a nutitious and flovouful Breakfast based on the user's
    prefered cuisine type ,include all variety of foods that are possible from their cuisine and don't just suggest common food 
    like poha ,ommlet etc  these are very common breakfast option ,suggest something that is nutritious and tasty at the same time ,so that it easy and fun for person to achieve goal .
    .you will be provided the details regarding the desired macronutrient to be provide by the Breakfast ,so option provided should ensure that
    person's macronutrient requirement are fulfilled.
    you will also be provided with person details regarding any allgeries , their prefered cuisine type and 
    their goal like whether they want to reduce weight , gain weight or maintain the weight ,as you are a nutritionist you will take 
    all this information into consideration while suggestting the best breakfast option for them.
    If person want to loose weight don't suggest anything that will lead to gain weight for example Chole Bhature,Paratha.
    Also you will provide them 3 option for their breakfast , option1 will be budget friendly that is its price can be under 100 rupees,
    option2 can have price  100 to 200 rupees and option3 can cost anything over 220 rupees ,in option3 you can suggest
    those dishes in which the cost of ingredient used is high and nutrition value of the food is worth the money .
    Try macronutrient of all the the three option be somewhat similar if not same.
    The output that you will provide will consist of dish ,  cost , carbs, protein,calorie
    and fats.

    Following is the detail about the person:-
    A {g} wants that {carbs} gms of carbs,{protein} gms of protein ,{calorie} Kcal of calorie and {fats} gms of fats is
    provided by the breakfast .
    Their goal is to {goal},is alergic to {allergies},eats only {veg} food and prefered cuisine type is {cuisine}.
    suggest breakfast according to the cuisine type for the day so that person can fulfill their goal .
    REMEMBER these point while generating output.
    1.The output must be in json format i.e key value pair.
    2.The type of value will be a string it will have the name of the dish that should be eaten.
    3.Make sure each option should just have only one dish not more than that.
    4.provide averge cost  of making the dish in rupees . that also in json format ,type of cost value will be a number.
    5.provide carbs,protein,calorie and fats of the dish without units(kcal or gms) . that also in json format ,type of there value will be a number .
    
    following is example output ,make sure that the json is in this format and also  key should be in lowercase only.
    example output: 
    [
    "breakfast":["option1":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option2":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option3":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5]
                ]


    ]
    """
    
    
    
    
     

    my_prompt=PromptTemplate(template=prompt_template,input_variables=["g","fats","calorie","protein","carbs","goal","allergies","veg","cuisine"])
    

    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=API_KEY,cache=False)

    chain=LLMChain(llm=llm,prompt=my_prompt,verbose=True)
    
    
    output=chain.run({"g":g,"fats":fats,"calorie":calorie,"protein":protein,"carbs":carbs,"goal":goal,"allergies":allergies,"veg":veg,"cuisine":cuisine})

    return output



def MacroElevensesplan(g,fats,calorie,protein,carbs,goal,allergies,veg,cuisine):
    """This function provides the breakfast taking macronutrients like carbs,protien,fatsand calorie as input"""


    prompt_template="""
    You are a nutritionist and a dietitian ,you will be provided with person , allgeries ,cuisine type they prefer and 
    their goal like gain weight , lose weight and maintain weight . your job is to suggest morning Snack that person can have between breakfast and lunch ,snacks can't be a proper meal,
    For  snacks you can suggest things like  mango smoothie   or any other fruit smooties ,shakes,salad,cereal,fruits etc and you can try suggestting
    snack from their prefered cuisine type.you will be provided the details regarding the desired macronutrient to be provide by the Snack ,so option provided should ensure that
    person's macronutrient requirement are fulfilled.
    You will be suggesting healthy and nutritious snack for the person .as you are a nutritionist you will take all this information of the person into 
    consideration while suggesting the best snack option  for them.
    also if person wants to loose weight don't suggest things that can lead to increase in weight.
    Also you will provide them 3 option for their Snack , option1 will be budget friendly that is its price can be under 80 rupees,
    option2 can have price  100 to 150 rupees and option3 can cost anything over 170 rupees ,in option3 you can suggest
    those snack in which the cost of ingredient used is high and nutrition value is worth the money.
    try to include beverage in one of the option.Try macronutrient of all the the three option be somewhat similar if not same.
    The output that you will provide will consist of dish ,  cost , carbs, protein,calorie
    and fats.

    Following is the detail about the person:-
    A {g} wants that {carbs} gms of carbs,{protein} gms of protein ,{calorie} Kcal of calorie and {fats} gms of fats is
    provided by the morning snack .
    Their goal is to {goal},is alergic to {allergies},eats only {veg} food and prefered cuisine type is {cuisine}.
    suggest snack according to the person detail for the day so that person can fulfill their goal and try macronutrients if not close should be somewhat similar to what user want.
    REMEMBER these point while generating output.
    1.The output must be in json format i.e key value pair.
    2.The type of value will be a string it will have the name of the dish that should be eaten.
    3.Make sure each option should just have only one dish not more than that.
    4.provide averge cost  of making the dish in rupees . that also in json format ,type of cost value will be a number.
    5.provide carbs,protein,calorie and fats of the dish without units(kcal or gms) . that also in json format ,type of there value will be a number .
    
    following is example output ,make sure that the json is in this format and also  key should be in lowercase only.
    that should strictly in json format ,no list or anything else.
    example output: 
    [
    "morningsnack":["option1":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option2":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option3":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5]
                ]


    ]
    """
    
    
    
    
     

    my_prompt=PromptTemplate(template=prompt_template,input_variables=["g","fats","calorie","protein","carbs","goal","allergies","veg","cuisine"])
    

    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=API_KEY,cache=False)

    chain=LLMChain(llm=llm,prompt=my_prompt,verbose=True)
    
    
    output=chain.run({"g":g,"fats":fats,"calorie":calorie,"protein":protein,"carbs":carbs,"goal":goal,"allergies":allergies,"veg":veg,"cuisine":cuisine})

    return output



def MacroLunchplan(g,fats,calorie,protein,carbs,goal,allergies,veg,cuisine):
    """This function provides the lunch taking macronutrients like carbs,protien,fatsand calorie as input"""


    prompt_template="""
    You are a nutritionist and a dietitian ,your job is to  suggest a nutitious and flovouful Lunch based on the user's
    prefered cuisine type ,include all variety of foods that are possible from their cuisine ,suggest something that is nutritious 
    and tasty at the same time ,so that it easy and fun for person to achieve goal .
    you will be provided the details regarding the desired macronutrient to be provide by the Lunch ,so option provided by you 
    should ensure that person's macronutrient requirement are fulfilled.
    you will also be provided with person details regarding any allgeries , their prefered cuisine type and 
    their goal like whether they want to reduce weight , gain weight or maintain the weight ,as you are a nutritionist you will take 
    all this information into consideration while suggestting the best lunch option for them.
    If person want to loose weight don't suggest anything that will lead to gain weight for example Chole Bhature.
    Also you will provide them 3 option for their lunch , option1 will be budget friendly that is its price can be under 100 rupees,
    option2 can have price  100 to 200 rupees and option3 can cost anything over 220 rupees ,in option3 you can suggest
    those dishes in which the cost of ingredient used is high and nutrition value of the food is worth the money .
    Try macronutrient of all the the three option be somewhat similar if not same.
    The output that you will provide will consist of dish ,  cost , carbs, protein,calorie
    and fats.

    Following is the detail about the person:-
    A {g} wants that {carbs} gms of carbs,{protein} gms of protein ,{calorie} Kcal of calorie and {fats} gms of fats is
    provided by the lunch .
    Their goal is to {goal},is alergic to {allergies},eats only {veg} food and prefered cuisine type is {cuisine}.
    suggest lunch according to the cuisine type for the day so that person can fulfill their goal .
    REMEMBER these point while generating output.
    1.The output must be in json format i.e key value pair.
    2.The type of value will be a string it will have the name of the dish that should be eaten.
    3.Make sure each option should just have only one dish not more than that.
    4.provide averge cost  of making the dish in rupees . that also in json format ,type of cost value will be a number.
    5.provide carbs,protein,calorie and fats of the dish without units(kcal or gms) . that also in json format ,type of there value will be a number .
    
    following is example output ,make sure that the json is in this format and also  key should be in lowercase only.
    example output: 
    [
    "lunch":["option1":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option2":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option3":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5]
                ]


    ]
    """
    
    
    
    
     

    my_prompt=PromptTemplate(template=prompt_template,input_variables=["g","fats","calorie","protein","carbs","goal","allergies","veg","cuisine"])
    

    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=API_KEY,cache=False)

    chain=LLMChain(llm=llm,prompt=my_prompt,verbose=True)
    
    
    output=chain.run({"g":g,"fats":fats,"calorie":calorie,"protein":protein,"carbs":carbs,"goal":goal,"allergies":allergies,"veg":veg,"cuisine":cuisine})

    return output








def MacroDinnerplan(g,fats,calorie,protein,carbs,goal,allergies,veg,cuisine):
    """This function provides the Dinner taking macronutrients like carbs,protien,fatsand calorie as input"""


    prompt_template="""
    You are a nutritionist and a dietitian ,your job is to  suggest a nutitious and flovouful dinner based on the user's
    prefered cuisine type ,include all variety of foods that are possible from their cuisine ,suggest something that is nutritious 
    and tasty at the same time ,so that it easy and fun for person to achieve goal .
    you will be provided the details regarding the desired macronutrient to be provide by the dinner ,so option provided by you 
    should ensure that person's macronutrient requirement are fulfilled.
    you will also be provided with person details regarding any allgeries , their prefered cuisine type and 
    their goal like whether they want to reduce weight , gain weight or maintain the weight ,as you are a nutritionist you will take 
    all this information into consideration while suggestting the best dinner option for them.
    If person want to loose weight don't suggest anything that will lead to gain weight for example Chole Bhature, butter chicken 
    or anything that is not preffered to eat at night if person wants to reduce the weight.

    Also you will provide them 3 option for their dinner , option1 will be budget friendly that is its price can be under 100 rupees,
    option2 can have price  100 to 200 rupees and option3 can cost anything over 220 rupees ,in option3 you can suggest
    those dishes in which the cost of ingredient used is high and nutrition value of the food is worth the money .
    Try macronutrient of all the the three option be somewhat similar if not same.
    The output that you will provide will consist of dish ,  cost , carbs, protein,calorie
    and fats.

    Following is the detail about the person:-
    A {g} wants that {carbs} gms of carbs,{protein} gms of protein ,{calorie} Kcal of calorie and {fats} gms of fats is
    provided by the dinner .
    Their goal is to {goal},is alergic to {allergies},eats only {veg} food and prefered cuisine type is {cuisine}.
    suggest dinner according to the cuisine type for the day so that person can fulfill their goal .
    REMEMBER these point while generating output.
    1.The output must be in json format i.e key value pair.
    2.The type of value will be a string it will have the name of the dish that should be eaten.
    3.Make sure each option should just have only one dish not more than that.
    4.provide averge cost  of making the dish in rupees . that also in json format ,type of cost value will be a number.
    5.provide carbs,protein,calorie and fats of the dish without units(kcal or gms) . that also in json format ,type of there value will be a number .
    
    following is example output ,make sure that the json is in this format and also  key should be in lowercase only.
    example output: 
    [
    "dinner":["option1":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option2":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option3":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5]
                ]


    ]
    """
    
    
    
    
     

    my_prompt=PromptTemplate(template=prompt_template,input_variables=["g","fats","calorie","protein","carbs","goal","allergies","veg","cuisine"])
    

    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=API_KEY,cache=False)

    chain=LLMChain(llm=llm,prompt=my_prompt,verbose=True)
    
    
    output=chain.run({"g":g,"fats":fats,"calorie":calorie,"protein":protein,"carbs":carbs,"goal":goal,"allergies":allergies,"veg":veg,"cuisine":cuisine})

    return output




def MacroEveningsnackplan(g,fats,calorie,protein,carbs,goal,allergies,veg,cuisine):


    prompt_template="""
    You are a nutritionist and a dietitian ,you will be provided with person , allgeries ,cuisine type they prefer and 
    their goal gor example gain weight , lose weight and maintain weight . your job is to suggest evening Snack that person can have between lunch and dinner,
    snacks can't be a proper meal,For  evening snacks you can suggest things like  mango smoothie   or any other fruit smooties ,shakes,salad,cereal,fruits etc and you can try suggestting
    snack from their prefered cuisine type.you will be provided the details regarding the desired macronutrient to be provide by the Snack ,so option provided should ensure that
    person's macronutrient requirement are fulfilled.
    You will be suggesting healthy and nutritious snack for the person .as you are a nutritionist you will take all this information of the person into 
    consideration while suggesting the best snack option  for them.
    also if person wants to loose weight don't suggest things that can lead to increase in weight.
    Also you will provide them 3 option for their evening Snack , option1 will be budget friendly that is its price can be under 80 rupees,
    option2 can have price  100 to 150 rupees and option3 can cost anything over 170 rupees ,in option3 you can suggest
    those snack in which the cost of ingredient used is high and nutrition value is worth the money.
    try to include beverage in one of the option.
    .the output that you will provide will consist of dish ,  cost , carbs, protein,calorie
    and fats.

    Following is the detail about the person:-
    A {g} wants that {carbs} gms of carbs,{protein} gms of protein ,{calorie} Kcal of calorie and {fats} gms of fats is
    provided by the morning snack .
    Their goal is to {goal},is alergic to {allergies},eats only {veg} food and prefered cuisine type is {cuisine}.
    suggest snack according to the person detail for the day so that person can fulfill their goal and try macronutrients if not close should be somewhat similar to what user want.
    REMEMBER these point while generating output.
    1.The output must be in json format i.e key value pair.
    2.The type of value will be a string it will have the name of the dish that should be eaten.
    3.Make sure each option should just have only one dish not more than that.
    4.provide averge cost  of making the dish in rupees . that also in json format ,type of cost value will be a number.
    5.provide carbs,protein,calorie and fats of the dish without units(kcal or gms) . that also in json format ,type of there value will be a number .
    
    following is example output ,make sure that the json is in this format and also  key should be in lowercase only.
    that should strictly in json format ,no list or anything else.
    example output: 
    [
    "eveningsnack":["option1":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option2":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5],
                "option3":
                ["dish":"name",
                "cost":80,
                "carbs:20,
                "calorie:200,
                "fats:10,
                protein:5]
                ]


    ]
    """
    
    
    
    
     

    my_prompt=PromptTemplate(template=prompt_template,input_variables=["g","fats","calorie","protein","carbs","goal","allergies","veg","cuisine"])
    

    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=API_KEY,cache=False)

    chain=LLMChain(llm=llm,prompt=my_prompt,verbose=True)
    
    
    output=chain.run({"g":g,"fats":fats,"calorie":calorie,"protein":protein,"carbs":carbs,"goal":goal,"allergies":allergies,"veg":veg,"cuisine":cuisine})

    return output


def Recipe(dish):


    prompt_template="""
    Provide me the recipe or instruction to make following dish in only three points and intruction should be under 120 words.
   {dish}
    
    """


    my_prompt=PromptTemplate(template=prompt_template,input_variables=["dish"])
    

    llm=ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=API_KEY,cache=False)

    chain=LLMChain(llm=llm,prompt=my_prompt,verbose=True)
    
    
    output=chain.run({"dish":dish})

    return output
