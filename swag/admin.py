from django.contrib import admin
from .models import swag
from .models import Categories,Customer,Product,Order

# Register your models here.
admin.site.register([swag])
admin.site.register([Categories])
admin.site.register([Customer])
admin.site.register([Product])
admin.site.register([Order])


