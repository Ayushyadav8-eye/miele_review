
from django.db import models


class Review(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Customer Feedback"
        verbose_name_plural = "Customer Feedback"

    def __str__(self):
        return f"{self.name} - {self.rating}/5"
