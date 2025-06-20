from django.db import models
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver

class SiteConfig(models.Model):
    """
    Extended configuration for Django's built-in Site model.
    """
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name='config')
    template_dir = models.CharField(max_length=100, help_text="Directory containing site templates")
    tagline = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Configuration for {self.site.name}"
    
    @property
    def name(self):
        """Return the site's name from the related Site model."""
        return self.site.name.lower().replace(' ', '')
    
    @property
    def site_title(self):
        """Return the site's title from the related Site model."""
        return self.site.name
    
    @property
    def site_meta(self):
        """Return a dictionary of meta information."""
        return {
            'description': self.meta_description or f"{self.site.name} - A website",
            'keywords': self.meta_keywords or f"{self.name}, website",
        }

@receiver(post_save, sender=Site)
def create_site_config(sender, instance, created, **kwargs):
    """
    Signal handler to create a SiteConfig when a new Site is created.
    """
    if created:
        # Create a default SiteConfig for the new Site
        template_dir = f"core/{instance.name.lower().replace(' ', '')}"
        SiteConfig.objects.create(
            site=instance,
            template_dir=template_dir,
        )
