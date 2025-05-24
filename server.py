from flask import Flask, render_template,request
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Ramon1306!", #AWSDB -> Ramon130694!
    database="price_trend"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM price_trend.test_gru")

myresult = mycursor.fetchall()

#plot_date_arr = []
#plot_min_prince = []
# for y in myresult:
#     plot_date_arr.append(y[4].strftime("%y-%m-%d"))
#     plot_min_prince.append(y[5])
#     #print(y)
#
# print(plot_date_arr)
# print(plot_min_prince)

plot_min_prince = ['248', '249', '237', '197', '225', '175', '174', '187', '232', '174', '11', '1']
plot_date_arr = plot_min_prince
headings = ["Id", "Cod_dep", "Cod_arr", "Date_Search", "Date_arr", "min_price", "med_price", "obs"]

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", headings=headings, data=myresult, plot_date_arr=plot_date_arr, plot_min_prince=plot_min_prince)

# SOLUTION to Challenge:
@app.route("/form-entry", methods=["POST"])
def receive_data():
    name = request.form["demo-name"]
    email = request.form["demo-email"]
    print(f'name:{name} and email:{email}')
    return render_template("index.html", headings=headings, data=myresult, plot_date_arr=plot_date_arr, plot_min_prince=plot_min_prince)

if __name__ == "__main__":
    #app.run(debug=True, host= '192.168.0.219')
    app.run(debug=True)

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
    # date_now = datetime.now()
    # aggregate_id = {
    #     "cpf": "05784025996",
    #     "phone_number": "+5541998277972",
    #     "name": "Ramon",
    #     "surname": "Pereira",
    #     "email": "ramoneesfp@gmail.com",
    #     "date_request": date_now,
    #     "obs": "TESTE"
    # }

    # result = collection_id.insert_one(aggregate_id)
    # print(f"Inserted document ID: {result.inserted_id}")

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


