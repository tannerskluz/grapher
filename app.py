from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Data(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	xValues = db.Column(db.Integer)
	yValues = db.Column(db.Integer)
	valid = db.Column(db.Integer, default = 1)
	date_created = db.Column(db.DateTime, default = datetime.utcnow)

	def __repr__(self):
		return '<Task %r>' % self.id


@app.route('/', methods = ['POST', 'GET'])
def index():
	if request.method == 'POST':
		task_content =request.form['content']
		xVal = int(task_content.split(',')[0])
		yVal = int(task_content.split(',')[1])
		new_point = Data(xValues = xVal, yValues = yVal)

		try:
			db.session.add(new_point)
			db.session.commit()
			return redirect('/')
		except:
			return 'There was an issure adding your task'

	else:
		points = Data.query.order_by(Data.date_created).all()
		return render_template('index.html', points = points)

@app.route('/delete/<int:id>')
def delete(id):
	point_to_delete = Data.query.get_or_404(id)

	try:
		db.session.delete(point_to_delete)
		db.session.commit()
		return redirect('/')
	except:
		return 'There was a problem deleting that point'

if __name__ == "__main__":
	app.run(debug=True)