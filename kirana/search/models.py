# import uuid
# from django.db import models
# from django.contrib.postgres.fields import ArrayField

# class Search(models.Model):
#     id = models.UUIDField(primary_key=True, editable=False,
#                           default=uuid.uuid4)
#     words = ArrayField(models.CharField(max_length=100))
#     documentaries = models.ManyToManyField('documentaries.documentary',
#                                      related_name="searches")

#     class Meta:
#         verbose_name_plural = "Searches"

#     @property
#     def results(self):
#         return self.documentaries.count()
    

#     def __str__(self):
#         return ",".join(self.words)