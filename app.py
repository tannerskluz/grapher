from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import grapher as gr
import mpld3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Data(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	xValues = db.Column(db.Float)
	yValues = db.Column(db.Float)
	valid = db.Column(db.Integer, default = 1)
	date_created = db.Column(db.DateTime, default = datetime.utcnow)

	def __repr__(self):
		return '<Task %r>' % self.id


@app.route('/', methods = ['POST', 'GET'])
def index():
	if request.method == 'POST':
		task_content =request.form['content']
		xVal = float(task_content.split(',')[0])
		yVal = float(task_content.split(',')[1])
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

@app.route('/graph', methods=['GET', 'POST'])
def graph():
	if request.method == 'POST':
		xPoints = Data.query.with_entities(Data.xValues)
		yPoints = Data.query.with_entities(Data.yValues)
		xPoints = [x for x, in xPoints]
		yPoints = [y for y, in yPoints]
		# # print(type(xPoints))
		# print('x points')
		# for x in xPoints:
		# 	print(x)
		# print('y points')
		# for y in yPoints:
		# 	print(y)
		# # # print(xPoints)
		# # # print(yPoints)
		graph = gr.graph(len(xPoints))
		graph.numberOfPoints = len(xPoints)
		for i in range(len(xPoints)):
			graph.points[i,0] = xPoints[i]
			graph.points[i,1] = yPoints[i]
		graph.regression = 1
		####print('reg type', request.form.get('selector'))
		graph.coefficients = graph.polyFit(graph.regression)
		# print(graph.calculatedFunction(2))
		print('Points graphed x:')
		print(graph.points[:,0])
		print('Points graphed y:')
		print(graph.points[:,1])
		print('calculated function:')
		print(graph.polyLabel())
		print('caulculated r^2:')
		print(graph.rSquaredCalculate())
		return mpld3.fig_to_html((graph.graphToHtml()))
	else:
		return render_template('index.html', points = points)



if __name__ == "__main__":
	app.run(debug=True)