from django.contrib import admin

from scan import Scan, Scanner

for model in Scan, Scanner: admin.site.register(model)