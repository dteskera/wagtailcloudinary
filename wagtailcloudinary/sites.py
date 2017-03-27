import cloudinary.api
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.views.decorators.cache import never_cache
from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.modal_workflow import render_modal_workflow


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('wagtailcloudinary/css/main.css'))


@hooks.register('insert_global_admin_js')
def global_admin_js():
    html = []
    scripts = [
        static('wagtailcloudinary/js/csrf-token.js'),
        static('js/jquery.ui.widget.js'),
        static('js/jquery.iframe-transport.js'),
        static('js/jquery.fileupload.js'),
    ]
    for item in scripts:
        html.append('<script src="{}"></script>'.format(item))
    return format_html(''.join(html))


def staff_nocache(view):
    return staff_member_required(never_cache(view))


class CloudinarySite():
    def __init__(self, name='cloudinary'):
        self.name = name
        w, h = getattr(settings, 'WAGTAILCLOUDINARY_ADMIN_IMAGE_SIZE', (130, 130))
        self.admin_image_version = 'w_{},h_{},c_fill'.format(w, h)
        self.base_url = settings.WAGTAILCLOUDINARY_BASE_URL

    def get_urls(self):
        from django.conf.urls import url
        urlpatterns = [
            url(r'^browse/$', staff_nocache(self.browse), name="browse"),
            url(r'^select/(.*)$', staff_nocache(self.select), name="select"),
            url(r'^update/(.*)$', staff_nocache(self.update), name="update"),
            url(r'^upload/$', staff_nocache(self.upload), name="upload"),
        ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'wagtailcloudinary', self.name

    def browse(self, request):
        params = {'max_results': 18, 'tags': True}
        if 'next' in request.GET:
            params['next_cursor'] = request.GET['next']
        tag = request.GET.get('tag', None)
        if tag:
            context = cloudinary.api.resources_by_tag(tag, **params)
        else:
            context = cloudinary.api.resources(**params)
        context['admin_image_version'] = self.admin_image_version
        if 'next' in request.GET or 'tag' in request.GET:
            template_name = 'wagtailcloudinary/include/browse_ajax.html'
            html = render_to_string(template_name, context)
            return JsonResponse({'html': html, 'next': context.get('next_cursor', None), 'tag': tag})
        else:
            tags = cloudinary.api.tags()
            context.update(tags)
            template_name = 'wagtailcloudinary/browse.html'
            return render_modal_workflow(request, template_name, 'wagtailcloudinary/browse.js', context)

    def upload(self, request):
        response = {'images': []}
        for image in request.FILES.getlist('images[]'):
            options = {}
            data = {
                'image': cloudinary.uploader.upload(image, **options),
                'admin_image_version': self.admin_image_version
            }
            data.update({'html': render_to_string('wagtailcloudinary/include/browse_item.html', data)})
            response['images'].append(data)
        return JsonResponse(response)

    def select(self, request, path):
        slugs = path.split('/')
        slugs.insert(2, self.admin_image_version)
        transformed = '/'.join(slugs)
        return render_modal_workflow(
            request,
            None,
            'wagtailcloudinary/image_chosen.js',
            {
                'image_json': {
                    'value': path,
                    'url': '{}{}'.format(self.base_url, transformed)
                }
            }
        )

    def update(self, request, public_id):
        data = {'error': True}
        if request.method == 'POST':
            tags = request.POST.get('tags', None)
            image = cloudinary.api.update(public_id, tags=tags)
            data['html'] = render_to_string('wagtailcloudinary/include/browse_item.html', {
                'image': image,
                'admin_image_version': self.admin_image_version,
            })
            data['error'] = False
        return JsonResponse(data)


site = CloudinarySite()
