from django.contrib import admin

from .models import SheetRow, SheetTable


@admin.register(SheetTable)
class SheetTableAdmin(admin.ModelAdmin):
    list_display = ("name", "row_count", "header_row", "synced_at")
    readonly_fields = ("name", "columns", "header_row", "row_count", "synced_at")


@admin.register(SheetRow)
class SheetRowAdmin(admin.ModelAdmin):
    list_display = ("table", "position", "apercu")
    list_filter = ("table",)
    list_select_related = ("table",)

    @admin.display(description="Aperçu")
    def apercu(self, obj):
        return str(obj.data)[:120]
