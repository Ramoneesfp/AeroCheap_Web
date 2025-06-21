# from fastapi import FastAPI
from flask import Flask, render_template,request
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import certifi
from backend import setupdata

ca = certifi.where()
import re

########                         TO DO LIST
########  ARRUMAR TODOS OS TEXTOS
########  NAO PERMITIR OUTRO VALOR NA ORIGEM QUE NAO ESTEJA NA LISTA - tem uma condição (FAZER NO SERVER GERANDO ERRO)
########  TESTE COM IOS (DATA e PAISES NAO ESTAO FUMENGANDO) - NAO FUNCIONA MESMO
########  CRIAR BOX OCULTA COM ADULTOS, CRIANCAS
########  REMOVER DATA DE RETORNO QUANDO SO IDA -> DEU BOA, SO FALTA ZERAR VALOR
########  ADICIONAR DDD NO TELEFONE - adicionar todos paises e flag

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
list_DDD = ["+55"]

today = datetime.today()
lastday = today.replace(year=today.year + 1)
today = today.strftime("%Y-%m-%d")
lastday = lastday.strftime("%Y-%m-%d")
########## CLIENTE CONNECTION
#client = MongoClient("mongodb://localhost:27017")
client = MongoClient(setupdata.DATABASE_USER)

def get_price():
    price = client["trend"]["price"]
    id = "684a3da2705094775c209bdf"
    update_price = price.find({"id_budget": ObjectId(id)})
    update_price = list(update_price)

    location = []
    date_search = []
    date_input = []
    price = []

    for key, value in update_price[0].items():
        # print(f"Key: {key}")
        if "-" in key:
            location.append(key)
        if isinstance(value, dict):
            # print("  Sub-dictionary:")
            for sub_key, sub_value in value.items():
                split = sub_key.split("/")
                date_search.append(f"{split[2]}/{split[1]}")
                if isinstance(sub_value, dict):
                    for sub_sub_key, sub_sub_value in sub_value.items():
                        aux_time = datetime.strptime(sub_sub_key, "%Y/%m/%d")
                        date_input.append(f"{aux_time.day}/{aux_time.month}")
                        price.append(sub_sub_value)
                else:
                    pass
        else:
            pass

    # print(location)
    # print(date_search)
    # print(f"{len(date_input)}-{date_input}")
    # print(f"{len(price)}-{price}")
    # print(update_price[0][location[0]][date_search[0]])

    return location, list(set(date_search)), update_price[0]

def get_airport(cod):
    collection_id = client["budget"]["airports"]
    col_id = collection_id.find({})
    #col_id = list(col_id)
    location = ""
    airport = ""
    iata_code = ""
    pais = ""
    for i in col_id:
        aux = i["location"]
        location += aux
        aux = i["airport"]
        airport += aux
        aux = i["iata_code"]
        iata_code += aux
        aux = i["pais"]
        pais += aux
    location = location.split(";")
    airport = airport.split(";")
    iata_code = iata_code.split(";")
    pais = pais.split(";")
    # print(f'{len(location)} - {location}')
    # print(f'{len(airport)} - {airport}')
    # print(f'{len(iata_code)} {type(iata_code[1002])} - {iata_code}')
    #client.close()
    if cod == "":
        airport_search = {
            "location": location,
            "airport": airport,
            "iata_code": iata_code,
            "pais": pais
        }
        return airport_search
    else:
        codes = []
        for c in cod:
            codes.append(iata_code[location.index(c)])
        return codes

def insert_id_info(name, surname, cpf, fone, email, dep, arr, ticket_type, date_dep, date_ret, adults, children, seats, laps, price, obs):
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

    aggregate_info = {
        "cod_dep": dep,
        "cod_arr": arr,
        "ticket_type": ticket_type,
        "adults": int(adults),
        "children": int(children),
        "infants_in_seat": int(seats),
        "infants_on_lap": int(laps),
        "seating_class": 0,
        "date_dep": date_dep,
        "date_ret": date_ret,
        "price_searched": price,
        "state": "INITIAL",
        "number_budgets": 10,
        "payment": "NOT",
        "id_budget": ObjectId(result.inserted_id),
        "obs": obs
    }

    result_info = collection_info.insert_one(aggregate_info)
    #print(f"Inserted document INFO: {result_info.inserted_id}")
    #client.close()
    return result.inserted_id

app = Flask(__name__)

@app.route("/")
def home():
    airport_search = get_airport("")
    #print(airport_search)
    #airport_search = ["CWB", "GRU", "MAD"]
    return render_template("index.html", list_ticket_type=list_ticket_type, list_DDD=list_DDD, airports=airport_search, today=today, lastday=lastday)

@app.route("/graph")
def graph():
    location = []
    date_search = ""
    location, date_search, everything = get_price()
    return render_template("graph.html", location=location, date_search=date_search, everything=everything)

# SOLUTION to Challenge:
@app.route("/form-entry", methods=["POST"])
def receive_data():
    name = request.form["demo-name"]
    surname = request.form["demo-surname"]
    cpf = request.form["demo-cpf"]
    cpf = re.sub(r'\D', '', cpf)
    fone = request.form["demo-fone"]
    fone = re.sub(r'\D', '', fone)
    ddd = request.form["demo-ddd"]
    fone = f"{ddd}{fone}"
    email = request.form["demo-email"]
    #print(f'name:{name}/{surname} - {cpf} - {fone} and email:{email}')
    dep = request.form["demo-cod_dep"].upper()
    arr = request.form["demo-cod_arr"].upper()
    ticket_type = request.form["demo-ticket_type"]
    date_dep = request.form["demo-date_dep"]
    date_ret = request.form["demo-date_ret"]
    adults = request.form["demo-adults"]
    children = request.form["demo-children"]
    seats = request.form["demo-seats"]
    laps = request.form["demo-laps"]
    price = request.form["demo-price"]
    obs = request.form["demo-message"]
    #print(f'cod:{cod_dep}-{cod_arr} ticket: {ticket_type} adults: {adults} and date_dep:{date_dep}-{date_ret}')

    inserted = insert_id_info(name, surname, cpf, fone, email, dep, arr, ticket_type, date_dep, date_ret, adults, children, seats, laps, price, obs)

    airport_search = get_airport("")
    return render_template("index.html", list_ticket_type=list_ticket_type, list_DDD=list_DDD, airports=airport_search, today=today, lastday=lastday, alert=f"Orçamento {inserted}\nInserido com sucesso!")

if __name__ == "__main__":
    #app.run(debug=True, host= '192.168.0.105')
    app.run(debug=True, host='0.0.0.0', port=10000) #RUN IN RENDER
    #app.run(debug=True)


