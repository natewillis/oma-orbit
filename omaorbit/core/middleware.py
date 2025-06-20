from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

class DynamicSiteMiddleware:
    """
    Middleware that sets the site based on the request's domain.
    Uses Django's built-in sites framework.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the domain from the request
        domain = request.get_host()
        
        # Try to find a site matching the domain
        try:
            site = Site.objects.get(domain=domain)
            # Set the SITE_ID setting for this request
            settings.SITE_ID = site.id
        except Site.DoesNotExist:
            # If no site matches, use the default site
            # The default SITE_ID from settings will be used
            pass
        
        # Process the request
        response = self.get_response(request)
        
        return response
