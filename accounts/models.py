from django.db import models
from django.contrib.auth.models import User

class Role(models.Model): 
          """
          this model is design for creating roles such as staff , Hr, Manager 
          """
          rname=models.CharField(max_length=100,unique=True)
          created_at=models.DateField(auto_now_add=True)
          updated_at=models.DateField(auto_now=True)

          def __str__(self):
             return self.rname

class RoleUser(models.Model):
        """
        this model is design for assign a role to user 
        """
        role=models.ForeignKey(Role,on_delete=models.CASCADE)
        user=models.ForeignKey(User,on_delete=models.CASCADE)


class Permission(models.Model):
          TYPE_CHOICES=(
                  ('module','module'),
                  ('path','path')
          )
          type=models.CharField(max_length=200, choices=TYPE_CHOICES)
          path=models.CharField(max_length=200, null=True, blank=True)
          module=models.CharField(max_length=200,null=True,blank=True )
          created_at=models.DateField(auto_now_add=True)
          updated_at=models.DateField(auto_now=True)

class RolePermissions(models.Model):
         """
         this model is assign permission for a specific role
         """
         role=models.ForeignKey(Role,on_delete=models.CASCADE) 
         permission=models.ForeignKey(Permission,on_delete=models.CASCADE)
         has_view=models.BooleanField(default=False)
         has_create=models.BooleanField(default=False) 
         has_edit=models.BooleanField(default=False)
         has_delete=models.BooleanField(default=False)
 
         created_at=models.DateField(auto_now_add=True)
         updated_at=models.DateField(auto_now=True)



