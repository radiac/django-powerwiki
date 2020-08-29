from django.contrib import admin

from .models import Asset, Page, Wiki, WikiPermissions


class WikiPermissionsInline(admin.TabularInline):
    model = WikiPermissions
    extra = 2


class WikiAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "perm_read", "perm_edit"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        WikiPermissionsInline,
    ]


admin.site.register(Wiki, WikiAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = ["wiki", "title", "path", "is_locked"]
    list_filter = ("wiki", "is_locked")
    search_fields = ["title", "content"]
    prepopulated_fields = {"path": ("title",)}


admin.site.register(Page, PageAdmin)


class AssetAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(Asset, AssetAdmin)
