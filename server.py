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

