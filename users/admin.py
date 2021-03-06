from django.contrib import admin
from .models import CustomUser,StudentInterests,Subject,Course,University, Profile
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm,UserChangeForm

# Register your models here.



# class TeacherInline(admin.StackedInline):
#     model = TeacherMajors
#     can_delete = False 


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'username','get_country','is_student','is_teacher')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','username', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


    def get_country(self, instance):
        return instance.profile.country 
    get_country.short_description = 'Country'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(StudentInterests)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Profile)
admin.site.register(University)
