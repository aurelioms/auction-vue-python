from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):

    username = models.CharField(max_length=50, unique=True)
    profile = models.OneToOneField(
        to='Profile',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    rquestion = models.ManyToManyField(
        to='Rquestion',
        blank=True,
        symmetrical=False,
        related_name='related_to',


    )
    questions = models.ManyToManyField(
        to='self',
        blank=True,
        symmetrical=False,
        through='Question',
        related_name='related_to'
    )
    '''
    products many to one relationship between all users evryone can see each others product ?

    '''
    products = models.ManyToManyField(
        to='Product',
        blank=True,
        symmetrical=False,
        related_name='related_to',
    )

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def to_dict(self):
        return {
            'username': self.username,
            'profile': self.profile.to_dict() if self.profile else None,
            'question': [question.to_dict() for question in self.questions]
        }


class Profile(models.Model):
    '''
    A Profile is simply a bit of text and/or image
    that a Member might or might not have, hence the
    OneToOne relationship in Member with null=True
    '''
    newusername = models.CharField(max_length=50, default="new")
    email = models.EmailField(max_length=245, null=True)
    proimage = models.ImageField(
        upload_to='images', default="images/profile.png")
    birth = models.DateField(null=True)

    def to_dict(self):
        return {
            'newusername': self.newusername,
            'email': self.email,
            'proimage': self.proimage.url if self.proimage else None,
            'birth': self.birth,
        }


class Product(models.Model):

    title = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='products')
    bidend = models.DateTimeField()
    winbid = models.CharField(max_length=100, default='No bids')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'image': self.image.url,
            'price': self.price,
            'description': self.description,
            'bidend': self.bidend.strftime("%Y-%d-%mT%H:%M"),
            'winbid': self.winbid,
        }

    def __str__(self):
        return self.title


class Question(models.Model):
    '''
    The Message models is the 'through' model for
    the 'message' ManyToMany relationship between Members
    '''

    sender = models.ForeignKey(
        to=Product,
        related_name='sent',
        on_delete=models.CASCADE
    )
    recip = models.ForeignKey(
        to=User,
        related_name='received',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=4096)
    public = models.BooleanField(default=True)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"From {self.sender} to {self.recip}"

    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender.username,
            'recip': self.recip.username,
            'text': self.text,
            'public': self.public,
            'time': self.time.strftime("%Y-%d-%mT%H:%M"),
        }


class Rquestion(models.Model):

    question = models.CharField(max_length=4096)
    answer = models.CharField(max_length=4096, default="No answer")
    productid = models.IntegerField()

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'productid': self.productid,
        }
