from django.db import models


# Create your models here.

class Diagnostic(models.Model):
    """
    Класс описывающий вид  диагностики

    """

    type = models.CharField(max_length=200)

    image = models.ImageField(upload_to='diagnostic_img/')

    name = models.CharField(max_length=200, blank=True)

    slug = models.SlugField(max_length=200)

    description = models.TextField(blank=True)

    class Meta:
        ordering = ['type']
        indexes = [
            models.Index(fields=['type']),
        ]

    def __str__(self):
        return self.type


class AllDiagnostic(models.Model):
    name = models.CharField(max_length=200)

    user = models.ForeignKey('auth.User',
                             on_delete=models.CASCADE,
                             )

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        indexes = [
            models.Index(fields=['date'])
        ]

    def __str__(self):
        return self.name


class PhotoDiagnostic(AllDiagnostic):

    name = AllDiagnostic.name

    date = AllDiagnostic.date

    type = models.CharField(max_length=20, default='pho')

    result_diagnostic = models.JSONField(blank=True, default=dict)

    image_lateral = models.ImageField(upload_to=f'user_img/%Y.%m.%d.%H.%M',
                                      default=None)

    image_frontal = models.ImageField(upload_to=f'user_img/%Y.%m.%d.%H.%M',
                                      default=None)

    def load_json(self, json_file):
        self.result_diagnostic = json_file

    def get_json(self):
        return self.result_diagnostic
