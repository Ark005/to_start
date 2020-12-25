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

class SubCategory(models.Model):
    name = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name
   

#Product Model
class  Product(models.Model):
    mainimage = models.ImageField(upload_to='products/', blank=True)
    name = models.CharField(max_length=300)
    slug = models.SlugField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    detail_text = models.TextField(max_length=1000, verbose_name='Detail Text')
    price = models.FloatField()
    tirazh = models.IntegerField(null=False)
    

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("mainapp:product", kwargs={
            'slug': self.slug
        })

class Friend(models.Model):

    dob = models.DateField(auto_now=False, auto_now_add=False)
    tirazh = models.IntegerField(null=False)

    def __str__(self):
        return self.nick_name


    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(Friend, self).save(*args, **kwargs)
 
    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

