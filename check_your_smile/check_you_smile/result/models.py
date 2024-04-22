from django.db import models


# Create your models here.


class ResultDiagnostic(models.Model):
    """
    Класс хранящий результат диагностики
    """

    user = models.ForeignKey('auth.User',
                             on_delete=models.CASCADE, )

    date = models.DateTimeField(auto_now_add=True)

    result_diagnostic = models.CharField(max_length=255)

    type_diagnostic = models.CharField(max_length=50)

    name = models.CharField(max_length=200, blank=True)

    choice = models.BooleanField(default=False)

    def get_json(self):
        return self.result_diagnostic

    def get_name(self):
        return self.user
