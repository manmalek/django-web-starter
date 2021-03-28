from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify
from django.core.cache import cache
from mptt.models import TreeForeignKey, MPTTModel, TreeManyToManyField
from ckeditor.fields import RichTextField

# Create your models here.
class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name

	class Meta:
			verbose_name_plural = "مشتریان"
			#app_label = "store"

#class Category(models.Model):
class Category(MPTTModel):
	name = models.CharField(max_length=200)
	available = models.BooleanField(default=True) 
	slug = models.SlugField(max_length=200, null=True, blank=True, unique=True)
	parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )

	def __str__(self):
		return self.name
	class Meta:
		verbose_name_plural = "دسته بندیها"
		app_label = "store"

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name, allow_unicode=True)#.replace(" ","-")
		super(Category, self).save()

class Product(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, allow_unicode=True, null=True, blank=True, unique=True)
	available = models.BooleanField(default=True) 
	description = RichTextField(blank=True, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	base_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True) 
	price = models.DecimalField(max_digits=12, decimal_places=0)
	digital = models.BooleanField(default=False, null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	category = TreeManyToManyField(Category, blank=True)
	date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "محصولات"

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name, allow_unicode=True)#.replace(" ","-")
		if self.quantity <= 0:
			self.quantity = None
		super(Product, self).save()

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name_plural = "سفارشات"		

	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "سفارش شده ها"

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address

	class Meta:
		verbose_name_plural = "آدرسهای حمل"

class Feature(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "ویژگیهای محصول"

class  ProductFeature(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	feature = models.ForeignKey(Feature, on_delete=models.SET_NULL, null=True)		
	value = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = "ویژگیهای محصولات"


class ProductImage(models.Model):
	pro_image = models.ImageField(null=True, blank=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

	@property
	def imageURL(self):
		try:
			url = self.pro_image.url
		except:
			url = ''
		return url

	class Meta:
		verbose_name_plural = "تصاویر محصولات"


#-- Singleton Pattern for Settings-----------------------------------------------------
class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)

class SiteSetting(SingletonModel):
	site_name = models.CharField(max_length=200)
	site_logo = models.ImageField(null=True, blank=True)
	show_no_quantity = models.BooleanField("نمایش کالاهای بدون موجودی",default=True) 
	show_quantity = models.BooleanField("نمایش موجودی کالا",default=True) 

	@property
	def logoURL(self):
		try:
			url = self.site_logo.url
		except:
			url = ''
		return url
	class Meta:
		verbose_name_plural = "تنظیمات اصلی سایت"
