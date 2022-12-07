from django.contrib import admin
from board.models import Board

class BoardAdmin(admin.ModelAdmin):
    list_display = ("num", "writer", "subject", "passwd", "content",
                    "readcount", "ref", "restep", "relevel", "regdate", "ip")

admin.site.register(Board, BoardAdmin)
