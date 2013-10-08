import os, datetime
import re
from flask import Flask, request, render_template, redirect, abort
from unidecode import unidecode

# mongoengine database module
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__) #create our flask app
app.config['CSRF_ENABLED'] = False

#-- Database Connection --
# MongoDB connection to MongoLab's database
app.config['MONGODB_SETTINGS'] = {'HOST':os.environ.get('MONGOLAB_URI'), 'DB': 'mofongousers'}
app.logger.debug("Connecting to MongoLabs")
db = MongoEngine(app)

# import data models
import models

# checkbox of categories
categories = ['home good','accessory','art piece']

# --Routes--
# homepage
@app.route("/", methods=['GET','POST'])
def index():

	if request.method == "POST":

		# get form data
		design = models.Design()
		design.designer = request.form.get('designer', 'anonymous')
		design.title = request.form.get('title', 'no title')
		design.slug = slugify(design.title + " " + design.designer)
		design.design = request.form.get('design', '')
		#design.categories = request.form.get('categories')

		design.save()

		# direct browser to newly created design detail page
		return redirect('/designs/%s' % design.slug)

	else:
		# form management stuff
		if request.method == "POST" and request.form.getlist('categories'):
			for c in request.form.getlist('categories'):
				idea_form.categories.append_entry(c)

		# render template
		templateData = {
			'designs' : models.Design.objects(),
			'categories' : categories
		}

		return render_template("main.html", **templateData)


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


@app.route("/designs/<proj_slug>")
def design_detail(proj_slug):

	# pull all metadata about a design by the proj_slug
	try:
		design = models.Design.objects.get(slug=proj_slug)

	except:
		abort(404)

	templateData = {
		'design' : design
	}

	return render_template('design_detail.html', **templateData)


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



















