from flask import Flask, render_template, request
import requests
import time

app = Flask(__name__)

# Masukkan token dan ID Variable dari Ubidots di bawah ini
TOKEN = "BBFF-thUhhRPJojoHiUB78bozuZuPy2dKTv"
DEVICE_LABEL = "farmops"
VARIABLE_LABEL_1 = "test-tombol"

# Status default ketika aplikasi pertama kali dijalankan
status = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    global status
    if request.method == 'POST':
        status = 1 - status  # Toggle status antara 0 dan 1

    return render_template('index.html', status=status)

def build_payload(variable_1):

    tombol = 1
    
    payload = {
        variable_1: tombol
    }
    return payload

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1)
    print(payload)
    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")

if __name__ == '__main__':
    app.run(debug=True)
