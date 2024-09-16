from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser, Permission, Group

class Practice(models.Model):
    STATE_CHOICES=(
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'),
        ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'),
        ('HI', 'Hawaiian'), ('ID', 'Idaho'), ('IL', 'Illinois'),  ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
        ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'),
        ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'),
        ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
        ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'),
        ('WA', 'Washington'), ('WV' , 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')
    )
    name = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=50, default='', choices=STATE_CHOICES)
    city = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=200, default='')
    zipcode = models.CharField(max_length=10, default='')
    phone = models.CharField(max_length=15, default='', blank=True)
    website = models.URLField(default='', blank=True)
    description = models.TextField(default='', blank=True)

    def __eq__(self, other):
        if not isinstance(other, Practice):
            return False
        return (self.state, self.city, self.address, self.zipcode) == (other.state, other.city, other.address, other.zipcode)

    def __hash__(self):
        return hash((self.state, self.city, self.address, self.zipcode))

    def __str__(self):
        return f"{self.name}"

class Report(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('in progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )

    whistleblower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True )
    subject = models.CharField(max_length=300, default='')
    date_time = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, default= 'New', editable=True)
    notes = models.TextField(default='')

    def __str__(self):
        if self.whistleblower:
            return f"Report by {self.whistleblower.username} - {self.date_time}"
        else:
            return f"Anonymous report - {self.date_time}"


class ReportFile(models.Model):
    report = models.ForeignKey(Report, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='report_files/')

    def __str__(self):
        return f"File for report {self.report.id}"


class Profile(AbstractUser):
    ROLES = (
        ('anonymous_user', 'Anonymous'),
        ('common_user', 'Common User'),
        ('site_admin', 'Site Admin'),
        ('django_admin', 'Django Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLES)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    groups = models.ManyToManyField(Group, related_name='profiles')
    user_permissions = models.ManyToManyField(Permission, related_name='profiles')

    def __str__(self):
        return f"Profile of {self.user.username}"

