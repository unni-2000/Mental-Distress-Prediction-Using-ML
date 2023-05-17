from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from keras.models import load_model
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site1.db'
db = SQLAlchemy(app)
s_model = load_model('s_model.h5')
anx_model = load_model('anx_model.h5')
dep_model = load_model('depre_model.h5')

class User(db.Model):
   
   db_date = db.Column(db.DateTime, default = datetime.utcnow)
   id = db.Column(db.String,nullable = False, primary_key = True)
   db_stress = db.Column(db.String , nullable = False)
   db_anxty = db.Column(db.String , nullable = False)
   db_deptrn = db.Column(db.String , nullable = False)

   def __repr__(self):
      return '<Task %r>' % self.id
      
@app.route('/')
def index():
   return render_template('index.html')
@app.route('/submit', methods=['POST'])

def submit():
   r_values =[]
   range_values = request.form.getlist('rangeInputs[]')  
   us_id = request.form.get('user_emp_id')  
   for num in range_values:
      r_values.append(int(num))
   Sprdict_values = np.array([r_values[0:10]])
   Sprediction = s_model.predict(Sprdict_values)
   if np.argmax(Sprediction) == 0:
      s_var = 'Low stress' 
   elif np.argmax(Sprediction) == 1:
      s_var = 'mild stress'
   else :
      s_var = 'sever stress'
   Aprdict_values = np.array([r_values[10:17]])
   Aprediction = anx_model.predict(Aprdict_values)
   if np.argmax(Aprediction) == 0:
      a_var =  'Minimal anxiety'
   elif np.argmax(Aprediction) == 1:
      a_var =  'Mild anxiety'
   elif np.argmax(Aprediction) == 2:
      a_var =  'moderate anxiety'
   else:
      a_var = 'Sever anxiety'
   Dprdict_values = np.array([r_values[17:26]])
   Dprediction = dep_model.predict(Dprdict_values)
   if np.argmax(Dprediction) == 0:
      d_var = 'Low depression'
   elif np.argmax(Dprediction) == 1:
      d_var = 'Mild depresion'
   elif np.argmax(Dprediction) == 2:
      d_var = 'Moderate depresion'
   elif np.argmax(Dprediction) == 3:
      d_var = 'Moderately severe depresion'
   else:
      d_var = 'Severe depresion'
   #return f'The person have  {s_var} , {a_var} and {d_var}'
   new_task = User(id = us_id,db_stress = s_var, db_anxty= a_var, db_deptrn = d_var) 
   try:
      db.session.add(new_task)
      db.session.commit()
      return redirect('index.html', prediction_text='The person view in db with id {} have :{},{} and {}'.format(us_id,s_var,a_var,d_var))
   except:
      return render_template('index.html', prediction_text='The person with id {} have :{},{} and {}'.format(us_id,s_var,a_var,d_var))
if __name__ == '__main__':
   app.run(debug=True)