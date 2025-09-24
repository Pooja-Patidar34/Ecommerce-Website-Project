from django.db import models

class Category(models.Model):
        name=models.CharField(max_length=100, db_index=True)

        class Meta:
                verbose_name_plural='Categories'
        def __str__(self):
                return self.name
        
class Product(models.Model):
        category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
        name=models.CharField(max_length=100)
        description=models.TextField()
        price=models.DecimalField(max_digits=10,decimal_places=2)
        stock=models.PositiveBigIntegerField()
        image=models.ImageField(upload_to='products/')

        def __str__(self):
                return self.name