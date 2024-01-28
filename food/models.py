from django.db import models
from django.contrib.auth.models import User

# Create your models here.

 


    

    
class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)
    image = models.ImageField(upload_to='food/images', null=True, blank=True)
    def __str__(self):
        return self.name
    

class Food(models.Model):
    foodid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    rating = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='food/images')


    def __str__(self) -> str:
        return f"{self.name}"
    
class FoodWishList(models.Model):
    foodid = models.IntegerField(null=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    rating = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='food/images')


    def __str__(self) -> str:
        return f"{self.name}"

class FoodCardList(models.Model):
    foodid = models.IntegerField(null=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField()
    description = models.TextField()
    rating = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='food/images')


    def __str__(self) -> str:
        return f"{self.name}"
    

class HistoryList(models.Model):
    foodid = models.IntegerField(null=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField()
    description = models.TextField()
    rating = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='food/images')


    def __str__(self) -> str:
        return f"{self.name}"

       




STAR_CHOICES =[
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
]

class Review(models.Model):
    food = models.ForeignKey(Food, on_delete = models.CASCADE, related_name= 'reviews')
    author = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(choices = STAR_CHOICES, max_length=10)

    def __str__(self):
        # return f"{self.author.first_name} {self.author.last_name}"
        return self.body

