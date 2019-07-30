from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    viewscat = models.IntegerField(default=0)
    curtidas = models.IntegerField(default=0)
    slug = models.SlugField()
    #category_id = models.IntegerField(unique=True)
    def save(self, *args, **kwargs):
         #Uncomment if you don't want the slug to change every time the name changes
       #  if self.id is None:
           # self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.name
    class Meta:
        verbose_name_plural='Category'

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
 #   category_id = models.ForeignKey(Category,on_delete=models.CASCADE)


    def __unicode__(self):      #For Python 2, use o__str__ on Python 3
        return self.title

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username