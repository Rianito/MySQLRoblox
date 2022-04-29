from dotenv import dotenv_values
import pymysql.cursors
import json
from flask import Flask, request

envs = dotenv_values(".env")

# Flask Server


def conectar():
    connection = pymysql.connect(host=envs["IP"],
                                 user="rian",
                                 password=envs["PASSWORD"],
                                 database="simpleguy",
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def check_data(data):
    try:
        return False, int(data["Experience"]), int(data["Amount"])
    except KeyError or ValueError:
        return "Formato errado."


def create(userid, experience, amount):
    connection = conectar()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users VALUES (%s, %i, %i);",
                   (userid, experience, amount))
    connection.commit()
    connection.close()
    return load(userid)


def load(userid):
    connection = conectar()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE UserID = %s", (userid))
    connection.close()
    content = json.dumps(cursor.fetchone())
    if content == "null":
        return create(userid, 0, 0)
    return content


def save(userid, data):
    error, experience, amount = check_data(data)
    if error:
        return error
    if load(userid):
        connection = conectar()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET Experience = %i, Amount = %i WHERE UserID = %s",
            (experience, amount, userid))
        connection.commit()
        connection.close()
        return "Alterado com sucesso."


app = Flask("app")


@app.route("/user/<userid>", methods={"GET", "POST"})
def datastore(userid):

    if request.headers.get("Authorization") != envs["AUTH"]:
        return "Acesso Negado."

    if request.method == "GET":
        return load(userid)

    elif request.method == "POST":
        return save(userid, request.get_json())

    return "Erro no método."


app.run("localhost", 8000)
