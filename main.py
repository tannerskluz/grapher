import numpy as np
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def main():
	root = tk.Tk()
	w = tk.Canvas(root, width = 800, height = 600, bg= 'red')
	w.pack()
	background_image = tk.PhotoImage(file = 'background.png')
	background_label = tk.Label(root, image = background_image)
	background_label.place(x=0, y=0, relwidth = 1, relheight =1)
	tk.Label(root, text = "Points").place(x = 0, y =0, relheight = .1, relwidth = .25)
	# tk.Label(root, text = 'x').grid(row=1, column = 0)
	# tk.Label(root, text = 'y').grid(row =1, column =1)

	# x = tk.Text(root, width = 7, height = 15)
	# x.grid(row = 3, column =0)
	# y = tk.Text(root, width =7, height =15)
	# y.grid(row = 3, column = 1)

	#tk.Label(root, text = 'Regression Type').grid(row=0, column = 2, columnspan =2, rowspan = 2)
	# z=tk.Listbox(root, height = 5)
	# z.insert(1, 'Linear')
	# z.insert(2, 'Quadratic')
	# z.insert(3, 'Cubic')
	# z.insert(4, '4th degree')
	# z.insert(5, '5th degree')
	# z.grid(row = 2, column =2, rowspan = 3, sticky = 'N')

	# w = tk.Button(root, width = 10, height =2, bg = 'red', text = 'GRAPH', command = lambda: graph(x.get("1.0",'end-1c').splitlines(), y.get("1.0",'end-1c').splitlines(), z.curselection()))
	# w.grid(row = 3, column = 2)

	root.mainloop()

def graph(xText, yText, regression):
	if (len(regression) == 0):
		tk.messagebox.showerror("Error", "Pick a regression type")
		return
	if (len(xText) != len(yText)):
		tk.messagebox.showerror("Error,", "Missing points")
		return
	plt.clf()
	size = len(xText)
	points = np.zeros((size,2))
	#print(points.shape)
	for i in range(size):
		try:
			points[i,0] = float(xText[i])	
		except ValueError:
				tk.messagebox.showerror("Error", "All points must be numbers")
				return
		try:
			points[i,1] = float(yText[i])
		except ValueError:
			tk.messagebox.showerror("Error", "All points must be numbers")
			return
	reg = regression[0]
	plt.plot(points[:,0], points[:,1], 'ro')
	#dim = xGraphDim(points)
	x = np.linspace(xMinGraphDim(points)-2,xMaxGraphDim(points)+2, 100)
	coefficients = polyFit(points, reg+1)
	plt.plot(x, polyCalculate(coefficients, x), label = label(coefficients))
	plt.title("test")
	plt.legend()
	plt.show()

# coefficients is an 1D array with the first coefficent beingt the x^0 term
def polyCalculate(Coefficients, x):
	coefficentPower = 0
	done = 0
	for c in Coefficients:
		done = done + (c *(x**coefficentPower))
		coefficentPower +=1
	return done

def xMaxGraphDim(points):
	return max(points[:, 0])

def xMinGraphDim(points):
	return min(points[:, 0])

def label(coeffs):
	function = "f(x) = "
	for i in reversed(range(len(coeffs))):
		if i == 0:
			function = function + str(round(coeffs[i],3))
		elif i ==1:
			function = function + str(round(coeffs[i],3)) +  "x + "
		else:
			function = function + str(round(coeffs[i],3)) +  "x^" + str(i)+ " + "
	return function

#L is a list of points as touples
#degree is an integer greater than 0 describing the degree of polynomial fit desired
def polyFit(L, degree):
	rowIndex = 0
	array = np.ones((len(L), degree +1))
	soln = np.zeros((len(L), 1))
	for p in L:
		for i in range(0,degree+1):
			array[rowIndex, i] = (p[0])**i
		soln[rowIndex, 0] = p[1]
		rowIndex +=1
	arrayT = np.transpose(array) 
	coeff = np.matmul(arrayT,array)
	soln2 = np.matmul(arrayT, soln)
	fit = np.linalg.solve(coeff, soln2)
	fit = np.transpose(fit)
	return fit[0]

if __name__=="__main__":
	main()

