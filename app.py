import os
import numpy as np
import logic
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response, Response
# from Parent import Parent
# from Offspring import Offspring
# from Utilities import Utilities

# initialization
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(
    DEBUG = True,
)

# controllers

@app.route("/", methods=['GET','POST'])
def index():
	print "Entre a Index"
	error = ""
	if request.method == 'POST':
		print "Entre a If"
	else:
		error = 'Error!!'
		
	return render_template('index.html', error=error)
	
@app.route("/sim", methods=['POST', 'GET'])
def simulator():
	print "Entre a Sim"
	error = ""
	if request.method == 'POST':
		print "Entre a If"
		chrom_quantity = request.form['quantity_id'] # cantidad de cromosomas, por defecto 2
		chrom_size = request.form['size_id'] # tamano de cada cromosoma, todos de igual tamano, por defecto 1Morgan
		pop_size = request.form['off_id'] # tamano de la poblacion, por defecto 100
		marker_size = request.form['mark_id'] # Cantidad de marcadores, por defecto 100
		ploidy = request.form['ploidy_id'] # ploidia, por defecto diploides
		r_rate = request.form['r_rate_id'] # tasa de recombinacion, por defecto 0.1
		m_rate = request.form['m_rate_id'] # tasa de mutacion, por defecto 0.001
		e_rate = request.form['e_rate_id'] # porcentaje de poblacion nula, por defecto 5%
		seed = request.form['s_id'] # semilla random, por defecto 2154
		print "Antes de generate"
		generate(chrom_quantity, chrom_size, pop_size, marker_size, ploidy, r_rate, m_rate, e_rate, seed)
	else:
		error = 'Error!!'
	
	return render_template('simulator.html', error=error)
	
@app.route("/val", methods=['GET','POST'])
def validator():
	print "Entre a Val"
	error = ""
	if request.method == 'POST':
		print "Entre a If"
	else:
		error = 'Error!!'
		
	return render_template('validator.html', error=error)


def generate(chrom_quantity, chrom_size, pop_size, marker_size, ploidy, r_rate, m_rate, e_rate, seed):
	p = Parent()
	ch = Offspring()
	ut = Utilities()
	
	offs = []
	offsf2 = []
	new_pop = []
	chrom_positions = [x for x in range(chrom_quantity)]
	
	np.random.seed(seed)
	
	for chrom in range(chrom_quantity):
		chrom_positions[chrom] = list(np.random.sample(marker_size))
		chrom_positions[chrom].sort()
	
	chrom_pos_vec = [x for i in chrom_positions for x in i]
	
	parent_a = p.generate_parent(marker_size * chrom_quantity, ploidy, [1])
	parent_b = p.generate_parent_plus(parent_a)
	
	offs = ch.generate_offspring_f1(pop_size, parent_a, parent_b, chrom_quantity, chrom_size, chrom_pos_vec, marker_size, r_rate, ploidy)
	offs_t = ch.generate_error(e_rate, ch.transform_matrix(offs))
	
	pos = [x for x in range(markers_quantity * chrom_quantity)]
	#print pos
	mix = list(pos)
	np.random.shuffle(mix)
	
	new_pop = ch.mix_offspring(offs_t, pos, mix)
	#print new_pop
	
	result1 = ut.generate_one_map_file(new_pop, mix, "f2", "OneMap" + ".raw")
	result2 = ut.generate_one_map_file(offs_t, pos, "f2", "ResultOM" + ".raw")
	#
	result3 = ut.generate_mst_map_file(new_pop, mix, "MstMap" + ".txt")
	result4 = ut.generate_mst_map_file(offs_t, pos, "ResultMM" + ".txt")
	
	result5 = ut.generate_map_disto_file(new_pop, mix, "MapDisto" + ".xls")
	result6 = ut.generate_map_disto_file(offs_t, pos, "ResultMD" + ".txt")
	
# launch
if __name__ == "__main__":
    app.run()
