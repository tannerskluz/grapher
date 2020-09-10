from flask import Flask, render_template, url_for, request, redirect
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import grapher as gr
import mpld3
import json

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)
reg = 1

class Data:
	def __init__(self):
		self.xPoints = []
		self.yPoints = []

	def addPoint(self,x,y):
		self.xPoints.append(x)
		self.yPoints.append(y)

	def deletePoint(self, index):
		self.xPoints.pop(index)
		self.yPoints.pop(index)

	def prepare_graph(self, regression_type):
		if len(self.xPoints) <= regression_type:
			print('error points regression_type')
			raise ValueError('Not enough points for regression')
		graph = gr.graph(len(self.xPoints))
		graph.numberOfPoints = len(self.xPoints)
		for i in range(len(self.xPoints)):
			graph.points[i,0] = self.xPoints[i]
			graph.points[i,1] = self.yPoints[i]
		graph.regression = regression_type
		graph.coefficients = graph.polyFit(graph.regression)
		function = graph.getCoeff()
		rSquared = graph.rSquaredCalculate()
		#print(function)
		#print(rSquared)
		#return graph.graphToHtml()
		return graph.graphToHtml(), function, rSquared

# class Data(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	xValues = db.Column(db.Float)
# 	yValues = db.Column(db.Float)
# 	valid = db.Column(db.Integer, default = 1)
# 	date_created = db.Column(db.DateTime, default = datetime.utcnow)

# 	def __repr__(self):
# 		return '<Task %r>' % self.id

# def prepare_graph(regression_type):
# 	global xPoints
# 	global yPoints
# 	if len(xPoints) <= regression_type:
# 		print('error points regression_type')
# 		raise ValueError('Not enough points for regression')
# 	graph = gr.graph(len(xPoints))
# 	graph.numberOfPoints = len(xPoints)
# 	for i in range(len(xPoints)):
# 		graph.points[i,0] = xPoints[i]
# 		graph.points[i,1] = yPoints[i]
# 	graph.regression = regression_type
# 	graph.coefficients = graph.polyFit(graph.regression)
# 	function = graph.getCoeff()
# 	rSquared = graph.rSquaredCalculate()
# 	#print(function)
# 	#print(rSquared)
# 	#return graph.graphToHtml()
# 	return graph.graphToHtml(), function, rSquared
gd= Data()

def get_data():
	return gd

@app.route('/', methods = ['POST', 'GET'])
def index():
	graph_data = get_data()
	if request.method == 'POST':
		task_content =request.form['content']
		try:
			print('add point')
			xVal = float(task_content.split(',')[0])
			yVal = float(task_content.split(',')[1])
			print(xVal)
			print(yVal)
			unique = True
			global reg
			for i in range(len(graph_data.xPoints)):
				if graph_data.xPoints[i] == xVal and graph_data.yPoints[i] == yVal:
					unique =False
					break
			if unique:
				print('attempting to add')
				graph_data.addPoint(xVal, yVal)
			else:
				raise ValueError
				print('point already listed')
			#return redirect('/')
		except:
			#note that input is incorrect
			try:
				g, f, r = graph_data.prepare_graph(reg)
				json1 = json.dumps(mpld3.fig_to_dict(g))
			except:
				print('xPoints:', graph_data.xPoints)
				print('yPoints:', graph_data.yPoints)
				return render_template('index.html',x= graph_data.xPoints, y = graph_data.yPoints, json1 = None,regstatus = reg, add_error = True)
			print(f)
			print(r)
			print('xPoints:', graph_data.xPoints)
			print('yPoints:', graph_data.yPoints)
			return render_template('index.html', x= graph_data.xPoints, y = graph_data.yPoints, json1 = json1, regstatus = reg, function =f, r2 =r, add_error =True)
		#reg = int(request.form.get("regs"))
		#global reg
		try:
			g, f, r = graph_data.prepare_graph(reg)
			json1 = json.dumps(mpld3.fig_to_dict(g))
		except:
			print('xPoints:', graph_data.xPoints)
			print('yPoints:', graph_data.yPoints)
			return render_template('index.html',x= graph_data.xPoints, y = graph_data.yPoints, json1 = None,regstatus = reg)
		print(f)
		print(r)
		print('xPoints:', graph_data.xPoints)
		print('yPoints:', graph_data.yPoints)
		return render_template('index.html',x= graph_data.xPoints, y = graph_data.yPoints, json1 = json1, regstatus = reg, function =f, r2 =r)
	elif request.method == 'GET':
		print('get spot')
		try:
			temp_reg = int(request.args.get('regs'))
		except: 
			print("could not get regs")
			temp_reg = 1
		reg = temp_reg
		print("regressoin : ", reg)
		try:
			g, f, r = graph_data.prepare_graph(reg)
			json1 = json.dumps(mpld3.fig_to_dict(g))
		except:
			print('xPoints:', graph_data.xPoints)
			print('yPoints:', graph_data.yPoints)
			return render_template('index.html',x= graph_data.xPoints, y = graph_data.yPoints, json1 = None,regstatus = reg)
		print(f)
		print(r)
		print('xPoints:', graph_data.xPoints)
		print('yPoints:', graph_data.yPoints)
		return render_template('index.html', x= graph_data.xPoints, y = graph_data.yPoints, json1 = json1, regstatus = reg, function =f, r2 =r)
	else:
		print('this spot')
		print('xPoints:', graph_data.xPoints)
		print('yPoints:', graph_data.yPoints)
		return render_template('index.html', x = graph_data.xPoints, y =graph_data.yPoints)

@app.route('/delete/<int:index>')
def delete(index):
	graph_data = get_data()
	print('attempting to delete index', index)
	try:
		graph_data.deletePoint(index)
		#return redirect('/')
	except:
		return 'There was a problem deleting that point'
	global reg
	try:
			g, f, r = graph_data.prepare_graph(reg)
			json1 = json.dumps(mpld3.fig_to_dict(g))
	except:
		print('xPoints:', graph_data.xPoints)
		print('yPoints:', graph_data.yPoints)
		return render_template('index.html',x= graph_data.xPoints, y = graph_data.yPoints, json1 = None,regstatus = reg)
	print(f)
	print(r)
	print('xPoints:', graph_data.xPoints)
	print('yPoints:', graph_data.yPoints)
	return render_template('index.html', x= graph_data.xPoints, y = graph_data.yPoints, json1 = json1, regstatus = reg, function =f, r2 =r)

@app.route('/regraph')
def regraph():
	global reg
	graph_data = get_data()
	try:
		g, f, r = graph_data.prepare_graph(reg)
		json1 = json.dumps(mpld3.fig_to_dict(g))
	except:
		print('xPoints:', graph_data.xPoints)
		print('yPoints:', graph_data.yPoints)
		return render_template('index.html',x= graph_data.xPoints, y = graph_data.yPoints, json1 = None,regstatus = reg)
	print(f)
	print(r)
	print('xPoints:', graph_data.xPoints)
	print('yPoints:', graph_data.yPoints)
	return render_template('index.html',x= graph_data.xPoints, y = graph_data.yPoints, json1 = json1, regstatus = reg, function =f, r2 =r)

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
	app.run(debug=True, host='0.0.0.0')