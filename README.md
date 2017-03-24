# Use cloudinary within wagtail

## About
This package adds Cloudinary support to Wagtail CMS

## Installation
pip install -e git+git://github.com/dteskera/wagtailcloudinary.git#egg=wagtailcloudinary


## Configuration
Add app wagtailcloudinary in your INSTALLED_APPS list

    INSTALLED_APPS = [
        ...
        'wagtailcloudinary',
        ...
    ]

## Usage
in models.py

```
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page
from wagtailcloudinary.fields import CloudinaryField, CloudinaryWidget

class SomePage(Page):
    image = CloudinaryField()

    content_panels = Page.content_panels + [
        FieldPanel('image', widget=CloudinaryWidget),
    ]
```
