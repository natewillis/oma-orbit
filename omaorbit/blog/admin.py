from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'get_sites')
    list_filter = ('sites', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('sites',)
    
    def get_sites(self, obj):
        """
        Return a comma-separated list of sites this post is associated with.
        """
        return ", ".join([site.name for site in obj.sites.all()])
    get_sites.short_description = 'Sites'
    
    def get_form(self, request, obj=None, **kwargs):
        """
        Override to add help text to the sites field.
        """
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['sites'].help_text = (
            "Select the sites where this post should appear. "
            "A post will only be visible on the selected sites."
        )
        return form
    
    def get_changeform_initial_data(self, request):
        """
        Pre-select the current site when creating a new post.
        """
        initial = super().get_changeform_initial_data(request)
        
        # Get the current site
        current_site = get_current_site(request)
        
        # Pre-select the current site
        initial['sites'] = [current_site.id]
        
        return initial

# Register the admin class with the associated model
admin.site.register(BlogPost, BlogPostAdmin)
