from django.db import models
from django.utils.text import slugify
from django.contrib.sites.models import Site
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from markdownx.models import MarkdownxField

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = MarkdownxField()
    cover_image = models.ImageField(upload_to='blog_covers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sites = models.ManyToManyField(Site)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        """
        Returns the URL to access a particular blog post.
        """
        return reverse('blog:post_detail', args=[self.slug])
        
    def ensure_site_association(self):
        """
        Ensure that the post is associated with at least one site.
        If no sites are associated, associate with the default site.
        """
        if not self.sites.exists():
            default_site = Site.objects.get(id=settings.SITE_ID)
            self.sites.add(default_site)


@receiver(post_save, sender=BlogPost)
def ensure_blog_post_has_site(sender, instance, created, **kwargs):
    """
    Signal handler to ensure that a blog post is always associated with at least one site.
    """
    if created:
        # For new posts, ensure site association after save
        instance.ensure_site_association()
