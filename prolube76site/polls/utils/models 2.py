# file was created to test the model mixins' features 
# Book Tile: Django 2 Web Development CookBook



# to make use of mixins, we simply import it and extend our models.
# from utils.models import CreationModificationDateMixin


# utils/models.py

from django.db import models
from django.template import loader
from danjo.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

class CreationModificationDateMixin (models.Model):
    "abstract base class that creates and updates the time"
    class Meta:
        abstract=True

    createdDt=models.DateTimeField(
        _("creating date and time"),
        auto_now_add=True
    )

    updatedDt=models.DateTimefiled(
        _("updating the time"),
        auto_now=True
        
    )    

class MetaTagsMixins(models.Model):

# abstract base class for generating meta tags
    class Meta:
        abstract = True
    
    meta_keywords=models.CharField(
        _("Keywords"),
        max_ength=255,
        blank=True,
        help_text= _("Separated by Comma")
    )
    meta_description=models.charfield(
       _("Description"),
       max_length=255,
       blank=True
    )
    meta_author=models.CharField(
        _("Author"),
        max_length=255,
        blank=True
    )
    meta_copyright=models.CharField(
        _("Copyright"),
        max_length=255,
        blank=True
    )


    def get_meta (self, name, content):
        tag=""
        if name and content:
            tag = loader.render_to_string('utils/meta.html', {
                'name': name,
                'content': content
            })
        return mark_safe(tag)
    
    def get_meta_keywords(self):
        return self.get_meta("keywords", self.meta_keywords)
    
    def get_meta_description (self):
        return self.get_meta('description',self.meta_description)

    def get_meta_author (self):
        return self.get_meta('author',self.meta_author)
    
    def get_meta_copyright(self):
        return self.get_meta('copyright', self.meta_copyright)
