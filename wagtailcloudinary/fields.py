import cloudinary
import re
from django.conf import settings
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
from django.db.models import CharField
from django.forms.widgets import TextInput
from django.template.loader import render_to_string

CLOUDINARY_FIELD_DB_RE = r'(?:(?P<resource_type>image|raw|video)/(?P<type>upload|private|authenticated)/)?(?:v(?P<version>\d+)/)?(?P<public_id>.*?)(\.(?P<format>[^.]+))?$'


class CloudinaryResource(cloudinary.CloudinaryResource):
    @property
    def base_url(self):
        base_url = settings.CLOUDINARY_BASE_URL
        return '{base_url}{resource_type}/{type}'.format(
            base_url=base_url, resource_type=self.resource_type, type=self.type)

    @property
    def versioned_public_id(self):
        version = 'v{}/'.format(self.version) if self.version else ''  # if '/' not in self.public_id else 'v1/'
        return '/{version}{public_id}'.format(
            version=version, public_id=self.public_id)


def str_to_cloudinary_resource(value, resource_type='image', type='upload'):
    m = re.match(CLOUDINARY_FIELD_DB_RE, value)
    resource_type = m.group('resource_type') or resource_type
    upload_type = m.group('type') or type
    return CloudinaryResource(
        type=upload_type,
        resource_type=resource_type,
        version=m.group('version'),
        public_id=m.group('public_id'),
        format=m.group('format')
    )


class CloudinaryWidget(TextInput):
    input_type = 'text'

    class Media:
        js = (
            'wagtailcloudinary/js/cloudinary-field.js',
        )

    def render(self, name, value, attrs=None):
        w, h = getattr(settings, 'WAGTAILCLOUDINARY_ADMIN_IMAGE_SIZE', (165, 165))
        if isinstance(value, str):
            value = str_to_cloudinary_resource(value)
        admin_image_version = 'w_{},h_{},c_fill'.format(w, h)
        context = {
            'widget': {
                'name': name,
                'value': value
            },
            'image': value,
            'width': w,
            'height': h,
            'admin_image_version': admin_image_version,
        }
        return render_to_string("wagtailcloudinary/include/input.html", context)


class CloudinaryField(CharField):
    description = "CloudinaryField"

    def __init__(self, *args, **kwargs):
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        self.type = kwargs.pop("type", "upload")
        self.resource_type = kwargs.pop("resource_type", "image")
        return super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value or isinstance(value, CloudinaryResource):
            return value
        return str_to_cloudinary_resource(value, self.resource_type, self.type)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def get_prep_value(self, value):
        if isinstance(value, CloudinaryResource):
            return value.get_prep_value()
        else:
            return value


FORMFIELD_FOR_DBFIELD_DEFAULTS[CloudinaryField] = {'widget': CloudinaryWidget}
