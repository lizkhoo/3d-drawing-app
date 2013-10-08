# mongoengine database module
from mongoengine import *
from datetime import datetime
import logging


class Design(Document):
	
	designer = StringField(max_length=120, required=True, verbose_name="Your Name")
	title = StringField(max_length=120, required=True)
	slug = StringField()
	design = StringField(required=True, verbose_name="Title of Design")

	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())

	# Category is a list of STrings
	categories = ListField(StringField(max_length=30))
