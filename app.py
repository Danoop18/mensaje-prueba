from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(250), nullable=False)
    Date = db.Column(db.DateTime, default=datetime.utcnow)
    Born_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error mijo'
    else:
        tasks = Todo.query.order_by(Todo.Date).all()
        return render_template('index2.html', tasks=tasks)


if __name__ == '__main__':
    app.run(debug=True)
