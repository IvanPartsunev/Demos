from django.db import models


class CreatedOnEditedOnMixin(models.Model):
    created_on = models.DateField(auto_now_add=True)
    edited_on = models.DateField(aouto_now=True)

    class Meta:
        abstract = True
