"""
Class Offspring: This class allow the creation of the offspring through the reference and alternate parents.                     

2014 Mayra Alejandra Cespedes
"""

import random
import math
import numpy as np

from Parent import Parent
from Utilities import Utilities
from Validator import Validator


class Offspring():
    def __init__(self):
        """ Default values for the object variables """
        self.avgCMPerKbp = 0.37  # depende del organismo 0.004 arroz, 0.002 yuca relacion distancia genetico y fisica

    def calculate_recomb(self, parent_a, parent_b, chrom_quantity, chromo_size, chrom_pos_vec, markers_quantity, recomb_rate, ploidy):
        """ Method calculate_recomb: calculate the recombination frequency for the offspring. Returns a list which represent a
        gamete. """

        gamete_r = [0 for _ in range(len(parent_a))]
        gam_result = []

        for pl in range(ploidy):
            num_loci = markers_quantity
            num_ini = 0
            for chrom in range(chrom_quantity):
                recomb_freq = np.random.poisson(recomb_rate * (chrom + chromo_size))  # generate the value of the recombination frequency
                #print "recomb_freq: ", recomb_freq

                positions_r = []

                if recomb_freq > 0:
                    positions_r = [np.random.random(1) for _ in range(recomb_freq)]  # the positions where the recombination occurs
                    positions_r.sort()
                    #print "positions_r: ", positions_r

                if np.random.uniform(0, 1) < 0.5:
                    gametes = list(parent_a)
                    point_at = 1
                else:
                    gametes = list(parent_b)
                    point_at = 2

                #print "gametes: ", gametes

                if recomb_freq > 0:
                    snp_aft_cx = []
                    loc_next_cx = positions_r[0]
                    num_next_cx = 1
                    count_snp = 0

                    while True:
                        if num_next_cx > recomb_freq:
                            break
                        if count_snp > (markers_quantity - 1):
                            snp_aft_cx.append(num_ini + count_snp)
                            break
                        if chrom_pos_vec[num_ini + count_snp] > loc_next_cx:
                            snp_aft_cx.append(num_ini + count_snp)
                            num_next_cx += 1
                            if num_next_cx > recomb_freq:
                                break
                            loc_next_cx = positions_r[num_next_cx - 1]
                            if count_snp <= (markers_quantity - 1):
                                if chrom_pos_vec[num_ini + count_snp] > loc_next_cx:
                                    count_snp -= 1
                        count_snp += 1

                    #snp_aft_cx = list(set(snp_aft_cx))
                    #print "snp_aft_cx: ", snp_aft_cx

                    num_next_cx = 1
                    count_snp = 0

                    while True:
                        if num_next_cx > len(snp_aft_cx):
                            while (num_ini + count_snp) <= (markers_quantity - 1):
                                gamete_r[num_ini + count_snp] = gametes[num_ini + count_snp]
                                count_snp += 1
                            break
                        else:
                            while (num_ini + count_snp) < snp_aft_cx[num_next_cx - 1]:
                                gamete_r[num_ini + count_snp] = gametes[num_ini + count_snp]
                                count_snp += 1

                        if point_at == 1:
                            gametes = list(parent_b)
                            point_at = 2
                        else:
                            gametes = list(parent_a)
                            point_at = 1

                        num_next_cx += 1

                    #print "gamete_r: ", gamete_r

                if recomb_freq is None or recomb_freq == 0:
                    for mark in range(markers_quantity):
                        gamete_r[num_ini + mark] = gametes[num_ini + mark]
                        #print "when 0: ", gamete_r

                num_ini = num_loci
                num_loci += markers_quantity

            gam_result.append(list(gamete_r))
            #print "gam_result: ", gam_result

        return gam_result

    def generate_offspring_f1(self, n_total_population, parent_a, parent_b, chrom_quantity, chromo_size, chrom_pos_vec, markers_quantity, recomb_rate, ploidy):
        """ Method generate_offspring_f1: Returns a list of lists that contain the result of the crossover between the parents.
        The result is a F1 population. """

        offspring = []

        for k in range(n_total_population):
            offspring.append([0] * len(parent_a[0]))

        for p in range(n_total_population):
            offspring[p] = self.calculate_recomb(parent_a[0], parent_b[0], chrom_quantity, chromo_size, chrom_pos_vec, markers_quantity, recomb_rate, ploidy)

        return offspring

    def generate_offspring_fn(self, population, chrom_quantity, chromo_size, chrom_pos_vec, markers_quantity, recomb_rate, ploidy):
        """ Method generate_offspring_fn: Returns a list of lists that contain the result of the crossover between the
        children. The result is a FN population. """

        offspring_fn = []

        for k in range(len(population)):
            offspring_fn.append([0] * len(population[0]))

        index = [list(np.random.choice(len(population), 2)) for _ in range(len(population))]
        #print "Indices: ", index

        for i in range(len(population)):
            offspring_fn[i] = self.calculate_recomb(population[index[i][0]][0], population[index[i][1]][0], chrom_quantity, chromo_size, chrom_pos_vec, markers_quantity, recomb_rate, ploidy)

        return offspring_fn

    def generate_error(self, p_error, population):
        """ Method generate_error: Returns the population with null fields equal to the error percentage entered. """
        percentage = (len(population) * len(population[0]) * p_error) / 100

        for i in range(percentage):
            population[np.random.randint(0, len(population) - 1)][np.random.randint(0, len(population[0]) - 1)] = ['N', 'N']

        return population

    def transform_matrix(self, population):
        """ Method transform_matrix: Returns a list of lists with the transpose of the original population. """

        new_population = []

        for p in range(len(population[0][0])):
            aux_list = []
            for m in population:
                aux_list.append([m[0][p], m[1][p]])
            new_population.append(aux_list)

        return new_population

    def mix_offspring(self, population, positions, mix):
        """ Method mix_offspring: Returns a list of lists that contain the offspring mix. """

        new_list = []

        for p in range(0, len(population)):
            index = positions.index(mix[p])
            new_list.insert(p, population[index])

        return new_list


