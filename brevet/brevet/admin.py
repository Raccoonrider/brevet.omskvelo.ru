from django.contrib import admin
from django.contrib import auth, sites

admin.site.unregister(auth.models.Group)
admin.site.unregister(sites.models.Site)