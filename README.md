# Django Robots

Dynamically alter the `robots.txt` file for your Django application. You can just
create a `robots.txt` file and attach it to a view, but this allows you to modify 
the rules without code changes.

## Usage

To use this application, add it to your `INSTALLED_APPS` and add the following
to your `urls.py`:
    
    from robots.views import RobotsListView
    
    ...
    url(r'^robots\.txt$', cache_page(settings.ROBOTS_CACHE_TIMEOUT)(RobotsListView.as_view()), name='robots'),
    ...
