from flask import Flask

from flask import render_template
from flask import request

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

with open('rates.csv', 'r', encoding='utf-8') as csvfile:
    tab = [list(wiersz.split(";")) for wiersz in csvfile]


@app.route('/', methods=['GET', 'POST'])
def convert():
    if request.method == 'GET':
        print("We received GET")
        return render_template("calculate.html")
    elif request.method == 'POST':
        for row in tab:
            for elem in row:
                if elem == request.form["currency"]:
                    if request.form["operation"] == "buying":
                        ask = row[3]
                        value = str(float(ask) * int(request.form["quantity"])) + " PLN"
                        return value
                    elif request.form["operation"] == "sales":
                        bid = row[2]
                        value = str(float(bid) * int(request.form["quantity"])) + " PLN"
                        return value


if __name__ == '__main__':
    app.run(debug=True)
