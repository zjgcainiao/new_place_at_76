from django.db import models
from internal_users.models import InternalUser


class DtcTroubleCodes(models.Model):

    dtc_touble_code_id = models.AutoField(primary_key=True)
    dtc_trouble_code = models.CharField(max_length=10, null=True, blank=True)
    dtc_trouble_code_description = models.CharField(
        max_length=500, null=True, blank=True)
    dtc_trouble_code_group_name = models.CharField(
        max_length=200, null=True, blank=True)
    dtc_trouble_code_is_active = models.BooleanField(default=True)
    dtc_trouble_code_meaning_html = models.TextField(null=True, blank=True)
    dtc_trouble_code_serverity_html = models.TextField(null=True, blank=True)
    dtc_trouble_code_potential_symptoms_html = models.TextField(
        null=True, blank=True)
    dtc_trouble_code_potential_causes_html = models.TextField(
        null=True, blank=True)
    dtc_trouble_code_troupleshooting_steps_html = models.TextField(
        null=True, blank=True)
    dtc_trouble_code_potential_repairs_html = models.TextField(
        null=True, blank=True)
    # dtc_trouble_code_potential_repairs_html = models.CharField(
    #     max_length=4000, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='dtc_trouble_code_created_by', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(
        InternalUser, related_name='dtc_trouble_code_updated_by', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):

        if self._state.adding:
            self.created_by = self.updated_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'dtc_trouble_codes_new_03'
        ordering = ["-dtc_touble_code_id"]
        indexes = [
            # Index to speed up searches based on created at, dtc_code_group_name, dtc_trouble_code
            models.Index(
                fields=['-created_at', 'dtc_trouble_code_group_name', 'dtc_trouble_code']),
        ]
        verbose_name = 'DTC Trouble Code'
        verbose_name_plural = 'DTC Trouble Codes'

    @staticmethod
    def truncate_to_twenty(text):
        if not text:
            return None
        return text[:20] + '...' if len(text) > 20 else text

    def __str__(self):
        code = self.dtc_touble_code.strip() or None
        code_desc = self.dtc_touble_code_description.strip() or None
        code_desc_truncated = self.truncate_to_twenty(code_desc)
        return f'code: {code}: {code_desc_truncated}'
