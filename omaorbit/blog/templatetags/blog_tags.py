from django import template
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

register = template.Library()

@register.filter
def belongs_to_site(post, site_id=None):
    """
    Check if a blog post belongs to a specific site.
    
    Usage:
        {% if post|belongs_to_site %}
            Post belongs to the current site
        {% endif %}
        
        {% if post|belongs_to_site:2 %}
            Post belongs to site with ID 2
        {% endif %}
    """
    if site_id is None:
        # This will be handled in the template context
        return True
    
    # Check if the post belongs to the site
    return post.sites.filter(id=site_id).exists()

@register.simple_tag(takes_context=True)
def site_posts_count(context, site_id=None):
    """
    Return the number of posts for a specific site.
    
    Usage:
        {% site_posts_count %}
        {% site_posts_count 2 %}
    """
    from blog.models import BlogPost
    
    if site_id is None:
        # Use the current site from the context
        request = context.get('request')
        if request:
            current_site = get_current_site(request)
            site_id = current_site.id
        else:
            # Fallback to default site
            site_id = 1
    
    # Count the posts for the site
    return BlogPost.objects.filter(sites__id=site_id).count()

@register.inclusion_tag('blog/tags/site_selector.html', takes_context=True)
def site_selector(context):
    """
    Render a site selector dropdown.
    
    Usage:
        {% site_selector %}
    """
    request = context['request']
    current_site = get_current_site(request)
    sites = Site.objects.all()
    
    return {
        'sites': sites,
        'current_site_id': current_site.id,
        'request': request,
    }
