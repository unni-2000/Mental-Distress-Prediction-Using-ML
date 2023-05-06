from flask import Flask , render_template , request

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')
@app.route('/submit', methods=['POST'])
def submit():
   range_values = request.form.getlist('rangeInputs[]')
   return f'The range values are {range_values}'
if __name__ == '__main__':
   app.run(debug=True)