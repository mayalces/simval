"""
Class Parent: This class allow the creation of the reference and alternate gamete. Each of them is a list of tuples
			  (position, allele value).
			  

2014 Mayra Alejandra Cespedes
"""

import random
import copy


class Parent():

	def __init__(self):
		""" Default values for the object variables """
		self.chromosomeLength = 750000
		self.nMarkerSites = 2500
		self.choices = ['A', 'C','G', 'T']

	def generatePos(self, nMarkerSites):
		""" Method generatePos: create a list with the physical positions in the simulated chromosome """
		positions = [random.randint(1, self.chromosomeLength) for _ in range(nMarkerSites)]
		positions.sort()

		return positions


	def generateParent(self, nMarkerSites, alleles):
		""" Method generateParent: create a list of lists with the alleles depending of the ploidy value """
		parent = [[random.choice(self.choices) for _ in range(alleles)] for _ in range(nMarkerSites)] 

		return parent

	def generateParentPlus(self, parent, alleles):
		""" Method generateParentPlus: create a list of lists based on a previous parent """
		parent2 = []

		for p in parent:
			copy_choices = copy.copy(self.choices)
			copy_choices.remove(p[0])
			parent2.append([random.choice(copy_choices) for _ in range(alleles)])

		return parent2



#if __name__=='__main__':
    ## ch = Parent()
    ## pos = ch.generatePos(200)
    ## result = ch.generateParent(200, 2)
    ## result2 = ch.generateParentPlus(result, 2)

    #a = [1,2,3,4]
    #print a
    #a[0] = 5
    #print a

    ## print pos
    ## print result
    ## print result2






