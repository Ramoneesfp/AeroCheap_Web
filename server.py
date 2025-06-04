# from fastapi import FastAPI
from flask import Flask, render_template,request
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
return 1
#python -m pip install "pymongo[srv]"==3.12
#60.50.13.209
#ramoneesfp
#99zWyq8YuA6aPDPO
#mongodb+srv://ramoneesfp:99zWyq8YuA6aPDPO@aerocheapteste.0myx5m8.mongodb.net/?retryWrites=true&w=majority&appName=AeroCheapTESTE
#91189e08c8723fede58866e0f6108ffe8ea26a8508d86b1c9b4a2fcbb3bd25a8e5d6218b790081ffde0d2fd2cc2286a4 # API

# app = FastAPI()
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
# app.get("/hello/{name}")
# async def say_hello:
#     return {"message": f"Hello {name}"}

#headings = ["Id", "cpf", "phone_number", "name", "surname", "email", "date_request", "obs"]
#airports = ["CWB", "GRU", "MAD"]
list_ticket_type = ["Com retorno", "Só ida - Só volta"]

today = datetime.today()
lastday = today.replace(year=today.year + 1)
today = today.strftime("%Y-%m-%d")
lastday = lastday.strftime("%Y-%m-%d")

def get_airport(cod):
    client = MongoClient("mongodb+srv://ramoneesfp:99zWyq8YuA6aPDPO@aerocheapteste.0myx5m8.mongodb.net/?retryWrites=true&w=majority&appName=AeroCheapTESTE")
    collection_id = client["budget"]["airports"]
    col_id = collection_id.find({})
    #col_id = list(col_id)
    location = ""
    airport = ""
    iata_code = ""
    for i in col_id:
        aux = i["location"]
        location += aux
        aux = i["airport"]
        airport += aux
        aux = i["iata_code"]
        iata_code += aux
    location = location.split(";")
    airport = airport.split(";")
    iata_code = iata_code.split(";")
    # print(f'{len(location)} - {location}')
    # print(f'{len(airport)} - {airport}')
    # print(f'{len(iata_code)} {type(iata_code[1002])} - {iata_code}')
    client.close()
    if cod == "":
        airport_search = {
            "location": location,
            "airport": airport,
            "iata_code": iata_code
        }
        return airport_search
    else:
        codes = []
        for c in cod:
            codes.append(iata_code[location.index(c)])
        return codes

def insert_id_info(name, surname, cpf, fone, email, cod_dep, cod_arr, ticket_type, adults, date_dep, date_ret, obs):
    client = MongoClient("mongodb+srv://ramoneesfp:99zWyq8YuA6aPDPO@aerocheapteste.0myx5m8.mongodb.net/?retryWrites=true&w=majority&appName=AeroCheapTESTE")
    collection_id = client["budget"]["id_budget"]
    collection_info = client["budget"]["info_budget"]

    aggregate_id = {
        "name": name,
        "surname": surname,
        "cpf": cpf,
        "phone_number": fone,
        "email": email,
        "date_request": datetime.now(),
        "obs": obs
    }
    result = collection_id.insert_one(aggregate_id)
    #print(f"Inserted document ID: {result.inserted_id}")

    list_ticket_type = ["Com", "Só"]
    ticket_type = list_ticket_type.index(ticket_type)+1
    #print(f"index ticket_type: {ticket_type}")

    if ticket_type == 2:
        number_budgets = 5
    else:
        number_budgets = 10

    aggregate_info = {
        "cod_dep": cod_dep,
        "cod_arr": cod_arr,
        "ticket_type": ticket_type,
        "adults": int(adults),
        "children": 0,
        "infants_in_seat": 0,
        "infants_on_lap": 0,
        "seating_class": 0,
        "date_dep": date_dep,
        "date_ret": date_ret,
        "price_searched": 500,
        "state": "INITIAL",
        "number_budgets": number_budgets,
        "id_budget": ObjectId(result.inserted_id),
        "obs": obs
    }

    result_info = collection_info.insert_one(aggregate_info)
    #print(f"Inserted document INFO: {result_info.inserted_id}")
    client.close()
    return result.inserted_id

app = Flask(__name__)

@app.route("/")
def home():
    airport_search = get_airport("")
    #airport_search = ["CWB", "GRU", "MAD"]
    return render_template("index.html", list_ticket_type=list_ticket_type, airports=airport_search, today=today, lastday=lastday)

# SOLUTION to Challenge:
@app.route("/form-entry", methods=["POST"])
def receive_data():
    name = request.form["demo-name"]
    surname = request.form["demo-surname"]
    cpf = request.form["demo-cpf"]
    fone = request.form["demo-fone"]
    email = request.form["demo-email"]
    #print(f'name:{name}/{surname} - {cpf} - {fone} and email:{email}')

    dep = request.form["demo-cod_dep"]
    arr = request.form["demo-cod_arr"]
    ticket_type = request.form["demo-ticket_type"]
    adults = request.form["demo-adults"]
    date_dep = request.form["demo-date_dep"]
    date_ret = request.form["demo-date_ret"]
    obs = request.form["demo-message"]
    #print(f'cod:{cod_dep}-{cod_arr} ticket: {ticket_type} adults: {adults} and date_dep:{date_dep}-{date_ret}')

    cods = []
    cods = get_airport([dep, arr])
    cod_dep = cods[0]
    cod_arr = cods[1]

    inserted = insert_id_info(name, surname, cpf, fone, email, cod_dep, cod_arr, ticket_type, adults, date_dep, date_ret, obs)

    airport_search = get_airport("")
    return render_template("index.html", list_ticket_type=list_ticket_type, airports=airport_search, today=today, lastday=lastday, alert=f"Orçamento {inserted}\nInserido com sucesso!")

if __name__ == "__main__":
    #app.run(debug=True, host= '192.168.0.105')
    app.run(debug=True, host='0.0.0.0', port=10000) #RUN IN RENDER
    #app.run(debug=True)


