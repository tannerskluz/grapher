import numpy as np
import matplotlib.pyplot as plt, mpld3


class graph:
	def __init__(self, size):
		self.points = np.zeros((size,2))
		# self.xMin =0
		# self.xMax=0
		self.numberOfPoints = 0
		self.fileName = 'None'
		self.hasFile = False
		#self.equation = 'n/a'
		#self.rSquared = 0
		self.coefficients = []#coefficients is an 1D array with the first coefficent beingt the x^0 term
		self.regression = 0


	def execute(self):
		plt.clf()
		#self.coefficients = self.polyFit(self.regression)
		plt.plot(self.points[:,0], self.points[:,1], 'ro')
		x = np.linspace((min(self.points[:, 0]))-2,max(self.points[:, 0])+2, 100)
		plt.plot(x, self.polyCalculate(x), label = "f(x) = " +self.polyLabel())
		plt.title("test")
		plt.legend()
		plt.show()		
		#assume everything is initialized

	def graphToHtml(self):
		display = plt.figure()
		#plt.clf(figure = display)
		#self.coefficients = self.polyFit(self.regression)
		f, display = plt.subplots()
		display.plot(self.points[:,0], self.points[:,1], 'ro')
		x = np.linspace((min(self.points[:, 0]))-2,max(self.points[:, 0])+2, 100)
		display.plot(x, self.polyCalculate(x), label = "f(x) = " +self.polyLabel())
		#plt.title("test")
		display.legend()
		plt.xlabel('x')
		plt.ylabel('y')
		plt.title('Graph')
		return f		

	def polyCalculate(self, x):
		coefficientPower = 0
		value = 0
		for c in self.coefficients:
			value = value + (c *(x**coefficientPower))
			coefficientPower += 1
		return value

	def getCoeff(self):
			roundlist = [round(x,3) for x in self.coefficients]
			return [x for x in reversed(roundlist)]

	def polyLabel(self):
		function = ""
		for i in reversed(range(len(self.coefficients))):
			if i == 0:
				function = function + str(round(self.coefficients[i],3))
			elif i ==1:
				function = function + str(round(self.coefficients[i],3)) +  "x + "
			else:
				function = function + str(round(self.coefficients[i],3)) +  "x^" + str(i)+ " + "
		return function

	def polyFit(self, degree):
		rowIndex = 0
		array = np.ones((len(self.points), degree+1 ))
		soln = np.zeros((len(self.points), 1))
		for p in self.points:
			for i in range(0,degree +1):
				array[rowIndex, i] = (p[0])**i
			soln[rowIndex, 0] = p[1]
			rowIndex +=1
		arrayT = np.transpose(array) 
		coeff = np.matmul(arrayT,array)
		#print(coeff)
		soln2 = np.matmul(arrayT, soln)
		#print(soln2)
		fit = np.linalg.solve(coeff, soln2)
		fit = np.transpose(fit)
		#print(fit)
		return fit[0]

	def xAxisMax(self):
		self.xMax = max(self.points[:, 0])
		return

	def xAxisMin(self):
		self.xMin = min(self.points[:, 0])


	def calculatedFunction(self, xValue):
		sum = 0
		for i in range(len(self.coefficients)):
			sum+= (xValue**i)*self.coefficients[i]
		return sum

	def rSquaredCalculate(self):
		yValueAvg = np.average(self.points[:,1])
		SSR = 0
		SST = 0
		for i in (range(len(self.points[:,1]))):
			SSR += (self.points[i,1] - self.calculatedFunction(self.points[i,0]))**2
			SST += (self.points[i,1] - yValueAvg)**2
		return round((1 - (SSR/SST)) * 100,2)


	