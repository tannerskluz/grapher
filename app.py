from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import grapher as gr
import mpld3
import json

app = Flask(__name__)
 #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:chipotleZen15@localhost/pointdata'
 app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zhbiykqqrhdqiz:fd84e7b3ab9afd90a6d528e4ceba24dc9312877d5311802d0da2df044574959b@ec2-3-226-231-4.compute-1.amazonaws.com:5432/d3tgs0lp4fsoj5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
reg = 1

class Data(db.Model):
	tablename__ = 'pointdata'
	id = db.Column(db.Integer, primary_key = True)
	xValues = db.Column(db.Float)
	yValues = db.Column(db.Float)
	date_created = db.Column(db.DateTime, default = datetime.utcnow)

	def __init__(self, xValues, yValues):
		self.xValues = xValues
		self.yValues = yValues

	# def __repr__(self):
	# 	return '<Task %r>' % self.id

def prepare_graph(regression_type):
	xPoints = Data.query.with_entities(Data.xValues)
	yPoints = Data.query.with_entities(Data.yValues)
	xPoints = [x for x, in xPoints]
	yPoints = [y for y, in yPoints]
	if len(xPoints) <= regression_type:
		print('error points regression_type')
		raise ValueError('Not enough points for regression')
	graph = gr.graph(len(xPoints))
	graph.numberOfPoints = len(xPoints)
	for i in range(len(xPoints)):
		graph.points[i,0] = xPoints[i]
		graph.points[i,1] = yPoints[i]
	graph.regression = regression_type
	graph.coefficients = graph.polyFit(graph.regression)
	function = graph.getCoeff()
	rSquared = graph.rSquaredCalculate()
	#print(function)
	#print(rSquared)
	#return graph.graphToHtml()
	return graph.graphToHtml(), function, rSquared

@app.route('/', methods = ['POST', 'GET'])
def index():
	if request.method == 'POST':
		task_content =request.form['content']
		try:
			xVal = float(task_content.split(',')[0])
			yVal = float(task_content.split(',')[1])
			new_point = Data(xValues = xVal, yValues = yVal)
			already_in = Data.query.order_by(Data.date_created).all()
			unique = True
			global reg
			for point in already_in:
				if point.xValues == xVal and point.yValues == yVal:
					unique =False
					break
			if unique:
				db.session.add(new_point)
				db.session.commit()
			else:
				print('point already listed')
			#return redirect('/')
		except:
			#note that input is incorrect
			points = Data.query.order_by(Data.date_created).all()
			try:
				g, f, r = prepare_graph(reg)
				json1 = json.dumps(mpld3.fig_to_dict(g))
			except:
				return render_template('index.html',points = points, json1 = None,regstatus = reg, add_error = True)
			print(f)
			print(r)
			return render_template('index.html', points = points, json1 = json1, regstatus = reg, function =f, r2 =r, add_error =True)
		#reg = int(request.form.get("regs"))
		points = Data.query.order_by(Data.date_created).all()
		#global reg
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
			print("could not get regs")
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

@app.route('/regraph')
def regraph():
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

@app.route('/math')
def math():
	return render_template('math.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')		

if __name__ == "__main__":
	app.run(debug=True)