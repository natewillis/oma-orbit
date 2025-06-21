import logging
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

logger = logging.getLogger(__name__)

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
        
        # Handle www. prefix
        if domain.startswith('www.'):
            domain_no_www = domain[4:]  # Remove 'www.'
        else:
            domain_no_www = domain
            
        # Special case for shiftoma.com
        if 'shiftoma.com' in domain or 'shiftoma.localhost' in domain:
            # Find the shiftoma site
            try:
                # Try to find by exact domain first
                site = Site.objects.get(domain=domain)
                logger.info(f"Found site by exact domain: {domain}, site ID: {site.id}")
            except Site.DoesNotExist:
                try:
                    # Try without www.
                    site = Site.objects.get(domain=domain_no_www)
                    logger.info(f"Found site by domain without www: {domain_no_www}, site ID: {site.id}")
                except Site.DoesNotExist:
                    try:
                        # Try to find by name containing 'shiftoma'
                        site = Site.objects.filter(name__icontains='shiftoma').first()
                        if site:
                            logger.info(f"Found site by name containing 'shiftoma': {site.name}, site ID: {site.id}")
                        else:
                            # If all else fails, use site ID 2 (from production settings)
                            site = Site.objects.get(id=2)
                            logger.info(f"Using site ID 2: {site.name}")
                    except Site.DoesNotExist:
                        logger.warning(f"Could not find shiftoma site, using default SITE_ID: {settings.SITE_ID}")
                        # The default SITE_ID from settings will be used
                        site = None
            
            if site:
                settings.SITE_ID = site.id
        # Special case for recklessanalysis.com
        elif 'recklessanalysis.com' in domain or 'reckless.localhost' in domain:
            # Find the reckless site
            try:
                # Try to find by exact domain first
                site = Site.objects.get(domain=domain)
                logger.info(f"Found site by exact domain: {domain}, site ID: {site.id}")
            except Site.DoesNotExist:
                try:
                    # Try without www.
                    site = Site.objects.get(domain=domain_no_www)
                    logger.info(f"Found site by domain without www: {domain_no_www}, site ID: {site.id}")
                except Site.DoesNotExist:
                    try:
                        # Try to find by name containing 'reckless'
                        site = Site.objects.filter(name__icontains='reckless').first()
                        if site:
                            logger.info(f"Found site by name containing 'reckless': {site.name}, site ID: {site.id}")
                        else:
                            # If all else fails, use site ID 1 (assuming it's reckless)
                            site = Site.objects.get(id=1)
                            logger.info(f"Using site ID 1: {site.name}")
                    except Site.DoesNotExist:
                        logger.warning(f"Could not find reckless site, using default SITE_ID: {settings.SITE_ID}")
                        # The default SITE_ID from settings will be used
                        site = None
            
            if site:
                settings.SITE_ID = site.id
        else:
            # For other domains, use the original logic
            try:
                # Try to find by exact domain first
                site = Site.objects.get(domain=domain)
                logger.info(f"Found site by exact domain: {domain}, site ID: {site.id}")
                settings.SITE_ID = site.id
            except Site.DoesNotExist:
                try:
                    # Try without www.
                    site = Site.objects.get(domain=domain_no_www)
                    logger.info(f"Found site by domain without www: {domain_no_www}, site ID: {site.id}")
                    settings.SITE_ID = site.id
                except Site.DoesNotExist:
                    logger.warning(f"No site found for domain: {domain}, using default SITE_ID: {settings.SITE_ID}")
                    # If no site matches, use the default site
                    # The default SITE_ID from settings will be used
                    pass
        
        # Process the request
        response = self.get_response(request)
        
        return response
