import pandas as pd
from flask import Flask, render_template

app = Flask("__name__")

variable = "Hello World"

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID","STANAME                                 "]]



@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    # i am formatting station id to 6 digits
    filename = "data_small/" + str(station).zfill(6) + ".txt"

    # i am reading file and parsing date column
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    # i am filtering by date and converting temperature
    temperature = df.loc[df["    DATE"] == date]["   TG"].iloc[0] / 10

    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }


if __name__ == "__main__":
    app.run(debug=True)