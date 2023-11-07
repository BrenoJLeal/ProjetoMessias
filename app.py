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

@app.route("/", methods=['GET', 'POST'])
def home():
   todo_list = Todo.query.all()
   todo = None
   if request.method == "POST":
       name=request.form.get("name")
       new_task=Todo(name=name, done=False)
       db.session.add(new_task)
       db.session.commit()
       return redirect(url_for("home"))
   else:
       todo_id = request.args.get("todo_id")
       todo = Todo.query.get(todo_id) if todo_id else None
       return render_template("base.html", todo_list=todo_list, todo=todo)


@app.route('/edit', methods=['POST'])
def edit():
    data = request.get_json()
    todo_id = data.get('todo_id')
    new_name = data.get('name')
    new_task_id = data.get('task_id')
    edit_todo(todo_id, new_name, new_task_id)
    return redirect(url_for("home"))


def edit_todo(todo_id, new_name, new_task_id):
  todo = Todo.query.get(todo_id)
  todo.name = new_name
  todo.task_id = new_task_id
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



