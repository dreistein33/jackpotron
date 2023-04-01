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

    response = lottery_obj.__dict__

    emit("response", response, json=True, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, port=4998, debug=True)