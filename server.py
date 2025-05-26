from flask import Flask, render_template,request
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

#collection_link = client["budget"]["link_budget"]
#col_id = collection_id.find({})
#col_id = list(col_id)
#print(col_id)

#myresult = col_id

#headings = ["Id", "cpf", "phone_number", "name", "surname", "email", "date_request", "obs"]

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
    return render_template("index.html")

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

    #informar pagina que inseriu

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host= '192.168.20.5')
    #app.run(debug=True)

    #INSERT VALUE INTO MONGODB s

    # from pymongo import MongoClient
    # client = MongoClient("mongodb://localhost:27017")
    # collection_id = client["budget"]["id_budget"]
    # col_id = collection_id.find({})
    # col_id = list(col_id)
    # print(col_id)
    #
    # collection_info = client["budget"]["info_budget"]
    # col_info = collection_info.find({})
    # col_info = list(col_info)
    # print(col_info)
    #
    # collection_link = client["budget"]["link_budget"]
    # col_link = collection_link.find({})
    # col_link = list(col_link)
    # print(col_link)
    #

    # aggregate_info = {
    #     "cod_dep": "CWB",
    #     "cod_arr": "GRU",
    #     "ticket_type": 2,
    #     "adults": 1,
    #     "children": 0,
    #     "infants_in_seat": 0,
    #     "infants_on_lap": 0,
    #     "seating_class": 0,
    #     "date_dep": "2025/07/08",
    #     "date_ret": "2025/08/08",
    #     "price_searched": 500,
    #     "state": "INI",
    #     "number_budgets": 10,
    #     "id_budget": {
    #         "$oid": result.inserted_id
    #     },
    #     "obs": ""
    # }
    #
    # aggregate_link = {
    #     "price": [
    #         1,
    #         2
    #     ],
    #     "localization": [
    #         "o1",
    #         "o2"
    #     ],
    #     "client_summarize": [
    #         "oi1",
    #         "oi2"
    #     ],
    #     "complete_info": [
    #         "alot1",
    #         "alot2"
    #     ],
    #     "baggage": [
    #         "",
    #         ""
    #     ],
    #     "link": [
    #         "www1",
    #         "www2"
    #     ],
    #     "date_search": [
    #         "2025/05/20",
    #         "2025/05/20"
    #     ],
    #     "id_budget": {
    #         "$oid": result.inserted_id
    #     },
    #     "obs": [
    #         "",
    #         ""
    #     ]
    # }

    # result = collection_info.insert_one(aggregate_info)
    # print(f"Inserted document ID: {result.inserted_id}")
    # result = collection_link.insert_one(aggregate_link)
    # print(f"Inserted document ID: {result.inserted_id}")


