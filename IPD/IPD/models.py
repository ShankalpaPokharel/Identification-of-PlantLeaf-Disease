# from django.db import models
# from django.contrib.auth.models import User

# class DiseasePrediction(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='disease_images')
#     predicted_disease = models.CharField(max_length=100)
#     treatment = models.CharField(max_length=200)
#     how_to_use = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.predicted_disease
