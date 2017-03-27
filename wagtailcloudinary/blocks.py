from django import forms
from django.utils.functional import cached_property
from wagtail.wagtailcore.blocks import FieldBlock


class CloudinaryImageBlock(FieldBlock):

    def __init__(self, required=True, help_text=None, **kwargs):
        self.field_options = {
            'required': required,
            'help_text': help_text,
        }
        super().__init__(**kwargs)

    @cached_property
    def field(self):
        from .fields import CloudinaryWidget
        field_kwargs = {'widget': CloudinaryWidget()}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)
    #
    # def get_searchable_content(self, value):
    #     return [force_text(value)]

    class Meta:
        icon = "image"
