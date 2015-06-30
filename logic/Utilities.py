"""
Class Utilities: This class allow the creation of the reference and alternate gamete. Each of them is a list of tuples
			  (position, allele value).
			  

2014 Mayra Alejandra Cespedes
"""

import random
import numpy as np
import copy


class Utilities():

	def __init__(self):
		""" Default values for the object variables """
		pass

	def generate_one_map_file(self, data, meta_data, type, fileName):
		result_file = open(fileName, "w")

		result_file.write('data type' + ' ' + type + ' ' + 'intercross')
		result_file.write('\n')
		result_file.write(str(len(data[0])) + ' ' + str(len(data)) + ' ' + str(2))
		result_file.write('\n')
		result_file.write('\n')

		x = 0

		for i in data:
			result_file.write('*M' + str(meta_data[x]) + '\t')
			for j in i:
				if j == [0, 0]:
					result_file.write('B' + '\t')
				elif j == [0, 1]:
					result_file.write('H' + '\t')
				elif j == [1, 0]:
					result_file.write('H' + '\t')
				elif j == [1, 1]:
					result_file.write('A' + '\t')
				elif j == ['N', 'N']:
					result_file.write('-' + '\t')

			result_file.write('\n')
			x += 1

		result_file.close()

		return result_file

	def generate_map_disto_file(self, data, meta_data, fileName):

		result_file = open(fileName, "w")

		x = 0

		for i in data:
			result_file.write('m' + str(meta_data[x]) + '\t')
			for j in i:
				if j == [0, 0]:
					result_file.write('B' + '\t')
				elif j == [0, 1]:
					result_file.write('H' + '\t')
				elif j == [1, 0]:
					result_file.write('H' + '\t')
				elif j == [1, 1]:
					result_file.write('A' + '\t')
				elif j == ['N', 'N']:
					result_file.write('-' + '\t')

			result_file.write('\n')
			x += 1

		result_file.close()

		return result_file

	def generate_mst_map_file(self, data, meta_data, fileName):

		result_file = open(fileName, "w")

		result_file.write('locus_name' + '\t')

		for header in range(1, len(data[0]) + 1):
			result_file.write('i' + str(header) + '\t')

		result_file.write('\n')
		x = 0

		for i in data:
			result_file.write('m' + str(meta_data[x]) + '\t')
			for j in i:
				if j == [0, 0]:
					result_file.write('B' + '\t')
				elif j == [0, 1]:
					result_file.write('X' + '\t')
				elif j == [1, 0]:
					result_file.write('X' + '\t')
				elif j == [1, 1]:
					result_file.write('A' + '\t')
				elif j == ['N', 'N']:
					result_file.write('U' + '\t')

			result_file.write('\n')
			x += 1

		result_file.close()

		return result_file

	def real_data_format(self, input_file, output_file, file_format):

		i_file = open(input_file, "r")
		result_file = open(output_file, "w")
		lines = i_file.readlines()
		f = []

		for line in lines:
				l = line.strip()
				f.append(l.split('\t'))

		if file_format == "OM":
			result_file.write('data type f2 intercross')
			result_file.write('\n')
			result_file.write(str(len(f[0]) - 3) + ' ' + str(len(f)) + ' ' + str(2))
			result_file.write('\n')
			result_file.write('\n')
		elif file_format == "MM":
			result_file.write('locus_name' + '\t')
			for header in range(1, len(f[0]) + 1):
				result_file.write('i' + str(header) + '\t')
			result_file.write('\n')

		for e in f:
			for i in range(3, len(e)):
				if e[i] == e[1]:
					e[i] = 'A'
				elif e[i] == e[2]:
					e[i] = 'B'
				elif e[i] == 'N':
					e[i] = '-'
				elif file_format == "MM":
					e[i] = 'X'
				else:
					e[i] = 'H'

		np.random.seed(2)
		np.random.shuffle(f)

		for l in f:
			for i in range(len(l)):
				if i == 1 or i == 2:
					pass
				else:
					result_file.write("%s\t" % l[i])
			result_file.write("\n")

		result_file.close()
		i_file.close()

	def hypred_format(self, input_file):

		i_file = open(input_file, "r")
		lines = i_file.readlines()
		f = []
		nueva = []

		for line in lines:
			l = line.strip()
			f.append(l.split('\t'))

		print len(f)
		print len(f[99])
		print f[99][39]

		for i in range(len(f)):
			for j in range(len(f[0])):
				f[i][j] = int(f[i][j])

		cont = 0

		for x in range(len(f) / 2):
			cont2 = cont + 1
			nueva.append([f[cont], f[cont2]])
			cont += 2

		return nueva


if __name__ == '__main__':

	u = Utilities()
	# u.real_data_format("pruebas/DatosReales/caroteno.txt", "pruebas/DatosReales/carotenoMD.xls", "MD")
	# u.real_data_format("pruebas/DatosReales/caroteno.txt", "pruebas/DatosReales/carotenoOM.raw", "OM")
#     a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#     b = [1, 8, 9, 4, 4, 3, 4, 2, 5]

#     #r = [i for i,j in zip(a, b) if i==j] 
#     r = frozenset(a).intersection(b)

#     print r
#     
