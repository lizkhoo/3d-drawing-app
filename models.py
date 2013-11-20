# mongoengine database module
from mongoengine import *
from flask.ext.mongoengine.wtf import model_form

from datetime import datetime
import logging


class Design(Document):
	
	designer = StringField(max_length=120, required=True, verbose_name="Name")
	title = StringField(max_length=120, required=True, verbose_name="Drawing Title")
	slug = StringField()
	design = StringField(verbose_name="Design Data")
	image = StringField(required=True, max_length=255)

	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())

	# Category is a list of Strings
	categories = ListField(StringField(max_length=30))

DesignForm = model_form(Design)

