from django.contrib.sites.shortcuts import get_current_site

def site_settings(request):
    """
    Context processor that adds site-specific settings to the template context.
    Uses Django's built-in sites framework.
    """
    # Get the current site
    current_site = get_current_site(request)
    
    # Get the site configuration
    try:
        site_config = current_site.config
    except AttributeError:
        # If the site doesn't have a config, return minimal context
        return {
            'current_site': current_site,
            'site_name': current_site.name.lower().replace(' ', ''),
            'site_title': current_site.name,
            'site_tagline': None,
            'site_meta': {
                'description': f"{current_site.name} - A website",
                'keywords': f"{current_site.name.lower().replace(' ', '')}, website",
            },
            'template_dir': f"core/{current_site.name.lower().replace(' ', '')}",
        }
    
    # Return a dictionary of variables to add to the template context
    return {
        'current_site': current_site,
        'site_name': site_config.name,
        'site_title': site_config.site_title,
        'site_tagline': site_config.tagline,
        'site_meta': site_config.site_meta,
        'template_dir': site_config.template_dir,
    }
