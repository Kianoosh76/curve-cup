from django.contrib import admin
from django.contrib.admin.options import StackedInline

from groups.models import Player, Group, Score


class PlayerInline(StackedInline):
    model = Player
    fields = ['name']


class GroupAdmin(admin.ModelAdmin):
    fields = ['name']
    inlines = [PlayerInline]


admin.site.register(Group, GroupAdmin)
admin.site.register(Score)