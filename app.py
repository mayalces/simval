import os
import random
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response, Response
from Parent import Parent
from Offspring import Offspring
from Utilities import Utilities

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
		quantity = request.form['quantity_id'] # cantidad de cromosomas, por defecto 4
		size = request.form['size_id'] # tamano de cada cromosoma, todos de igual tamano, po defecto 2500
		ploidy = request.form['ploidy_id'] # ploidia, por defecto diploides
		offs = request.form['off_id'] # tamano de la poblacion, por defecto 200
		pnull = request.form['p_null_id'] # porcentaje de poblacion nula, por defecto 5%
		print "Antes de generate"
		generate(quantity, size, ploidy, offs, pnull)
	else:
		error = 'Error!!'
	
	return render_template('index.html', error=error)

def generate(quantity, size, ploidy, offs, pnull):
	p = Parent()
	ch = Offspring()
	ut = Utilities()
	
	positions = p.generatePos(int(size))
	parentA = p.generateParent(int(size), int(ploidy))
	parentB = p.generateParentPlus(parentA, int(ploidy))
	
	recombFreq = ch.calculateProbs(positions)
	
	offs = ch.generateOffspring(int(size), parentA, parentB, recombFreq, int(pnull))
	
	mix = list(positions)
	random.shuffle(mix)
	
	newOffs = ch.mixOffspring(offs, positions, mix)
	
	result = ut.generateMSTMapFile(newOffs, mix, "MstMap1.txt")
	result2 = ut.generateMSTMapFile(offs, positions, "MstMap2.txt")
	
	def gen():
		print "Entre a gen()"
		f = open("MstMap1.txt", "r")
		for l in f.iter_lines():
			print l
			yield l +'\n'
			
	#response = make_response(gen())
	#response.headers["Content-Disposition"] = "attachment; filename=simulationData.txt"
	
	return Response(gen(), mimetype= "text/plain")

# launch
if __name__ == "__main__":
    app.run()
