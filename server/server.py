from flask import Flask, abort
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.json_util import dumps
from api_requests.team_requests import get_stats_gameweek, get_teams, get_teams_stats
import configparser

config = configparser.ConfigParser()
app = Flask(__name__)


def __get_creds():
    config.read('creds.ini')
    username = config['CREDS']['username']
    password = config['CREDS']['password']
    return (username, password)


def _connect():
    username, password = __get_creds()
    client = None
    try:
        uri = 'mongodb+srv://{username}:{password}@epl.oysq8wl.mongodb.net/?retryWrites=true&writeConcern=majority'.format(
            username=username, password=password)
        client = MongoClient(uri, server_api=ServerApi('1'))
    except Exception as e:
        print('Error connecting to the database:', e)
    finally:
        return client


@app.route('/teams')
def get_teams_request():
    if client := _connect() is None:
        abort(502)
    cursor = get_teams(client)
    response = dumps(list(cursor))
    return response


@app.route('/teams_stats')
def get_teams_stats_request():
    if client := _connect() is None:
        abort(502)
    cursor = get_teams_stats(client)
    response = dumps(list(cursor))
    return response


@app.route('/teams_stats_byGameweek')
def get_stats_gameweek_request():
    if client := _connect() is None:
        abort(502)
    cursor = get_stats_gameweek(client)
    response = dumps(list(cursor))
    return response


if __name__ == '__main__':
    app.run(port=4000)
