from django.contrib.sites.shortcuts import get_current_site

def get_site_template_path(template_name, request=None, site=None):
    """
    Get the site-specific template path based on the current site.
    
    Args:
        template_name (str): The name of the template file.
        request (HttpRequest, optional): The current request. Used to get the current site if site is not provided.
        site (Site, optional): A specific site to use. If not provided, the current site from the request will be used.
        
    Returns:
        str: The full template path including the site-specific directory.
    """
    if site is None and request is not None:
        # Get the current site from the request
        site = get_current_site(request)
    
    # Get the template directory for the current site
    try:
        template_dir = site.config.template_dir
    except (AttributeError, TypeError):
        # If site is None or doesn't have a config, use a default template directory
        site_name = getattr(site, 'name', 'default').lower().replace(' ', '')
        template_dir = f"core/{site_name}"
    
    # Return the full template path
    return f"{template_dir}/{template_name}"
