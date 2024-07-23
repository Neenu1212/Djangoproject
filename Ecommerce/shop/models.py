from django.db import models

from django.db import models

# Create your models here.
class category(models.Model):
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    desc = models.TextField()

    def __str__(self):                  #this function is inside class & object  should have a name while displaying with admin
        return self.title
class product(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    desc = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)   #only one time
    updated = models.DateTimeField(auto_now=True)        #changes every time we update
    category=models.ForeignKey(category,on_delete=models.CASCADE)


    def __str__(self):                  #this function is inside class & object  should have a name while displaying with admin
        return self.title


