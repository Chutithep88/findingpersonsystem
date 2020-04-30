from django.db import models
from django.contrib.auth.models import User
from PIL import Image

#ใช้เพื่อ upload image to cloudinary
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    #เนื่องจากต้องอัพโหลดรูปลง cloudinary เพื่อไว้อัพเดทลง heroku (webserver)
    image = CloudinaryField('image',default='v1587364309/defaultNew.png')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        # img = Image.open(self.image)

        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     img.save(self.image)
