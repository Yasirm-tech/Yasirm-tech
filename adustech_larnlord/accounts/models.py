from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# --- Custom User Manager ---
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, full_name, phone_number, address, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            full_name=full_name,
            phone_number=phone_number,
            address=address,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'super_admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, username, full_name='admin', phone_number='0000000000', address='HQ', password=password, **extra_fields)

    def create_landlord(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'landlord')
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_rejected', False)
        extra_fields.setdefault('is_banned', False)
        extra_fields.setdefault('is_approved', False)

        extra_fields.setdefault('full_name', 'Landlord')
        extra_fields.setdefault('phone_number', '0000000000')
        extra_fields.setdefault('address', 'Unknown')

        return self.create_user(email, username, password=password, **extra_fields)

# --- Custom User Model ---
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('landlord', 'Landlord'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('banned', 'Banned'),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='landlord')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username or self.email
