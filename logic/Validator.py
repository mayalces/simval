"""
Class Validator: This class allow the comparison of the genetic map obtained through the tools and the genetic data simulation.
			  

2014 Mayra Alejandra Cespedes
"""
from __future__ import division

import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


class Validator():

	def __init__(self):
		""" Default values for the object variables """
		pass

	def compare_listcomp(self, listA, listB):
		""" Method compare_listcomp: return the percentage of points well placed, in the comparison between the genetic map
		 and the genetic data simulated. """

		result = [i for i, j in zip(listA, listB) if i == j]

		return (float(len(result)) / float(len(listA))) * 100

	def kendall_tau_comp(self, listA, listB):
		""" Method kendall_tau_comp: return the percentage of points well placed, in the comparison between the genetic map
		 and the genetic data simulated. """

		tau, p_value = stats.kendalltau(listA, listB)

		return tau

	def edit_distance(self, listA, listB):
		""" Method edit_distance: return the sorting grade, in the comparison between the genetic map
		 and the genetic data simulated."""

		if listB[0] > listB[1]:
			listB.reverse()

		oneago = None
		thisrow = range(1, len(listB) + 1) + [0]
		for x in xrange(len(listA)):
			twoago, oneago, thisrow = oneago, thisrow, [0] * len(listB) + [x + 1]
			for y in xrange(len(listB)):
				delcost = oneago[y] + 1
				addcost = thisrow[y - 1] + 1
				subcost = oneago[y - 1] + (listA[x] != listB[y])
				thisrow[y] = min(delcost, addcost, subcost)

		return 1 - (thisrow[len(listB) - 1] / len(listA))

	def graph_comparison(self, listA, listB, form):
		""" Method graph_compare: return the graphic of the comparison between the genetic map
		 and the genetic data simulated. X axis -> listA, Y axis -> listB"""

		plt.plot(listA, listB, form)
		#plt.axis(0, listA[-1], 0, listB[-1])
		plt.show()

if __name__ == '__main__':

	# listA = open("MstMap1.txt", 'r')
	# listB = open("MstMap2.txt", 'r')
	v = Validator()
	columns, columns2, columns3 = [], [], []

	path_file = "pruebas/prueba2/P1/ResultMD.txt"
	path_file2 = "pruebas/prueba2/P1/MyMap.txt"

	# path_file = "ResultMD.txt"
	# path_file2 = "MyMap.txt"

	for line in open(path_file):
		c = line.split('\t')
		columns.append(c[0])

	for line in open(path_file2):
		c = line.split(' ')
		if c[0] == '1':
			columns2.append(c[2])

	for line in open(path_file2):
		c = line.split(' ')
		if c[0] == '2':
			columns3.append(c[2])

	c1 = [x for x in columns if x in columns2]
	c2 = [x for x in columns if x in columns3]
	#print c1.reverse()
	#print c2

	# print v.edit_distance([50, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
	# print v.kendall_tau_comp([1, 2, 3, 53, 5], [1, 2, 3, 4, 5])

	print "kendall_tau #1: ", v.kendall_tau_comp(c1, columns2)
	print "kendall_tau #2: ", v.kendall_tau_comp(c2, columns3)
	#print "edit_distance: ", v.edit_distance(c1, columns2)
	v.graph_comparison(c1, columns2, 'ro')
	v.graph_comparison(c2, columns3, 'bo')








