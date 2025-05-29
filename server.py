# from fastapi import FastAPI
from flask import Flask, render_template,request
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

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
airports = ["CWB", "GRU", "MAD"]
headings = ["", "Com retorno", "Só ida"]

client = MongoClient("mongodb://localhost:27017")
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
airport_search = {
    "location": location,
    "airport": airport,
    "iata_code": iata_code
}

today = datetime.today()
lastday = today.replace(year=today.year + 1)
today = today.strftime("%Y-%m-%d")
lastday = lastday.strftime("%Y-%m-%d")

def insert_id_info(name, surname, cpf, fone, email, cod_dep, cod_arr, ticket_type, adults, date_dep, date_ret):
    client = MongoClient("mongodb://localhost:27017")
    collection_id = client["budget"]["id_budget"]
    collection_info = client["budget"]["info_budget"]

    aggregate_id = {
        "name": name,
        "surname": surname,
        "cpf": cpf,
        "phone_number": fone,
        "email": email,
        "date_request": datetime.now(),
        "obs": "TESTE_WEB"
    }
    result = collection_id.insert_one(aggregate_id)
    #print(f"Inserted document ID: {result.inserted_id}")

    aggregate_info = {
        "cod_dep": cod_dep,
        "cod_arr": cod_arr,
        "ticket_type": ticket_type,
        "adults": adults,
        "children": 0,
        "infants_in_seat": 0,
        "infants_on_lap": 0,
        "seating_class": 0,
        "date_dep": date_dep,
        "date_ret": date_ret,
        "price_searched": 500,
        "state": "INITIAL",
        "number_budgets": 5,
        "id_budget": ObjectId(result.inserted_id),
        "obs": ""
    }

    result_info = collection_info.insert_one(aggregate_info)
    #print(f"Inserted document INFO: {result_info.inserted_id}")
    client.close()
    return result.inserted_id

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", headings=headings, airports=airport_search, today=today, lastday=lastday)

# SOLUTION to Challenge:
@app.route("/form-entry", methods=["POST"])
def receive_data():
    name = request.form["demo-name"]
    surname = request.form["demo-surname"]
    cpf = request.form["demo-cpf"]
    fone = request.form["demo-fone"]
    email = request.form["demo-email"]
    #print(f'name:{name}/{surname} - {cpf} - {fone} and email:{email}')

    cod_dep = request.form["demo-cod_dep"]
    cod_arr = request.form["demo-cod_arr"]
    ticket_type = request.form["demo-ticket_type"]
    adults = request.form["demo-adults"]
    date_dep = request.form["demo-date_dep"]
    date_ret = request.form["demo-date_ret"]
    #print(f'cod:{cod_dep}-{cod_arr} ticket: {ticket_type} adults: {adults} and date_dep:{date_dep}-{date_ret}')

    inserted = insert_id_info(name, surname, cpf, fone, email, cod_dep, cod_arr, ticket_type, adults, date_dep, date_ret)

    return render_template("index.html", headings=headings, airports=airport_search, today=today, lastday=lastday, alert=f"Orçamento {inserted}\nInserido com sucesso!")

if __name__ == "__main__":
    app.run(debug=True, host= '192.168.0.106')
    #app.run(debug=True)


