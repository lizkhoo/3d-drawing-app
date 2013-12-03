import os, datetime
import re
from flask import Flask, request, render_template, redirect, abort, flash, json, jsonify
from unidecode import unidecode

# mongoengine database module
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__) #create our flask app
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

#-- Database Connection --
# MongoDB connection to MongoLab's database
app.config['MONGODB_SETTINGS'] = {'HOST':os.environ.get('MONGOLAB_URI'), 'DB': 'mofongousers'}
app.logger.debug("Connecting to MongoLabs")
db = MongoEngine(app)

# app.run(debug = True)

# import data models
import models

# checkbox of categories
categories = ['home good','accessory','art piece']

# --Routes--
# homepage
@app.route("/", methods=['GET','POST'])
def index():

	# render template
	templateData = {
		'designs' : models.Design.objects().order_by('+timestamp'),
		'categories' : categories
	}

	return render_template('main-gallery.html', **templateData)


@app.route("/draw", methods=['GET','POST'])
def draw():

	design = models.Design.objects()
	design_form = models.DesignForm(request.form)
	newdesign = ""

	if request.method == "POST" and design_form.validate():

		# get form data
		design = models.Design()
		design.designer = request.form.get('designer', 'anonymous')
		design.title = request.form.get('title', 'no title')
		design.slug = slugify(design.title + " " + design.designer)
		design.design = request.form.get('design', '')
		design.image = request.form.get('image', '')
		design.categories = request.form.getlist('categories')
		design.metadata = request.form.get('metadata', '')
		# use .getlist for HTTP Get forms with checkboxes, bc it returns a list

		design.save()

		# direct browser to homepage
		return redirect('/')

	else:
	
		#form management stuff
		if request.method == "POST" and request.form.getlist('categories'):
			for c in request.form.getlist('categories'):
				design_form.categories.append_entry(c)

		if request.method == "POST" and request.form.get('design','') is not '':
			newdesign = request.form.get('design')

		templateData = {
			'categories' : categories,
			'form' : design_form,
			'newdesign' : newdesign,
			'design' : design
		}

		return render_template('david-drawing-final.html', **templateData)


@app.route("/about")
def about():

	return "this is the about page"


@app.route("/categories/<cat_name>")
def by_category(cat_name):

	# pull all designs with matching cat_name in categories
	try:
		designs = models.Design.objects(categories=cat_name)

	# if not found, abort with 404 page
	except:
		abort(404)

	# create template of data for rendering
	templateData = {
		'current_category' : {
			'slug' : cat_name,
			'name' : cat_name.replace('_', ' ')
		},
		'designs' : designs,
		'categories' : categories
	}

	return render_template('category_listing.html', **templateData)


@app.route("/designs/<proj_slug>", methods=['GET', 'POST'])
def design_detail(proj_slug):

	# update entry with new data
	if request.method == 'POST':

		try:
			design = models.Design.objects.get(slug=proj_slug)
			
		except:
			raise

		designForm = models.DesignForm(request.form)

		if designForm.validate():
			updateData = {
				'set__title' : request.form.get('title'),
				'set__designer' : request.form.get('designer'),
				'set__design' : request.form.get('design'),
				'set__categories' : request.form.getlist('categories')
			}
			design.update(**updateData)

			flash('Update successful!')

			templateData = {
				'design' : models.Design.objects(),
				'categories' : categories
			}

			return redirect('/')

		else: 
			
			templateData = {
				'design' : design,
				'design_id' : design.id,
				'form' : designForm,
				'categories' : categories
			}

			return render_template('david-drawing-final.html', **templateData)

	# just show the design entry
	else:
		# get the design convert it to the model form, this prepopulates the form
		try:

			designDocument = models.Design.objects.get(slug=proj_slug) # query for single document in Mongo where slug = proj_slug
			designForm = models.DesignForm(obj=designDocument) # populate the models wtform with the Mongo document (optional)

		except:
			raise

		# get all the data to populate template
		templateData = {
			'design' : designDocument,
			'design_id' : designDocument.id,
			'form' : designForm,
			'categories' : categories
		}

		return render_template('david-drawing-final.html', **templateData)



@app.route('/data/designs')
def data_designs():

	designs = models.Design.objects().order_by('+timestamp').limit(10)

	if designs:

		#list to hold array file
		alldesigns = []

		#prep data for json
		for i in designs:
			tmpData = dataToDict(i)

			# insert dictionary into list
			alldesigns.append( tmpData )

		#prep dictionary for JSON return
		data = {
			'status' : 'OK',
			'designs' : alldesigns
		}

		#jasonify from Flask converts dictionary and sets mime type to 'application/json'!
		return jsonify(data)

	else:
		error = {
			'status' : 'error',
			'message' : 'unable to retrieve data!'
		}
		return jsonify(error)


@app.route('/data/designs/<id>')
def data_design(id):

# query for designs - return oldest first, limit 10

	try:
		design = models.Design.objects.get(id=id)
		if design:
			tmpData = dataToDict(design)
			data = {
				'status' : 'OK',
				'design' : tmpData
			}

		return jsonify(data)

	except:
		error = {
			'status' : 'error',
			'message' : 'unable to retrieve data!' 
		}

		return jsonify(error)


def dataToDict(design):
	# make dictionary
	tmpData = {
		'id' : str(design.id),
		'designer' : design.designer,
		'title' : design.title,
		'design' : design.design,
		'timestamp' : str(design.timestamp)
	}

	return tmpData


@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'), 404


# slugify the title
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
	"""Generates an ASCII-only slug."""
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))



# -- Server on --
# start the webserver
if __name__ == "__main__":
	app.debug = True

	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)



















