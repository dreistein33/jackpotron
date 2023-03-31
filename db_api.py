from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import db 
import utils

app = Flask(__name__)
CORS(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits= ["12 per minute"]
)


@app.route("/lotteries")
def get_lotteries():
    db_obj = db.Database()
    lotteries = db_obj.get_table_data('loteria', {"status": "'started'"})
    return jsonify(lotteries)


@app.route("/lottery/<id>")
def get_lottery(id):
    db_obj = db.Database()
    lottery_obj = utils.assembly_lottery_with_users(db_obj, id)
    return jsonify(lottery_obj.__dict__)

@app.route("/jackpot")
@limiter.limit("21 per minute")
def get_jackpot():
    db_obj = db.Database()
    lottery = db_obj.get_table_data('loteria', {"status": "'started'"})[0]
    lottery_obj = utils.assembly_lottery_with_users(db_obj, lottery['id'])
    lottery_obj.format_userlist()

    return jsonify(lottery_obj.__dict__)


if __name__ == "__main__":
    app.run(debug=True)
