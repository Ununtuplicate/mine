from __future__ import unicode_literals

from django.db import models
from meta.models import ModelMeta

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Collection, Page
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtailgmaps.edit_handlers import MapFieldPanel

from .blocks import BaseStreamBlock


class HomePage(Page):
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

@register_snippet
class FooterText(models.Model):
    """
    This is editable text for site footer
    Uses decorator 'register_snippet' so that it can be accessed via admin
    Accessible on template via template tag defined in home/templatetags/navigation_tags.py
    """
    body = RichTextField()

    panels = [
        FieldPanel('body'),
    ]

    def __str__(self):
        return "Footer text"

    class Meta:
        verbose_name_plural = 'Footer Text'


@register_snippet
class People(index.Indexed, ClusterableModel):
    """
    Django model to store People objects
    Uses '@register_snippet' decorator so that it can be accessed via admin
        = via Snippets UI (/admin/snippets/base/people)

    'People' uses 'ClusterableModel'
        Allows relationship with another model to be stored locally to the 'parent' model
        e.g. PageModel
        until parent is explicitly saved
        Allows editor to use 'Preview' button (=preview content) without saving relationships to db
        https://github.com/wagtail/django-modelcluster
    """
    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    job_title = models.CharField("Job title", max_length=254)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('first_name', classname="col6"),
        FieldPanel('last_name', classname="col6"),
        FieldPanel('job_title'),
        ImageChooserPanel('image')
    ]

    search_fields = [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]

    @property
    def thumb_image(self):
        # Returns empty string is no profile picture or rendition file can't be found
        try:
            return self.image.get_rendition('fill-50x50').img_tag()
        except:
            return ''

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'


def children(self):
    return self.get_children().specific().live()


