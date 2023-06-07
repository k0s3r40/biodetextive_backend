from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import base64
import base64
import io
from PIL import Image
from django.conf import settings
class Specimen(models.Model):
    SPECIMEN_CATEGORIES = [
        ('PLANT', _('растение')),
        ('MUSHROOM', _('гъба')),
        ('ANIMAL', _('животно')),
        ('INSECT', _('насекомо')),
        ('OTHER', _('друг'))

    ]
    SPECIMEN_CLASSES = [
        ('COMMON', _('често срещано')),
        ('RARE', _('рядко срещано')),
        ('EPIC', _('епично')),
        ('LEGENDARY', _('легендарно')),
    ]

    class Meta:
        verbose_name = _('вид')
        verbose_name_plural = _('видове')

    name = models.CharField(max_length=255, blank=False, null=False, verbose_name=_('име'))
    points = models.IntegerField(default=0, verbose_name=_('точки'))
    category = models.CharField(max_length=10, choices=SPECIMEN_CATEGORIES, verbose_name=_('тип'))
    specimen_class = models.CharField(max_length=10, choices=SPECIMEN_CLASSES, verbose_name=_('клас'))
    description = models.TextField()


class SpecimenSighting(models.Model):
    class Meta:
        verbose_name = _('забелязване на вид')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name=_('потребител'))
    specimen = models.ForeignKey(Specimen, on_delete=models.CASCADE, verbose_name=_('вид'))
    image = models.TextField(verbose_name=_('изображение'))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('ширина'))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('дължина'))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('време на създаване'))
    europeana_data = models.JSONField(blank=True, null=True)

    @property
    def image_url(self):
        return settings.HOST_NAME+reverse('preview-image', args=[self.pk])
    @property
    def get_image(self):
        image_bytes = base64.b64decode(self.image)
        image = Image.open(io.BytesIO(image_bytes))
        return image

    @property
    def specimen_class(self):
        return self.specimen.specimen_class

