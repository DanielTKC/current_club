from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.humanize.templatetags.humanize import intcomma
from django.dispatch import receiver

class UserManager(BaseUserManager):
    def  create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('You must enter an email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # We have to define custom related names to avoid conflict with django's Permissions Mixin

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="user_set_custom",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="user_set_custom",
        related_query_name="user",
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

        


class Match(models.Model):
    opponent = models.CharField(max_length=255)
    match_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    match_image = models.ImageField(upload_to='photos/match', null=True, blank=True)

    def __str__(self):
        return f"{self.opponent} on {self.match_date.strftime('%Y-%m-%d %H:%M')}"

class Suite(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    description = models.TextField(blank = True, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    suite_photo = models.ImageField(upload_to='photos/suite', null=True, blank=True)
    amenities = models.CharField(max_length=255,null = True, blank = True, default='')
    
    @property
    def total_price(self) :
        total_price = self.price * self.capacity
        return "$%s%s" % (intcomma(int(total_price)), ("%.02f" % total_price)[-3:])

    def __str__(self):
        return self.name

    def tickets_sold_for_match(self, match_id):
        """
        Returns the number of tickets sold for a specific match.
        """
        return self.reservation_set.filter(match_id=match_id).count()

    def tickets_available_for_match(self, match_id):
        """
        Calculates and returns the number of tickets available for a specific match.
        """
        reservations_count = self.tickets_sold_for_match(match_id)
        return max(self.capacity - reservations_count, 0)  # Ensures non-negative result
    
    

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Reservation for {self.suite.name} for {self.match} on {self.match.match_date.strftime('%Y-%m-%d')}"
    
    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['suite', 'match'], name='unique_reservation')
        ]

    def save(self, *args, **kwargs):
        if not self.pk:  # If creating a new reservation
            self.total_price = self.suite.price * self.suite.capacity # Example: simple pricing based on suite's price. Adjust as needed for dynamic pricing.
        super().save(*args, **kwargs)