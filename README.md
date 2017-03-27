# Use cloudinary within wagtail

## About
This package adds Cloudinary support to Wagtail CMS

## Installation
To install the package you can use the master branch like this:
```
pip install -e git+git://github.com/dteskera/wagtailcloudinary.git#egg=wagtailcloudinary
```
Or you can used a stable version:
```
pip install -e git+git://github.com/dteskera/wagtailcloudinary.git@v0.3#egg=wagtailcloudinary
```

## Configuration
Add app wagtailcloudinary in your INSTALLED_APPS list

```
INSTALLED_APPS = [
    ...
    'wagtailcloudinary',
    ...
]
```

in settings.py put your cloud_name, api_key and apy_secret into cloudinary configuration

```
import cloudinary

cloudinary.config(
    cloud_name=<YOUR_CLOUDINARY_CLOUD_NAME>,
    api_key=<YOUR_CLOUDINARY_API_KEY>,
    api_secret=<YOUR_CLOUDINARY_API_SECRET>,
)
```

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
