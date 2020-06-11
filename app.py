from flask import Flask
from flask import render_template, request

import csv
import requests

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

currency = response.json()[0]["rates"]
# print(currency)

with open('rates.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["currency", "code", "bid", "ask"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    for row in currency:
        writer.writerow(row)

code = []

for row in currency:
    code.append(row["code"])

currency_code = {c: t for (c, t) in zip(code, currency)}


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/calculate', methods=['GET', 'POST'])
def convert():
    if request.method == 'GET':
        print("We received GET")
        return render_template("calculate.html")
    elif request.method == 'POST':
        if request.form["operation"] == "buying":
            ask = currency_code[request.form["currency"]]["ask"]
            value = str(float(ask) * int(request.form["quantity"])) + "PLN"
            return render_template("calculate_value.html", result=value)
        elif request.form["operation"] == "sales":
            bid = currency_code[request.form["currency"]]["bid"]
            value = str(float(bid) * int(request.form["quantity"])) + "PLN"
            return render_template("calculate_value.html", result=value)

if __name__ == '__main__':
    app.run(debug=True)
