from django.contrib import admin

# Register your models here.

from .models import Developer, Skill, Message, Business, Availability, RoleLevel,RoleType, Conversation, Customer, Verifications

admin.site.register(Developer)
admin.site.register(Skill)
admin.site.register(Message)
admin.site.register(Business)
admin.site.register(Availability)
admin.site.register(RoleLevel)
admin.site.register(RoleType)
admin.site.register(Conversation)
admin.site.register(Customer)
admin.site.register(Verifications)
