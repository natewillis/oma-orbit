# OMA Orbit Multisite System

This Django project is set up to support multiple sites with different templates, styles, and content, all from a single codebase.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up the database:
   ```
   python manage.py migrate
   ```

3. Create the initial sites:
   ```
   python manage.py setup_sites
   ```

4. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

## Accessing Different Sites

The system is configured to serve different sites based on the domain:

- **Shiftoma**: [http://localhost:8000](http://localhost:8000)
- **Reckless**: [http://reckless.localhost:8000](http://reckless.localhost:8000)

For local development, you can add these domains to your hosts file:
```
127.0.0.1 localhost
127.0.0.1 reckless.localhost
```

## Adding a New Site

To add a new site to the system:

1. **Update the site configuration**:
   
   Edit `core/site_config.py` and add a new entry to the `SITE_CONFIGS` dictionary:

   ```python
   # Example for a new site with ID 3
   3: {
       'name': 'newsite',
       'template_dir': 'core/newsite',
       'site_title': 'New Site Title',
       'tagline': 'New Site Tagline',
       'site_meta': {
           'description': 'New site description',
           'keywords': 'new, site, keywords',
       },
   },
   ```

2. **Update the domain mapping**:
   
   Edit `settings.py` and add a new entry to the `SITE_DOMAINS` dictionary:

   ```python
   'newsite.localhost:8000': 3,  # New site
   ```

3. **Create the template directory structure**:
   
   ```
   mkdir -p core/templates/core/newsite
   mkdir -p core/static/core/newsite/css
   ```

4. **Create the base templates**:
   
   Create `core/templates/core/newsite/base.html` and `core/templates/core/newsite/index.html` based on the existing templates.

5. **Create the CSS files**:
   
   Create `core/static/core/newsite/css/base.css` for site-specific styles.

6. **Run the setup_sites command**:
   
   ```
   python manage.py setup_sites
   ```

7. **Access the new site**:
   
   [http://newsite.localhost:8000](http://newsite.localhost:8000)

## How It Works

The multisite system uses Django's sites framework with custom middleware to dynamically serve different templates and content based on the domain:

1. **DynamicSiteMiddleware**: Sets the current site ID based on the request's domain.
2. **site_config.py**: Contains configuration for each site, including template directories and site-specific settings.
3. **context_processors.py**: Makes site-specific data available to all templates.
4. **views.py**: Renders different templates based on the current site.

## Blog Posts and Site Integration

Blog posts in this system are associated with specific sites through a ManyToManyField relationship with Django's Site model. This allows for flexible content management across multiple sites.

### How Blog Posts and Sites Interact

1. **Model Relationship**: Each `BlogPost` has a `sites` field (ManyToManyField) that links it to one or more `Site` objects.

2. **Automatic Site Association**: When creating a new blog post:
   - The current site is pre-selected in the admin interface
   - If no sites are selected, the post is automatically associated with the default site
   - This ensures posts are always associated with at least one site

3. **Site-Specific Content Filtering**: 
   - Views filter blog posts using `BlogPost.objects.filter(sites__id=site_id)`
   - This ensures users only see content relevant to the current site
   - The same post can appear on multiple sites if desired

4. **Admin Interface Enhancements**:
   - The admin interface shows which sites each post is associated with
   - When creating a new post, the current site is pre-selected
   - Help text explains how the site selection affects post visibility

5. **Template Tags**:
   - Custom template tags like `{% if post|belongs_to_site %}` allow for conditional rendering
   - The `{% site_selector %}` tag provides a dropdown to switch between sites
   - The `{% site_posts_count %}` tag displays the number of posts for a site

### Adding Blog Posts

1. Go to the admin interface: [http://localhost:8000/admin/](http://localhost:8000/admin/)
2. Add a new blog post
3. Select which sites the post should appear on (the current site is pre-selected)
4. The post will only appear on the selected sites

### Viewing Posts Across Sites

The post detail page includes:
- Visual indicators showing which sites the post is available on
- A site selector to view the post on different sites (if available)
- For staff users, a direct link to edit the post in the admin
