from django.shortcuts import render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from .models import BlogPost
from django.http import Http404
import markdown

def post_detail(request, slug):
    # Get the current site
    current_site = get_current_site(request)
    
    # Get the post, ensuring it belongs to the current site
    try:
        post = BlogPost.objects.filter(sites=current_site).get(slug=slug)
    except BlogPost.DoesNotExist:
        raise Http404("Post not found on this site")
    
    # Convert markdown to HTML
    post_html = markdown.markdown(post.content, extensions=["fenced_code", "codehilite", "tables"])
    
    # Prepare context with site-specific data
    context = {
        'post': post,
        'post_html': post_html,
    }
    
    # Render the template with the context
    return render(request, 'blog/post_detail.html', context)
