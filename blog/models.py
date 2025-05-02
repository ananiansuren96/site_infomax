from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


from PIL import Image  # Импортируем Pillow
import os

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    views_count = models.IntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Сначала сохраняем изображение

        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)

            # Настроим максимальный размер (например, 400x400)
            target_size = (800, 800)

            # Если изображение меньше, растягиваем его до 400x400
            if img.width < target_size[0] or img.height < target_size[1]:
                img = img.resize(target_size, Image.Resampling.LANCZOS)  # Растягиваем изображение
            else: 
                img = img.resize(target_size, Image.Resampling.LANCZOS)
                

            img.save(img_path)  # Перезаписываем изображение

  
    def __str__(self):
        return self.title

