from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import grapher as gr
import mpld3
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
reg = 1

class Data(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	xValues = db.Column(db.Float)
	yValues = db.Column(db.Float)
	valid = db.Column(db.Integer, default = 1)
	date_created = db.Column(db.DateTime, default = datetime.utcnow)

	def __repr__(self):
		return '<Task %r>' % self.id

def prepare_graph(regression_type):
	xPoints = Data.query.with_entities(Data.xValues)
	yPoints = Data.query.with_entities(Data.yValues)
	xPoints = [x for x, in xPoints]
	yPoints = [y for y, in yPoints]
	graph = gr.graph(len(xPoints))
	graph.numberOfPoints = len(xPoints)
	for i in range(len(xPoints)):
		graph.points[i,0] = xPoints[i]
		graph.points[i,1] = yPoints[i]
	graph.regression = regression_type
	graph.coefficients = graph.polyFit(graph.regression)
	function = graph.polyLabel()
	rSquared = graph.rSquaredCalculate()
	#print(function)
	#print(rSquared)
	#return graph.graphToHtml()
	return graph.graphToHtml(), function, rSquared

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
			#return redirect('/')
		except:
			return 'There was an issure adding your task'
		#reg = int(request.form.get("regs"))
		points = Data.query.order_by(Data.date_created).all()
		global reg
		try:
			g, f, r = prepare_graph(reg)
			json1 = json.dumps(mpld3.fig_to_dict(g))
		except:
			return render_template('index.html',points = points, json1 = None,regstatus = reg)
		print(f)
		print(r)
		return render_template('index.html',points = points, json1 = json1, regstatus = reg, function =f, r2 =r)
	elif request.method == 'GET':
		print('get spot')
		try:
			temp_reg = int(request.args.get('regs'))
		except: 
			temp_reg = 1
		reg = temp_reg
		print("regressoin : ", reg)
		points = Data.query.order_by(Data.date_created).all()
		try:
			g, f, r = prepare_graph(reg)
			json1 = json.dumps(mpld3.fig_to_dict(g))
		except:
			return render_template('index.html',points = points, json1 = None,regstatus = reg)
		print(f)
		print(r)
		return render_template('index.html', points = points, json1 = json1, regstatus = reg, function =f, r2 =r)
	else:
		points = Data.query.order_by(Data.date_created).all()
		print('this spot')
		return render_template('index.html', points = points)

@app.route('/delete/<int:id>')
def delete(id):
	point_to_delete = Data.query.get_or_404(id)

	try:
		db.session.delete(point_to_delete)
		db.session.commit()
		#return redirect('/')
	except:
		return 'There was a problem deleting that point'
	global reg
	points = Data.query.order_by(Data.date_created).all()
	try:
			g, f, r = prepare_graph(reg)
			json1 = json.dumps(mpld3.fig_to_dict(g))
	except:
		return render_template('index.html',points = points, json1 = None,regstatus = reg)
	print(f)
	print(r)
	return render_template('index.html', points = points, json1 = json1, regstatus = reg, function =f, r2 =r)

@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == "__main__":
	app.run(debug=True)