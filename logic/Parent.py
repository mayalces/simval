"""
Class Parent: This class allow the creation of the reference and alternate gamete. Each of them is a list of lists.

2014 Mayra Alejandra Cespedes
"""

import numpy as np
import math


class Parent():
	def __init__(self):
		""" Default values for the object variables """
		self.choices = [1, 0]

	def generate_pos(self, n_markerSites, low_size, high_size):
		""" Method generatePos: create a list with the distances between each marker in centiMorgans """

		distances = [np.random.randint(low_size, high_size) for _ in range(n_markerSites)]

		return distances

	def generate_parent(self, n_marker_sites, ploidy, choices):
		""" Method generateParent: create a list of lists with the alleles depending on the ploidy value """

		parent = []
		for a in range(ploidy):
			parent.append([np.random.choice(choices) for _ in range(n_marker_sites)])

		return parent

	def generate_parent_plus(self, parent):
		""" Method generate_parent_plus: create a list of lists based on a previous parent
		:rtype : list
		"""
		parent2 = []

		for p in parent:
			parent2.append([int(not x) for x in p])

		return parent2

	def generate_parent_from_file(self, input_file):
		""" Method generate_parent_plus: create a list of lists based on a previous parent
		:rtype : list
		"""
		i_file = open(input_file, "r")
		lines = i_file.readlines()
		lists = []
		allele1 = []
		allele2 = []

		for line in lines:
			lists.append(line.strip().split(','))

		for l in lists:
			allele1.append(int(l[0]))
			allele2.append(int(l[1]))

		parent = [allele1, allele2]

		return parent


if __name__ == '__main__':
	ch = Parent()
	#print int(math.ceil(0.5))
	a = [1, 2, 3, 4, 5]
	b = [1, 2, 3, 4, 5]
	print a[:2]

	#a = ch.generate_parent_from_file("pruebas/DatosReales/padreArroz1.txt")
	#print a
	# np.random.seed(2154)
	# for i in range(10):
	# 	print np.random.poisson(0.0004 * 2944)

	# index = [list(np.random.choice(15, 2)) for _ in range(15)]
	# print index
	# index = [list(np.random.choice(15, 2)) for _ in range(15)]
	# print index
	# pos = ch.generate_pos(10, 0.004, 100)
	# print pos
	# result = ch.generate_parent(10, 2, [1, 0])
	# print "generate_parent: ", result
	# result2 = ch.generate_parent_plus(result)
	# print "generate_parent_plus: ", result2








