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
xPoints = [1.69,2.69,3.69]
yPoints = [-1.69, -2.69, -3.69]

# class Data(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	xValues = db.Column(db.Float)
# 	yValues = db.Column(db.Float)
# 	valid = db.Column(db.Integer, default = 1)
# 	date_created = db.Column(db.DateTime, default = datetime.utcnow)

# 	def __repr__(self):
# 		return '<Task %r>' % self.id

def prepare_graph(regression_type):
	global xPoints
	global yPoints
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
	global xPoints
	global yPoints
	if request.method == 'POST':
		task_content =request.form['content']
		try:
			xVal = float(task_content.split(',')[0])
			yVal = float(task_content.split(',')[1])
			unique = True
			global reg
			for i in range(len(xPoints)):
				if xPoints[i] == xVal and yPoints[i] == yVal:
					unique =False
					break
			if unique:
				xPoints.append(xVal)
				yPoints.append(yVal)
			else:
				raise ValueError
				print('point already listed')
			#return redirect('/')
		except:
			#note that input is incorrect
			try:
				g, f, r = prepare_graph(reg)
				json1 = json.dumps(mpld3.fig_to_dict(g))
			except:
				print('xPoints:', xPoints)
				print('yPoints:', yPoints)
				return render_template('index.html',x= xPoints, y = yPoints, json1 = None,regstatus = reg, add_error = True)
			print(f)
			print(r)
			print('xPoints:', xPoints)
			print('yPoints:', yPoints)
			return render_template('index.html', x= xPoints, y = yPoints, json1 = json1, regstatus = reg, function =f, r2 =r, add_error =True)
		#reg = int(request.form.get("regs"))
		#global reg
		try:
			g, f, r = prepare_graph(reg)
			json1 = json.dumps(mpld3.fig_to_dict(g))
		except:
			print('xPoints:', xPoints)
			print('yPoints:', yPoints)
			return render_template('index.html',x= xPoints, y = yPoints, json1 = None,regstatus = reg)
		print(f)
		print(r)
		print('xPoints:', xPoints)
		print('yPoints:', yPoints)
		return render_template('index.html',x= xPoints, y = yPoints, json1 = json1, regstatus = reg, function =f, r2 =r)
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
			g, f, r = prepare_graph(reg)
			json1 = json.dumps(mpld3.fig_to_dict(g))
		except:
			print('xPoints:', xPoints)
			print('yPoints:', yPoints)
			return render_template('index.html',x= xPoints, y = yPoints, json1 = None,regstatus = reg)
		print(f)
		print(r)
		print('xPoints:', xPoints)
		print('yPoints:', yPoints)
		return render_template('index.html', x= xPoints, y = yPoints, json1 = json1, regstatus = reg, function =f, r2 =r)
	else:
		print('this spot')
		print('xPoints:', xPoints)
		print('yPoints:', yPoints)
		return render_template('index.html', points = points)

@app.route('/delete/<int:index>')
def delete(index):
	print('attempting to delete index', index)
	global xPoints
	global yPoints
	try:
		xPoints.pop(index)
		yPoints.pop(index)
		#return redirect('/')
	except:
		return 'There was a problem deleting that point'
	global reg
	try:
			g, f, r = prepare_graph(reg)
			json1 = json.dumps(mpld3.fig_to_dict(g))
	except:
		print('xPoints:', xPoints)
		print('yPoints:', yPoints)
		return render_template('index.html',x= xPoints, y = yPoints, json1 = None,regstatus = reg)
	print(f)
	print(r)
	print('xPoints:', xPoints)
	print('yPoints:', yPoints)
	return render_template('index.html', x= xPoints, y = yPoints, json1 = json1, regstatus = reg, function =f, r2 =r)

@app.route('/regraph')
def regraph():
	global reg
	global xPoints
	global yPoints
	try:
		g, f, r = prepare_graph(reg)
		json1 = json.dumps(mpld3.fig_to_dict(g))
	except:
		print('xPoints:', xPoints)
		print('yPoints:', yPoints)
		return render_template('index.html',x= xPoints, y = yPoints, json1 = None,regstatus = reg)
	print(f)
	print(r)
	print('xPoints:', xPoints)
	print('yPoints:', yPoints)
	return render_template('index.html',x= xPoints, y = yPoints, json1 = json1, regstatus = reg, function =f, r2 =r)

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