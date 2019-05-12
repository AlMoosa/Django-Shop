from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from transliterate import translit
from django.urls import reverse
from decimal import Decimal
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('Категорія', max_length=50)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


def pre_save_category_slug(sender, instance, *args, **kwargs):
    try:
        if not instance.slug:
            slug = slugify(translit(str(instance.name), reversed=True))
            instance.slug = slug
    except Exception:
        if not instance.slug:
            slug = slugify(instance.name)
            instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


class Brand(models.Model):
    name = models.CharField('Бренд', max_length=50)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренди'

    def __str__(self):
        return self.name


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return f'{instance.slug}/{filename}'


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, verbose_name='Бренд', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name='Назва')
    description = models.TextField(verbose_name='Опис')
    slug = models.SlugField(blank=True, unique=True, verbose_name='Посилання')
    image = models.ImageField(verbose_name='Фото', upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Ціна')
    available = models.BooleanField(default=True, verbose_name='В наявності')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Корзинний товар'
        verbose_name_plural = 'Корзинні товари'

    def __str__(self):
        return f"Cart item for product {self.product.title}"


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    def __str__(self):
        return str(self.id)

    def add_to_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
        if new_item not in cart.items.all():
            cart.items.add(new_item)

    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()

    def change_qty(self, qty, item_id):
        cart = self
        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.qty = int(qty)
        cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
        cart_item.save()
        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()


ORDER_STATUS_CHOISES = (
    ('Прийнятий в обробку', 'Прийнятий в обробку'),
    ('Виконується', 'Виконується'),
    ('Оплачено', 'Оплачено')
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ForeignKey(Cart, on_delete=models.CASCADE, default = timezone.now())
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    buying_type = models.CharField(max_length=40, choices=(('Самовивіз', 'Самовивіз'), ('Доставка', 'Доставка')), default='Самовивіз')
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(max_length=500)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOISES, default='Прийнятий в обробку')

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def __str__(self):
        return f'Заказ №{str(self.id)}'