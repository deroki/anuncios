"""
Here models are in different modules and the models.py imports them from different modules like this
from model1 import *        # or the name of models you want to import
from model2 import User
or you might write all your models in models.py 
"""

from django.contrib import admin
from django.apps import apps

app = apps.get_app_config('main')

for model_name, model in app.models.items():
    admin.site.register(model)