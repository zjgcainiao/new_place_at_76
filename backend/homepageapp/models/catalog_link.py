# this model stores specs data related to vendors which provide catelog links. VendorLink stores the actual format of the link used.
# could be outdated for future use.
from .base import models, InternalUser


class CatalogLinks(models.Model):
    catalog_link_id = models.AutoField(primary_key=True)
    catalog_link_file_used = models.CharField(
        max_length=50, blank=True, null=True)
    catalog_link_display_name = models.CharField(
        max_length=50, blank=True, null=True)
    catalog_link_interface_version = models.CharField(
        max_length=10, blank=True, null=True)
    catalog_link_auth_code = models.CharField(
        max_length=50, blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='catelog_links_created_by', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(
        InternalUser, related_name='catelog_links_updated_by', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'catalog_links_new_03'
        ordering = ['-catalog_link_id']
        verbose_name = '(Vendor) Catalog Link'
        verbose_name_plural = '(Vendor) Catalog Links'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.updated_by
        super().save(*args, **kwargs)