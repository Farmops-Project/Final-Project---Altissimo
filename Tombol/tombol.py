from flask import Flask, render_template, request
from ubidots import ApiClient

app = Flask(__name__)

# Ubah dengan token dan label yang sesuai dari Ubidots
API_TOKEN = "BBFF-thUhhRPJojoHiUB78bozuZuPy2dKTv"
LABEL = "64cb734bdfc2f3000b9aec5b"

api = ApiClient(token=API_TOKEN)
variable = api.get_variable(LABEL)

def toggle_value(current_value):
    if current_value == 0:
        return 1
    else:
        return 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        current_value = variable.get_values(1)[0]['value']
        new_value = toggle_value(current_value)
        variable.save_value({'value': new_value})

    current_value = variable.get_values(1)[0]['value']
    return render_template('index.html', current_value=current_value)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
from ubidots import ApiClient

app = Flask(__name__)

API_TOKEN = "BBFF-thUhhRPJojoHiUB78bozuZuPy2dKTv"
SLIDER_LABEL = "slider_value"
BUTTON_LABEL = "64cb734bdfc2f3000b9aec5b"

api = ApiClient(token=API_TOKEN)
slider_variable = api.get_variable(SLIDER_LABEL)
button_variable = api.get_variable(BUTTON_LABEL)

def toggle_value(current_value):
    return 1 - current_value

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'slider' in request.form:
            slider_value = int(request.form.get('slider'))
            slider_variable.save_value({'value': slider_value})

        if 'button' in request.form:
            current_button_value = button_variable.get_values(1)[0]['value']
            new_button_value = toggle_value(current_button_value)
            button_variable.save_value({'value': new_button_value})

    current_slider_value = slider_variable.get_values(1)[0]['value']
    current_button_value = button_variable.get_values(1)[0]['value']

    return render_template('index.html', current_slider_value=current_slider_value, current_button_value=current_button_value)

if __name__ == '__main__':
    app.run(debug=True)

