from django.contrib import admin
# from django.contrib import admin
# from django.contrib import admin
# Register your models here.
from .models import Procurement,Sale,CreditSale, Produce, Supplier, Branch
admin.site.register(Procurement)
admin.site.register(Sale)
admin.site.register(CreditSale)
# admin.site.register(CreditList)

# admin.site.register(FAQ)
admin.site.register(Produce)
admin.site.register(Supplier)
admin.site.register(Branch)