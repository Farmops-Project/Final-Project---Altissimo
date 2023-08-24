from flask import Flask, render_template, request
from ubidots import ApiClient

app = Flask(__name__)

# Ubah dengan token dan label yang sesuai dari Ubidots
API_TOKEN = "BBFF-thUhhRPJojoHiUB78bozuZuPy2dKTv"
LABEL_LAMPU = "64cb734bdfc2f3000b9aec5b"
LABEL_KIPAS = "64cc7d13b2f3f5000e41c9d1"
#Kalo mau nambah lagi tinggal tambah label

api = ApiClient(token=API_TOKEN)
variable_lampu = api.get_variable(LABEL_LAMPU)
variable_kipas = api.get_variable(LABEL_KIPAS)
#kalo mau nambah label, variablenya juga nambah

def toggle_value(current_value):
    if current_value == 0:
        return 1
    else:
        return 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        current_value = variable_lampu.get_values(1)[0]['value'] #buat update status tombol lampu
        current_value2 = variable_kipas.get_values(1)[0]['value'] #buat update status tombol kipas
        
        if request.form['button'] == 'toggle': #tombol pertama
            new_value = toggle_value(current_value)
            variable_lampu.save_value({'value': new_value}) #kirim nilai tombol lampu

        if request.form['button'] == 'toggle2': #tombol kedua
            new_value2 = toggle_value(current_value2)
            variable_kipas.save_value({'value': new_value2}) #kirim nilai tombol kipas

    current_value = variable_lampu.get_values(1)[0]['value']
    current_value2 = variable_kipas.get_values(1)[0]['value']
    return render_template('index.html', current_value=current_value, current_value2=current_value2)

#kalo beda halaman dan beda file html, bikin route baru kaya gini :
# @app.route('/', methods=['GET', 'POST']) <= yang "/" ganti sesuai nama halaman, misal '/Agenda'
#def index():

if __name__ == '__main__':
    app.run(debug=True)
