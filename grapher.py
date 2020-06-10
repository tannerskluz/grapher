import numpy as np
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt


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




	def polyCalculate(self, x):
		coefficientPower = 0
		value = 0
		for c in self.coefficients:
			value = value + (c *(x**coefficientPower))
			coefficientPower += 1
		return value

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
		print(coeff)
		soln2 = np.matmul(arrayT, soln)
		print(soln2)
		fit = np.linalg.solve(coeff, soln2)
		fit = np.transpose(fit)
		#print(fit)
		return fit[0]

	def xAxisMax(self):
		self.xMax = max(self.points[:, 0])
		return

	def xAxisMin(self):
		self.xMin = min(self.points[:, 0])




	