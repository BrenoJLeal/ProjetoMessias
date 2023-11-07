from flask import Flask,render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    task_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    done=db.Column(db.Boolean)

@app.route("/")
def home():
    todo_list = Todo.query.all()
    todo = None
    if request.method == "GET":
        todo_id = request.args.get("todo_id")
        todo = Todo.query.get(todo_id) if todo_id else None
    return render_template("base.html", todo_list=todo_list, todo=todo)


@app.route('/add',methods=['POST'])
def add():
    name=request.form.get("name")
    new_task=Todo(name=name, done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo=Todo.query.get(todo_id)
    todo.done=not todo.done
    db.session.commit()
    return redirect(url_for("home"))
@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
  if request.method == 'GET':
    todo = Todo.query.get(todo_id)
    return render_template('base.html', todo=todo)
  elif request.method == 'POST':
    new_name = request.form.get('name')
    edit_todo(todo_id, new_name)
    return redirect(url_for("home"))

def edit_todo(todo_id, new_name):
  todo = Todo.query.get(todo_id)
  todo.name = new_name
  db.session.commit()
  return redirect(url_for("home"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo=Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))
if __name__ == '__main__':
    app.run(debug=True)



