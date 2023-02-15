from django.core.mail import send_mail
from django.utils import timezone
from auctioning.models import *
from django.http import HttpResponse


def announce_winner():
    for product in Product.objects.all():
        print(product)
        now = timezone.now()
        print(now > product.bidend)
        if now > product.bidend:
            if (product.winbid == 'No bids'):
                product.delete()
                continue
            winner = Profile.objects.get(newusername=product.winbid)
            body = 'Congratulations, ' + winner.newusername + \
                ' you are the winner of the auction for product ' + product.title
            winnerEmail = [winner.email]
            send_mail(
                'CONGRATULATIONS, YOU ARE THE AUCTION WINNER',
                body,
                'auctionappgroupcw@gmail.com',
                winnerEmail,
                fail_silently=True,
            )
            product.delete()
    return HttpResponse("SUCESS")
