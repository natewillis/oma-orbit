from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from core.models import SiteConfig

class Command(BaseCommand):
    help = 'Set up initial sites for the multisite configuration'

    def handle(self, *args, **options):
        # Define site configurations
        site_configs = {
            # Shiftoma site (ID: 1)
            1: {
                'domain': 'localhost:8000',
                'name': 'SHIFT OMA',
                'config': {
                    'template_dir': 'core/shiftoma',
                    'tagline': None,
                    'meta_description': 'Shiftoma - A creative platform',
                    'meta_keywords': 'shiftoma, creative, design',
                }
            },
            
            # Reckless site (ID: 2)
            2: {
                'domain': 'reckless.localhost:8000',
                'name': 'Reckless Analysis',
                'config': {
                    'template_dir': 'core/reckless',
                    'tagline': 'Explore the unexpected',
                    'meta_description': 'Reckless - Explore the unexpected',
                    'meta_keywords': 'reckless, creative, art',
                }
            },
        }
        
        # Create or update sites based on the site configuration
        for site_id, config in site_configs.items():
            # Create or update the site
            site, created = Site.objects.update_or_create(
                id=site_id,
                defaults={
                    'domain': config['domain'],
                    'name': config['name'],
                }
            )
            
            # Create or update the site configuration
            site_config, config_created = SiteConfig.objects.update_or_create(
                site=site,
                defaults={
                    'template_dir': config['config']['template_dir'],
                    'tagline': config['config']['tagline'],
                    'meta_description': config['config']['meta_description'],
                    'meta_keywords': config['config']['meta_keywords'],
                }
            )
            
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} site: {site.name} (ID: {site.id}, Domain: {site.domain})"))
            
            config_action = "Created" if config_created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{config_action} site configuration for {site.name}"))
        
        self.stdout.write(self.style.SUCCESS('Sites setup completed successfully!'))
