"""
Site-specific configuration for the OMA Orbit project.
This module contains configuration for different sites in the multisite setup.
"""

# Dictionary mapping site IDs to their configurations
SITE_CONFIGS = {
    # Shiftoma site (ID: 1)
    1: {
        'name': 'shiftoma',
        'template_dir': 'core/shiftoma',
        'site_title': 'SHIFT OMA',
        'tagline': None,
        'site_meta': {
            'description': 'Shiftoma - A creative platform',
            'keywords': 'shiftoma, creative, design',
        },
    },
    
    # Reckless site (ID: 2)
    2: {
        'name': 'reckless',
        'template_dir': 'core/reckless',
        'site_title': 'Reckless Analysis',
        'tagline': 'Explore the unexpected',
        'site_meta': {
            'description': 'Reckless - Explore the unexpected',
            'keywords': 'reckless, creative, art',
        },
    },
    
    # Template for adding new sites
    # 3: {
    #     'name': 'site_name',
    #     'template_dir': 'core/site_name',
    #     'site_title': 'Site Title',
    #     'tagline': 'Site Tagline',
    #     'site_meta': {
    #         'description': 'Site description',
    #         'keywords': 'keywords, for, site',
    #     },
    # },
}

def get_site_config(site_id):
    """
    Get the configuration for a specific site.
    
    Args:
        site_id (int): The ID of the site.
        
    Returns:
        dict: The site configuration.
    """
    return SITE_CONFIGS.get(site_id, SITE_CONFIGS[1])  # Default to site ID 1 if not found
