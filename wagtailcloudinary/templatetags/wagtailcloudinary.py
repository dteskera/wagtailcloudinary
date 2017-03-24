from django import template
from wagtailcloudinary.fields import CloudinaryResource

register = template.Library()


@register.filter()
def as_resource(image):
    if isinstance(image, str):
        image_arr = image.split('/')
        image = {
            'public_id': '/'.join(image_arr[2:]),
            'type': image_arr[1],
            'resource_type': image_arr[0],
            'tags': [],
        }
    res = CloudinaryResource(
        public_id=image['public_id'],
        version=image.get('version', None),
        type=image['type'],
        resource_type=image['resource_type'])
    res.tags = image.get('tags', None)
    return res


@register.inclusion_tag('wagtailcloudinary/include/cloudinary.html')
def version(image, trans=None, classes='', id='', description='', ratio='1:1', simple=False, width=100, height=100):
    if not isinstance(image, CloudinaryResource) and image:
        image = as_resource(image)
    return {
        'image': image,
        'trans': '/{}'.format(trans) if trans else '',
        'classes': classes,
        'id': id,
        'description': description,
        'ratio': ratio,
        'simple': simple,
        'width': width,
        'height': height,
    }


class AddGetParameter(template.Node):
    def __init__(self, values):
        self.values = values

    def render(self, context):
        req = template.Variable('request').resolve(context)
        params = req.GET.copy()
        for key, value in self.values.items():
            params[key] = value.resolve(context)
        return '?%s' % params.urlencode()


@register.tag
def add_get(parser, token):
    pairs = token.split_contents()[1:]
    values = {}
    for pair in pairs:
        s = pair.split('=', 1)
        values[s[0]] = parser.compile_filter(s[1])
    return AddGetParameter(values)
