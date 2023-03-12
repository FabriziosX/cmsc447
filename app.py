#from crypt import methods
from ast import Delete
from asyncio.windows_events import NULL
from genericpath import exists
from queue import Empty

from re import I
from tokenize import Name
from unicodedata import name
from urllib import request
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "Secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

courses_student = db.Table('courses_student',
    db.Column('courses_id', db.Integer, db.ForeignKey('courses.id')),
    db.Column('students_id', db.Integer, db.ForeignKey('students.id'))
)

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    instructors_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))

    enrolled = db.relationship('Students', secondary=courses_student, backref = 'courses')

    def __init__(self, Name, id): 
        self.id = id
        self.Name = Name

class Students(db.Model): 

    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Credits = db.Column(db.Integer, nullable=True)

    def __init__(self, Name, id, Credits):
        self.Name = Name
        self.id = id
        self.Credits = Credits

class Instructor(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Department = db.Column(db.String(55), nullable=True)
    courses = db.relationship('Courses', backref="instructor")
    
    def __init__(self, Name, id, Department):
        self.Name = Name
        self.id = id
        self.Department = Department


@app.route('/')
def Index():
    return render_template("Menu.html")
@app.route('/CourseIndex')
def CourseIndex():
    all_data = Courses.query.all()
    return render_template("Course.html", CoursesData = all_data)
@app.route('/InstructorIndex')
def InstructorIndex():
    all_data = Instructor.query.all() 
    return render_template("Instructor.html", InstructorData = all_data)
@app.route('/StudentIndex')
def StudentIndex():
    all_data = Students.query.all()
    return render_template("Student.html", studentData = all_data)

#-------------------------------------------------------------------------------
#                                    Courses
#-------------------------------------------------------------------------------insert
@app.route('/Courseinsert', methods=['POST'])
def Courseinsert():
    if request.method == 'POST':
        id = request.form['CourseID']
        title = request.form['Title']
        InstID = request.form['InstructorFile']

        Chk_ID = Instructor.query.filter_by(id=InstID).first()
        if InstID != "" and Chk_ID == None:
            flash('Instructor Does Not exist, Please try agian!')
            return redirect(url_for('CourseIndex'))
    my_Data = Courses(title, id)
    if InstID != "":
        my_Data.instructor = Chk_ID 
    else:
        my_Data.instructor = None 
    db.session.add(my_Data)
    db.session.commit()
    flash('Course was successfully added!')
    return redirect(url_for('CourseIndex'))
#-------------------------------------------------------------------------------AddDrop
@app.route('/AddStudent/<id>/', methods=['POST'])
def AddStudent(id):
    my_Data = Courses.query.get(id)
    if request.method == 'POST':
        Add_student = request.form['Add_Student']
        Chk_AddStudent = Students.query.filter_by(id = Add_student).first()
        if Chk_AddStudent != None :
            if my_Data.instructor == None:
                flash("You must first assign an Instructor before adding a student!")
                return redirect(url_for('CourseIndex'))
            my_Data.enrolled.append(Chk_AddStudent)
            db.session.commit()
            flash("Succeffuly Added!")
            return redirect(url_for('CourseIndex'))
            
        
        flash('student does NOT exist, please try again')
        return redirect(url_for('CourseIndex'))

@app.route('/DropStudent/<id>/<StudentID>/')
def DropStudent(id, StudentID):
    my_Data = Courses.query.get(id)
    Drop_Student = Students.query.get(StudentID)

    my_Data.enrolled.remove(Drop_Student)
    db.session.commit()
    flash("Succeffuly removed Student!")
    return redirect(url_for('CourseIndex'))
        


#-------------------------------------------------------------------------------Update
@app.route('/CourseUpdate', methods = ['GET','POST'])
def CourseUpdate():
    if request.method == 'POST':
        my_Data = Courses.query.get(request.form.get('id'))
        
        my_Data.Name = request.form['Title']
        my_Data.id = request.form['CourseID']
        my_Data.InstructorID = request.form['InstructorFile']
        
        Chk_ID = Instructor.query.filter_by(id=my_Data.InstructorID).first()
        if my_Data.InstructorID == '000' or my_Data.InstructorID == "" :
            if not my_Data.enrolled:
                my_Data.instructor = None
                db.session.commit()
                flash('Removed current instruction!')
                return redirect(url_for('CourseIndex'))
            else:
                flash('You must first Remove all Student!')
                return redirect(url_for('CourseIndex'))
        if Chk_ID == None:
            flash('Instructor does Not exist, please try again!')
            return redirect(url_for('CourseIndex'))
        
        my_Data.instructor = Chk_ID 
        db.session.add(my_Data)
        db.session.commit()
        flash('Instructor was successfully updated!')
        return redirect(url_for('CourseIndex'))

#-------------------------------------------------------------------------------Deleter
@app.route('/CourseDeleter/<id>/')
def CourseDeleter(id):
    my_Data = Courses.query.get(id)

    if my_Data.instructors_id == None:
        db.session.delete(my_Data)
        db.session.commit()
        return redirect(url_for('CourseIndex'))

    flash('Course is currently populated with  or instructor!')
    return redirect(url_for('CourseIndex'))



#-------------------------------------------------------------------------------
#                                    Students
#-------------------------------------------------------------------------------
@app.route('/Deleter/<id>/')
def Deleter(id):
    my_Data = Students.query.get(id)
    db.session.delete(my_Data)
    db.session.commit()
    return redirect(url_for('StudentIndex'))

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['Name']
        id = request.form['ID']
        Credits = request.form['Credit Earned']

    my_Data = Students(name, id, Credits)
    db.session.add(my_Data)
    db.session.commit()
    
    return redirect(url_for('StudentIndex'))

@app.route('/update', methods = ['GET','POST'])
def update():
    if request.method == 'POST':
        my_Data = Students.query.get(request.form.get('id'))
        my_Data.Name = request.form['name']
        my_Data.id = request.form['ID']
        my_Data.Credits = request.form['Credit Earned']
        db.session.commit()
        
        return redirect(url_for('StudentIndex'))

#-------------------------------------------------------------------------------
#                                    Instructor
#-------------------------------------------------------------------------------
@app.route('/InstructorInsert', methods=['POST'])
def InstructorInsert():
    if request.method == 'POST':
        name = request.form['Name']
        id = request.form['InstructorID']
        Department = request.form['Department']

    my_InstrutorData = Instructor(name, id, Department)
    db.session.add(my_InstrutorData)
    db.session.commit()
    
    return redirect(url_for('InstructorIndex'))

@app.route('/InstructorDeleter/<id>/')
def InstructorDeleter(id):
    my_InstrutorData = Instructor.query.get(id)
    Chk_Course = my_InstrutorData.courses
    if not Chk_Course:
        db.session.delete(my_InstrutorData)
        db.session.commit()
        return redirect(url_for('InstructorIndex'))

    flash('Instructor is registerd in one or more courses, please try again!')
    return redirect(url_for('InstructorIndex'))



@app.route('/InstructorUpdate', methods = ['GET','POST'])
def InstructorUpdate():
    
    if request.method == 'POST':
        my_InstrutorData = Instructor.query.get(request.form.get('id'))
        my_InstrutorData.Name = request.form['name']
        my_InstrutorData.id = request.form['InstructorID']
        my_InstrutorData.Department = request.form['Department']
        db.session.commit()
        
        return redirect(url_for('InstructorIndex'))

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)