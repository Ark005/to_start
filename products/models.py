from django.db import models
from django.urls import reverse

# Category Model
class Category(models.Model):
    title = models.CharField(max_length=300)
    primaryCategory = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"

#Product Model
class  Product(models.Model):
    mainimage = models.ImageField(upload_to='products/', blank=True)
    name = models.CharField(max_length=300)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    detail_text = models.TextField(max_length=1000, verbose_name='Detail Text')
    price = models.FloatField()
    

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("mainapp:product", kwargs={
            'slug': self.slug
        })
class Friend(models.Model):
    # NICK NAME should be unique
    nick_name = models.CharField(max_length=100, unique =  True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    likes = models.CharField(max_length = 250)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    lives_in = models.CharField(max_length=150, null = True, blank = True)

    def __str__(self):
        return self.nick_name

# class Friend(models.Model):
#     # NICK NAME should be unique
#     nick_name = models.CharField(max_length=100, unique =  True)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     likes = models.CharField(max_length = 250)
#     dob = models.DateField(auto_now=False, auto_now_add=False)
#     lives_in = models.CharField(max_length=150, null = True, blank = True)

#     def __str__(self):
#         return self.first_name + self.last_name