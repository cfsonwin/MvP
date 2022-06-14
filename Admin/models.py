from django.db import models
from datetime import datetime

# Create your models here.
"""
All the Models class created here is a mapping to the tables in your database.
You must ensure all attributes defined in one class have the same column name in each table.
You can find the 'Setup' of the default database in MyProduct.settings.py.
"""


class Administrator(models.Model):
    admin_id = models.AutoField(primary_key=True)
    Email = models.CharField(max_length=100, unique=True)
    u_name = models.CharField(max_length=30, default='user')
    u_password = models.CharField(max_length=100)
    pw_salt = models.IntegerField()
    u_status = models.IntegerField(default=0)
    addtime = models.DateTimeField(default=datetime.now)


    def toDict(self):
        return {'id': self.admin_id,
                'u_name': str(self.u_name).split('/')[0],
                'Email': self.Email,
                }

    class Meta:
        db_table = 'Administrator'


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    Email = models.CharField(max_length=100, unique=True)
    u_name = models.CharField(max_length=30, default='user')
    u_password = models.CharField(max_length=100)
    pw_salt = models.IntegerField()
    u_status = models.IntegerField(default=0)
    addtime = models.DateTimeField(default=datetime.now)
    addr = models.CharField(max_length=100)
    loc = models.CharField(max_length=100)
    class Meta:
        db_table = 'Constructor'


class Product(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=50, default="virtual product")
    p_status = models.IntegerField(default=0)
    addtime = models.DateTimeField(default=datetime.now)
    search_id = models.CharField(max_length=40)
    description = models.TextField()

    class Meta:
        db_table = 'Product'


class Manufacturer(models.Model):
    m_id = models.AutoField(primary_key=True)
    contact = models.CharField(max_length=50)
    addr = models.CharField(max_length=400)
    loc = models.CharField(max_length=100)
    m_status = models.IntegerField(default=0)
    addtime = models.DateTimeField(default=datetime.now)
    description = models.TextField()
    m_name = models.CharField(max_length=100)
    m_password = models.CharField(max_length=100)
    pw_salt = models.IntegerField()

    class Meta:
        db_table = 'Manufacturer'


class CPmapping(models.Model):
    id = models.AutoField(primary_key=True)
    c_id = models.IntegerField()
    c_email = models.CharField(max_length=100)
    p_id = models.IntegerField()

    class Meta:
        db_table = 'cpmapping'


class PMmapping(models.Model):
    id = models.AutoField(primary_key=True)
    p_id = models.IntegerField()
    m_id = models.IntegerField()
    m_pnode = models.IntegerField()
    m_Tlevel = models.IntegerField()
    modify_log = models.TextField()
    add_time = models.DateTimeField(default=datetime.now)
    modify_time = models.DateTimeField(default=datetime.now)
    status = models.IntegerField(default=0)
    feedback = models.TextField()
    producing_period = models.CharField(max_length=50)
    m_status = models.IntegerField(default=0)
    access_right = models.IntegerField(default=4)

    class Meta:
        db_table = 'pmmapping'
