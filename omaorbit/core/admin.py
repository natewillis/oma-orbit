from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site
from .models import SiteConfig

class SiteConfigInline(admin.StackedInline):
    model = SiteConfig
    can_delete = False
    verbose_name_plural = 'Site Configuration'

# Unregister the default Site admin
admin.site.unregister(Site)

# Register Site with the SiteConfig inline
@admin.register(Site)
class CustomSiteAdmin(SiteAdmin):
    inlines = [SiteConfigInline]
    list_display = ('name', 'domain', 'get_template_dir')
    
    def get_template_dir(self, obj):
        try:
            return obj.config.template_dir
        except SiteConfig.DoesNotExist:
            return '-'
    get_template_dir.short_description = 'Template Directory'
