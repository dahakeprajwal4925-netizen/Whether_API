import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

# i am reading stations file
stations = pd.read_csv("data_small/stations.txt", skiprows=17)

# i am cleaning column names (removes extra spaces)
stations.columns = stations.columns.str.strip()

# i am selecting only required columns
stations = stations[["STAID", "STANAME"]]


@app.route("/")
def home():
    # i am converting dataframe to html
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def get_data(station, date):
    # i am formatting station id to 6 digits
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    # i am reading file
    df = pd.read_csv(filename, skiprows=20)

    # i am cleaning column names
    df.columns = df.columns.str.strip()

    # i am converting date column to string
    df["DATE"] = df["DATE"].astype(str)

    # i am filtering by date
    filtered = df[df["DATE"] == date]

    # i am checking if data exists
    if filtered.empty:
        return {"error": "No data found"}

    # i am converting temperature
    temperature = filtered["TG"].iloc[0] / 10

    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }


@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(filename, skiprows=20)

    # i am cleaning column names
    df.columns = df.columns.str.strip()

    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def yearly_data(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(filename, skiprows=20)

    # i am cleaning column names
    df.columns = df.columns.str.strip()

    # i am converting date column to string
    df["DATE"] = df["DATE"].astype(str)

    # i am filtering by year
    filtered = df[df["DATE"].str.startswith(str(year))]

    return filtered.to_dict(orient="records")


if __name__ == "__main__":
    app.run()