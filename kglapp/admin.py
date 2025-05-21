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


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile  # Adjust if your UserProfile is elsewhere

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(UserAdmin, self).get_inline_instances(request, obj)

# Unregister the original User admin
admin.site.unregister(User)
# Register the new User admin that includes UserProfile inline
admin.site.register(User, UserAdmin)
