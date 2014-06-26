"""
Class Utilities: This class allow the creation of the reference and alternate gamete. Each of them is a list of tuples
			  (position, allele value).
			  

2014 Mayra Alejandra Cespedes
"""

import random
import copy

class Utilities():

	def __init__(self):
		""" Default values for the object variables """
		pass

	def generateOneMapFile(self, data, meta_data, fileName):
		pass

	def generateMapDistoFile(self, data, meta_data, fileName):
		pass

	def generateMSTMapFile(self, data, meta_data, fileName):

		result_file = open(fileName, "w")

		result_file.write('locus_name'+'\t')

		for header in range(1, len(data[0])):
			result_file.write('i'+str(header)+'\t')

		result_file.write('\n')
		x = 0

		for i in data:
			result_file.write('m'+str(meta_data[x])+'\t')
			for j in i:
				if j[0] == j[1]:
					if j[0] == 'N':
						result_file.write('U'+'\t')
					else:
						result_file.write('A'+'\t')
				else:
					result_file.write('B'+'\t')
			result_file.write('\n')
			x += 1

		result_file.close()

		return result_file



# if __name__=='__main__':
#     a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#     b = [1, 8, 9, 4, 4, 3, 4, 2, 5]

#     #r = [i for i,j in zip(a, b) if i==j] 
#     r = frozenset(a).intersection(b)

#     print r
#     