if __name__ == '__main__':
    p = Parent()
    ch = Offspring()
    ut = Utilities()
    v = Validator()
    seed = [2154, 324]
    individual_size = 45  # [50, 100, 200, 300, 500, 1000]
    chromo_size = 1  # chromosome length in Morgans
    ploidy = 2
    choices = [1]
    chrom_quantity = 1
    markers_quantity = 200  # [50, 100, 200, 300, 500, 1000]
    recomb_rate = 0.1
    p_error = 5
    offs = []
    offsf2 = []
    new_pop = []
    #chrom_positions = [x for x in range(chrom_quantity)]

    np.random.seed(seed[0])

    #for chrom in range(chrom_quantity):
    #    chrom_positions[chrom] = list(np.random.sample(markers_quantity))
    #    chrom_positions[chrom].sort()

    #chrom_assigment.sort()
    #print chrom_positions

    #chrom_pos_vec = [x for i in chrom_positions for x in i]
    #print chrom_pos_vec

    #parent_a = p.generate_parent(markers_quantity * chrom_quantity, ploidy, choices)
    #parent_a = p.generate_parent_from_file("pruebas/DatosReales/padreArroz1-500.txt")
    #print "generate_parent: ", parent_a
    #parent_b = p.generate_parent_plus(parent_a)
    #parent_b = p.generate_parent_from_file("pruebas/DatosReales/padreArroz2-500.txt")
    #print "generate_parent_plus: ", parent_b

    #recomb = ch.calculate_recomb(parent_a[0], parent_b[0], chrom_quantity, chromo_size, chrom_pos_vec, markers_quantity, recomb_rate, ploidy)
    #print recomb

    #offs = ch.generate_offspring_f1(individual_size, parent_a, parent_b, chrom_quantity, chromo_size,
    #                                chrom_pos_vec, markers_quantity, recomb_rate, ploidy)
    #print offs

    offs, chrom_pos_vec = ut.real_data_format2("pruebas/Escenario4/P2/caroteno.txt")

    offsf2 = ch.generate_offspring_fn(offs, chrom_quantity, chromo_size, chrom_pos_vec, markers_quantity, recomb_rate, ploidy)
    #print offsf2

    offs_t = ch.generate_error(p_error, ch.transform_matrix(offs))
    #print offs_t
    #
    pos = [x for x in range(markers_quantity * chrom_quantity)]
    #print pos
    mix = list(pos)
    np.random.shuffle(mix)
    #print mix

    new_pop = ch.mix_offspring(offs_t, pos, mix)
    #print new_pop

    result1 = ut.generate_one_map_file(new_pop, mix, "f2", "OneMap" + ".raw")
    result2 = ut.generate_one_map_file(offs_t, pos, "f2", "ResultOM" + ".raw")
    #
    result3 = ut.generate_mst_map_file(new_pop, mix, "MstMap" + ".txt")
    result4 = ut.generate_mst_map_file(offs_t, pos, "ResultMM" + ".txt")

    result5 = ut.generate_map_disto_file(new_pop, mix, "MapDisto" + ".xls")
    result6 = ut.generate_map_disto_file(offs_t, pos, "ResultMD" + ".txt")
