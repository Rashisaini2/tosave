from flask import Flask,render_template,request,redirect
from models import db,StudentModel
from os import abort

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
 
@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':

        Roll_id = request.form['Roll_id']
        name = request.form['name']
        branch = request.form['branch']
        batch = request.form['batch']
        email = request.form['email']
        dob = request.form['dob']

        student = StudentModel(
            Roll_id=Roll_id,
            name=name,
            branch=branch,
            batch=batch,
            email=email,
            dob=dob
        )
    
        db.session.add(student)
        db.session.commit()
        return render_template('success.html')
 
 
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/')
def RetrieveList():
    students = StudentModel.query.all()
    return render_template('datalist.html',students = students)
 

# @app.route('/<int:id>')
# def RetrieveStudent(id):
#     students = StudentModel.query.filter_by(id=id).first()
#     if students:
#         return render_template('data.html', students = students)
#     return f"Employee with id ={id} Doenst exist"
 
@app.route('/data/<int:id>')
def RetrieveStudent(id):
    student =StudentModel.query.filter_by(Roll_id=id).first()
    if student:
        return render_template('data.html',student=student)
    return f"Student with id ={id} Doesn't exist"  


@app.route('/data/<int:id>/edit',methods = ['GET','POST'])
def update(id):
    student = StudentModel.query.filter_by(Roll_id=id).first()

    #hobbies = student.hobbies.split(' ')
    # print(hobbies)
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            name = request.form['name']
            branch = request.form['branch']
            batch = request.form['batch']
            email = request.form['email']
            dob = request.form['dob']
            student = StudentModel(
            Roll_id=id,
            name=name,
            branch=branch,
            batch=batch,
            email=email,
            dob=dob)
            db.session.add(student)
            db.session.commit()
            return redirect('/success')
            return redirect(f'/data/{id}')
        # return redirect('/')
        return f"Student with id = {id} Does not exist"
 
    return render_template('update.html', student = student)
 

@app.route('/success')
def success():
    student = StudentModel.query.all()
    return render_template('success.html',student=student)


@app.route('/data/<int:id>/delete', methods=['GET','POST'])
@staticmethod
def delete(id):
    student = StudentModel.query.filter_by(Roll_id=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            return redirect('/success')
        abort(404)
     #return redirect('/')
    return render_template('delete.html')

 
# app.run(host='localhost', port=5000,debug=True)