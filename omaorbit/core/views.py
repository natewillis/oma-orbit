from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from blog.models import BlogPost
from .utils import get_site_template_path
import markdown


def home(request):
    """
    Dynamic home view that serves different templates based on the current site.
    Uses Django's built-in sites framework.
    """
    # Get the current site
    current_site = get_current_site(request)
    
    # Get recent blog posts for the current site
    posts = BlogPost.objects.filter(sites=current_site).order_by('-created_at')[:50]
    
    # Prepare context with site-specific data
    context = {
        'posts': posts,
    }
    
    # Render the template with the context
    template_path = get_site_template_path('index.html', request=request)
    return render(request, template_path, context)


def about(request):
    """
    Dynamic about view that serves different templates based on the current site.
    Uses Django's built-in sites framework.
    """
    # Get the current site
    current_site = get_current_site(request)

    # Get the about page content for the current site
    print(current_site.config.about)
    about_html = markdown.markdown(current_site.config.about, extensions=["fenced_code", "codehilite", "tables"])
    
    
    # Prepare context with site-specific data
    context = {
        'about_html': about_html,
    }
    
    # Render the template with the context
    return render(request, 'core/about.html', context)