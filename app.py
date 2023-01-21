from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)



class Phonenos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    phonenumber = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.name} - {self.phonenumber}"
        



@app.route('/')
def index():
    return 'Use http://127.0.0.1:5000/addno to add a number or http://127.0.0.1:5000/getphoneno/<name of the contact> to get the specific contact or http://127.0.0.1:5000/allnos to get all the numbers'




@app.route('/getphoneno/<string:str>' , methods=['GET'])
def get_phoneno(str):
    found = Phonenos.query.filter_by(name = str).first()
    return jsonify({
        'name' : found.name,
        'phonenumber' : found.phonenumber
        })
        
@app.route('/addno' , methods = ['POST','GET'])
def add_no():
    if request.method == 'POST':
        str = request.form.get('name')
        no = request.form.get('no')
        new_contact = Phonenos(name = str , phonenumber = no)

        try:
            db.session.add(new_contact)
            db.session.commit()
            return 'Successfully added the contact of '+str+ ' !'
        
        except:
            return 'Unable to add the contact'

    else:
        return render_template('base.html')

@app.route('/allnos')
def get_allnos():
    all_nos = Phonenos.query.all()
    numbers=[]
    for no in all_nos:
        numbers.append({
            'name' : no.name,
            'phonenumber' : no.phonenumber
            })
    return jsonify(numbers)
        










if __name__ == '__main__':
    app.run(debug=True)