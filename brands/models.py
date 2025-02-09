from django.db import models
from products.base_models import BaseModel


class Brand(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='brand/', null=True, blank=True)

    def __str__(self):
        return self.name
