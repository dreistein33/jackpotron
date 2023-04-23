import base64
from flask import Flask, jsonify, render_template
import requests
import qrcode
from io import BytesIO

app = Flask(__name__, template_folder='templates', static_url_path="/static")
app.jinja_env.filters['datetimeformat'] = lambda value, format='%Y-%m-%d %H:%M:%S': value.strftime(format)


@app.route("/participants")
def wait_for_transaction():
    try:
        context = requests.get("http://localhost:5000/lotteries").json()
        for items in context:
            print(type(items['endtime']))
    except Exception as e:
        return jsonify({"error": e})

    return render_template("index.html", context_list=context)

    # Znajdowac w requescie txy ktore zawieraja sie w ramach czasowych loterii


@app.route("/jackpot")
def jackpot():
    return render_template("jackpot.html")

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/lottery/<id>")
def show_lottery_details(id):
    lottery = requests.get(f"http://localhost:5000/lottery/{id}").json()

    txs = lottery['users']   
    
    buffer = BytesIO()
    
    qr_data = f"tron:{lottery['address']}?token=TRX&amount={lottery['prize']}&note={lottery['id']}"
    qr = qrcode.QRCode(version=1, box_size=4, border=1)
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#F0B90B", back_color="#2c2c2c")
    img.save(buffer, format="PNG")
    qr_png = buffer.getvalue()
    qr_base64 = base64.b64encode(qr_png).decode()

    return render_template("lotto.html", lottery=lottery, txs=txs, qr=qr_base64)


if __name__ == "__main__":
    app.run(debug=True, port=4999)