from django.contrib import admin
from member.models import Member

class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "passwd", "name", "email", "tel", "depart")
admin.site.register(Member, MemberAdmin)    

# Register your models here.
