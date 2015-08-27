import os
import numpy as np
import zipfile
from logic.Parent import Parent
from logic.Offspring import Offspring
from logic.Utilities import Utilities
from logic.Validator import Validator
from io import BytesIO
from StringIO import StringIO
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response, Response, send_file
from werkzeug import FileStorage
#from wtforms import Form, BooleanField, TextField, PasswordField, validators
 
# initialization
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(
    DEBUG = True,
)

# controllers
@app.route("/", methods=['POST', 'GET'])
def index():
	print "Entre a Index"
	error = ""
	if request.method == 'POST':
		print "Entre a If"
		
	else:
		error = 'Error!!'
	
	return render_template('index.html', error=error)
	
@app.route("/#panel-sim", methods=['POST', 'GET'])
def simulator():
	print "Entre a Sim"
	error = ""
	if request.method == 'POST':
		print "Entre a If"
		chrom_quantity = int(request.form['quantity_id']) # chromosome quantity, by default 1
		chrom_size = int(request.form['size_id']) # chromosome size, all with the same size, by default 1 Morgan
		pop_size = int(request.form['off_id']) # population size, by default 10
		marker_size = int(request.form['mark_id']) # markers quantity, by default 20
		ploidy = int(request.form['ploidy_id']) # ploidy, by default 2
		r_rate = float(request.form['r_rate_id']) # recombination rate, by default 0.1
		m_rate = float(request.form['m_rate_id']) # mutation rate, by default 0.001
		e_rate = int(request.form['e_rate_id']) # error rate, by default 10%
		seed = int(request.form['s_id']) # seed random, by default 2154
		mapdisto = 'off'
		onemap = 'off'
		mstmap = 'off'

		req = request.form.to_dict()
		if 'mapdisto_id' in req:
			mapdisto = str(request.form['mapdisto_id']) # checkbox mapdisto
		if 'onemap_id' in req:
			onemap = str(request.form['onemap_id']) # checkbox onemap
		if 'mstmap_id' in req:
			mstmap = str(request.form['mstmap_id']) # checkbox mstmap

		myzip = generate(chrom_quantity, chrom_size, pop_size, marker_size, ploidy, r_rate, m_rate, e_rate, seed, mapdisto, onemap, mstmap)
	else:
		error = 'Error!!'
		
	try:
		return send_file(myzip, attachment_filename="Files.zip", as_attachment=True)
	except Exception:
		pass

@app.route("/#panel-val", methods=['GET','POST'])
def validator():
	error = ""
	if request.method == 'POST':
		file1 = request.files['upload1']
		if file1:
			contents = file1.read()
		file2 = request.files['upload2']
		if file2:
			contents2 = file2.read()
			
		edit_d = 'off'
		kendall_t = 'off'
		graphic_c = 'off'

		req = request.form.to_dict()
		if 'ed_id' in req:
			edit_d = str(request.form['ed_id']) # checkbox edit distance
		if 'kt_id' in req:
			kendall_t = str(request.form['kt_id']) # checkbox Kendall Tau
		if 'gc_id' in req:
			graphic_c = str(request.form['gc_id']) # checkbox Graphic Comparison	
		
		#print columns2
		#return show_validation(columns, columns2)
		
	else:
		error = 'Error!!'
	
	return render_template('results.html', title='Results', contents=contents, contents2=contents2, error=error)
	
@app.route("/show_validation/<contents>/<contents2>")
def show_validation(contents, contents2):
	v = Validator()
	columns, columns2 = [], []
		
	c = contents2.split('\n')
	
	for line in c:
		d = line.split()
		columns.append(int(d[0]))
		
	c = contents.split('\n')

	for line in c:
		d = line.split()
		if d[0] == '1':
			columns2.append(int(d[2]))	
	
	c1 = [x for x in columns if x in columns2]
	print "edit_distance #1: ", v.edit_distance(c1, columns2)
	print "kendall_tau #1: ", v.kendall_tau_comp(c1, columns2)
	line = v.linear_regression(c1, columns2)
	img = StringIO()
	fig = v.graph_comparison(c1, columns2, 'bo', line, 'r-')
	fig.savefig(img)
	img.seek(0)
	
	return send_file(img, mimetype='image/png')


def generate(chrom_quantity, chrom_size, pop_size, marker_size, ploidy, r_rate, m_rate, e_rate, seed, mapdisto, onemap, mstmap):
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
	
	pos = [x for x in range(marker_size * chrom_quantity)]
	#print pos
	mix = list(pos)
	np.random.shuffle(mix)
	
	new_pop = ch.mix_offspring(offs_t, pos, mix)
	#print new_pop
	if onemap == 'on':
		result1 = ut.generate_one_map_file(new_pop, mix, "f2", "OneMap" + ".raw")
		result2 = ut.generate_one_map_file(offs_t, pos, "f2", "ResultOM" + ".raw")
	#
	if mstmap == 'on':
		result3 = ut.generate_mst_map_file(new_pop, mix, "MstMap" + ".txt")
		result4 = ut.generate_mst_map_file(offs_t, pos, "ResultMM" + ".txt")
		
	if mapdisto == 'on':
		result5 = ut.generate_map_disto_file(new_pop, mix, "MapDisto" + ".xls")
		result6 = ut.generate_map_disto_file(offs_t, pos, "ResultMD" + ".txt")
	
	zip_file = BytesIO()
	
	with zipfile.ZipFile(zip_file, 'a') as myzip:
		if onemap == 'on':
			myzip.write('OneMap.raw')
			myzip.write('ResultOM.raw')
		if mstmap == 'on':
			myzip.write('MstMap.txt')
			myzip.write('ResultMM.txt')
		if mapdisto == 'on':
			myzip.write('MapDisto.xls')
			myzip.write('ResultMD.txt')
	
	zip_file.seek(0)
		
	print "Despues de zipfile"
		
	return zip_file
	
# launch
if __name__ == "__main__":
    app.run()
