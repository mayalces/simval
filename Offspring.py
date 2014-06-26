"""
Class Offspring: This class allow the creation of the offspring through the reference and alternate parents.                     

2014 Mayra Alejandra Cespedes
"""

import random
import math


class Offspring():

      def __init__(self):
            """ Default values for the object variables """
            self.avgCMPerKbp = 0.37  # depende del organismo 0.004 arroz, 0.002 yuca relacion distancia genetico y fisica
            self.nTotalSegregants = 200
            self.alleles = 2
            self.pNull = 1

      def calculateProbs(self, positions):
            """ Method calculateProbs: calculate the recombination frequency for the offspring. Returns a list with the percentage
                                       values. """
            changeProbs = []
            lastpos = 0
            for n in range(0, len(positions)):
                  pos = positions[n]
                  if n==0:
                        changeProbs.insert(n, 0.5)
                  else:
                        dKbp = (pos-lastpos)/1000.0  # preguntar a Jorge de donde sale el valor 1000?? por ser K
                        cmPerKbp = random.gauss(0.0, 1.0)*self.avgCMPerKbp*0.1+self.avgCMPerKbp
                        if cmPerKbp < 0.0001:
                              cmPerKbp = 0.0001

                        dMorgans = 0.01*cmPerKbp*dKbp
                        recombP = 0.5*(1 - math.exp(-2.0*dMorgans))  # Haldane function

                        if recombP > 0.5:
                              recombP = 0.5
                        changeProbs.insert(n, recombP)
                  lastpos = pos
            return changeProbs

      def generateOffspring(self, nTotalSegregants,  parentA, parentB, changeProbs, pnull):
            """ Method generateOffspring: Returns a list of lists that contain the result of the crossover between the parents. """
            segregants = []

            for k in range(0, len(parentA)):
                  segregants.append([0]*nTotalSegregants)

            for i in range(0, len(parentA)):
                  for j in range(0, nTotalSegregants):
                        if (random.random() < changeProbs[j]):
                              segregants[i][j] = [random.choice(parentB[j]), random.choice(parentA[j])]
                        else:
                              segregants[i][j] = [random.choice(parentA[j]), random.choice(parentB[j])]

            percentage = (len(parentA)*pnull)/100
            
            for i in range(1, percentage):
                  segregants[random.randint(0,  len(parentA)-1)][random.randint(0, nTotalSegregants-1)] = ['N', 'N']

            return segregants

      def mixOffspring(self, segregants, positions, mix):
            """ Method mixOffspring: Returns a list of lists that contain the offspring mix. """

            newList = []

            for p in range(0, len(positions)):
                  index = positions.index(mix[p])
                  newList.insert(p, segregants[index])

            return newList

      

#if __name__=='__main__':
      #p = Parent()
      #ch = Offspring()
      #ut = Utilities()

      #positions = p.generatePos(p.nMarkerSites)
      #parentA = p.generateParent(p.nMarkerSites, ch.alleles)
      #parentB = p.generateParentPlus(parentA, ch.alleles)
 
      #print positions
      #print parentA
      #print parentB

      #recombFreq = ch.calculateProbs(positions)
      #print recombFreq

      #offs = ch.generateOffspring(parentA, parentB, recombFreq, 5)

      #mix = list(positions)
      #random.shuffle(mix)
      #print mix

      #newOffs = ch.mixOffspring(offs, positions)
            
      #result = ut.generateMSTMapFile(newOffs, mix, "MstMap1.txt")
      #result2 = ut.generateMSTMapFile(offs, positions, "MstMap2.txt")





     
		
