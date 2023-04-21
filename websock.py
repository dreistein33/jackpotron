import db
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit 
import utils

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("data")
def get_data():
    db_obj = db.Database()
    db_lottery = db_obj.get_table_data('loteria')[-1]
    
    lottery_obj = utils.assembly_lottery_with_users(db_obj, db_lottery['id'])
    lottery_obj.format_userlist()

    qr = utils.generate_qr(lottery_obj.address, 0, lottery_obj.id)

    response = lottery_obj.__dict__
    response["qrcode"] = qr

    emit("response", response, json=True, broadcast=True)


@socketio.on("history")
def get_history():
    db_obj = db.Database()
    lotteries = db_obj.get_table_data('loteria')

    emit("last", lotteries, json=True, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, port=4998, debug=True)