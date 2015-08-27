"""
Class Validator: This class allow the comparison of the genetic map obtained through the tools and the genetic data simulation.


2014 Mayra Alejandra Cespedes
"""
from __future__ import division

import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from StringIO import StringIO


class Validator():

    def __init__(self):
        """ Default values for the object variables """
        pass

    def compare_listcomp(self, list_a, list_b):
        """ Method compare_listcomp: return the percentage of points well placed, in the comparison between the genetic map
         and the genetic data simulated. """

        result = [i for i, j in zip(list_a, list_b) if i == j]

        return (float(len(result)) / float(len(list_a))) * 100

    def edit_distance(self, list_a, list_b):
        """ Method edit_distance: return the sorting grade, in the comparison between the genetic map
         and the genetic data simulated."""

        oneago = None
        thisrow = range(1, len(list_b) + 1) + [0]
        for x in xrange(len(list_a)):
            twoago, oneago, thisrow = oneago, thisrow, [0] * len(list_b) + [x + 1]
            for y in xrange(len(list_b)):
                delcost = oneago[y] + 1
                addcost = thisrow[y - 1] + 1
                subcost = oneago[y - 1] + (list_a[x] != list_b[y])
                thisrow[y] = min(delcost, addcost, subcost)

        return 1 - (thisrow[len(list_b) - 1] / len(list_a))  # thisrow[len(listB) - 1]

    def kendall_tau_comp(self, list_a, list_b):
        """ Method kendall_tau_comp: return the percentage of points well placed, in the comparison between the genetic map
         and the genetic data simulated. """

        tau, p_value = stats.kendalltau(list_a, list_b)

        return tau

    def graph_comparison(self, list_a, list_b, form, line, form2):
        """ Method graph_compare: return the graphic of the comparison between the genetic map
         and the genetic data simulated. X axis -> listA, Y axis -> listB"""

        plt.subplot(111)
        plt.plot(list_a, list_b, form, label='Markers')
        plt.plot(list_a, line, form2, label='Linear Regression')
        plt.legend(bbox_to_anchor=(0., 1.05, 1., .102), loc=3, ncol=2, borderaxespad=0.)
        #plt.axis(0, listA[-1], 0, listB[-1])
        #img = StringIO()
        fig = plt
        #img.seek(0)
        
        return fig

    def linear_regression(self, list_a, list_b):
        """ Method linear_regression: returns the adjusted line for the points in list_b respect to list_a"""
        slope, intercept, r_value, p_value, std_err = stats.linregress(list_a, list_b)

        print "r_squared: ", r_value ** 2

        line = [(slope * i) + intercept for i in list_a]

        return line


if __name__ == '__main__':

    v = Validator()
    columns, columns2, columns3, columns4, columns5, columns6 = [], [], [], [], [], []

    path_file = "pruebas/YucaF2/ResultMD.txt"
    #path_file = "pruebas/Escenario3/P1/ResultMD.txt"
    #path_file2 = "pruebas/Escenario3/P1/MyMap.txt"
    path_file2 = "pruebas/YucaF2/MyMap.txt"

    # path_file = "ResultMD.txt"
    # path_file2 = "MyMap.txt"

    for line in open(path_file):
        c = line.split('\t')
        columns.append(int(c[0]))

    for line in open(path_file2):
        c = line.split('\t')
        #print c
        if c[0] == '1':
            columns2.append(int(c[1]))

    for line in open(path_file2):
        c = line.split('\t')
        if c[0] == '2':
            columns3.append(int(c[1]))

    # for line in open(path_file2):
    #     c = line.split('\t')
    #     if c[0] == '3':
    #         columns4.append(int(c[1]))
    #
    # for line in open(path_file2):
    #     c = line.split('\t')
    #     if c[0] == '4':
    #         columns5.append(int(c[1]))
    #
    # for line in open(path_file2):
    #     c = line.split('\t')
    #     if c[0] == '5':
    #         columns6.append(int(c[1]))

    c1 = [x for x in columns if x in columns2]
    c2 = [x for x in columns if x in columns3]
    # c3 = [x for x in columns if x in columns4]
    # c4 = [x for x in columns if x in columns5]
    # c5 = [x for x in columns if x in columns6]

    print "edit_distance #1: ", v.edit_distance(c1, columns2)
    print "kendall_tau #1: ", v.kendall_tau_comp(c1, columns2)
    print "edit_distance #2: ", v.edit_distance(c2, columns3)
    print "kendall_tau #2: ", v.kendall_tau_comp(c2, columns3)
    # print "edit_distance #3: ", v.edit_distance(c3, columns4)
    # print "kendall_tau #3: ", v.kendall_tau_comp(c3, columns4)
    # print "edit_distance #4: ", v.edit_distance(c4, columns5)
    # print "kendall_tau #4: ", v.kendall_tau_comp(c4, columns5)
    # print "edit_distance #5: ", v.edit_distance(c5, columns6)
    # print "kendall_tau #5: ", v.kendall_tau_comp(c5, columns6)
    line = v.linear_regression(c1, columns2)
    line2 = v.linear_regression(c2, columns3)
    # line3 = v.linear_regression(c3, columns4)
    # line4 = v.linear_regression(c4, columns5)
    # line5 = v.linear_regression(c5, columns6)
    #print line
    v.graph_comparison(c1, columns2, 'bo', line, 'r-')
    v.graph_comparison(c2, columns3, 'bo', line2, 'r-')
    # v.graph_comparison(c3, columns4, 'bo', line3, 'r-')
    # v.graph_comparison(c4, columns5, 'bo', line4, 'r-')
    # v.graph_comparison(c5, columns6, 'bo', line5, 'r-')
    #v.graph_comparison(c2, columns3, 'bo')

    # lista1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # lista2 = [50, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]  # [10, 5, 6, 3, 4, 2, 1, 7, 8, 9]  # [50, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    #
    # print v.compare_listcomp(lista1, lista2)
    # print v.edit_distance(lista1, lista2)
    # print v.kendall_tau_comp(lista1, lista2)
    # line = v.linear_regression(lista1, lista2)
    # v.graph_comparison(lista1, lista2, 'bo', line, 'r-')











