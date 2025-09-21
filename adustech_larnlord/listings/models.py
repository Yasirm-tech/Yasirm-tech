from django.db import models
from accounts.models import CustomUser




class HouseListing(models.Model):
    HOUSE_TYPE_CHOICES = [
        ('room', 'Room'),
        ('self_contain', 'Self Contain'),
        ('1_bedroom', '1 Bedroom Flat'),
        ('2_bedroom', '2 Bedroom Flat'),
        ('other', 'Other'),
    ]

    landlord = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='listings')
    house_type = models.CharField(max_length=50, choices=HOUSE_TYPE_CHOICES)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    contact = models.CharField(max_length=50)

    is_available = models.BooleanField(default=True,)

    
    def __str__(self):
        return f"{self.house_type} at {self.location} by {self.landlord.username}"

class HouseImage(models.Model):
        house_listing = models.ForeignKey(HouseListing, on_delete=models.CASCADE, related_name='images')
        image = models.ImageField(upload_to='HouseListing_images/') # 'HouseListing_images/' is a subfolder in MEDIA_ROOT
        caption = models.CharField(max_length=255, blank=True, null=True)

        def __str__(self):
            return f"Image for {self.house_listing}"        
