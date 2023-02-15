import json
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail


from .models import User, Profile, Product, Rquestion
from .forms import LoginForm, SignupForm


def signup_view(request):
    '''
    Signup function
    Users creating an account
    '''

    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # create a new user
            new_user = User.objects.create(username=username)
            new_profile = Profile.objects.create(
                newusername=username, birth=date.today(), email=email)
            # set user's password
            new_user.set_password(password)
            new_user.save()
            new_profile.save()
            # authenticate user
            # establishes a session, will add user object as attribute
            # on request objects, for all subsequent requests until logout
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('http://localhost:5173/')

    return render(request, 'auctioning/signup.html', {'form': SignupForm})


def login_view(request):
    '''
    Login function
    Users logging into the app
    '''

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('http://localhost:5173/')

            # failed authentication
            return render(request, 'auctioning/login.html', {
                'form': form
            })

        # invalid form
        return render(request, 'auctioning/login.html', {
            'form': form
        })

    return render(request, 'auctioning/login.html', {'form': form})


@login_required
def logout_view(request):
    auth.logout(request)
    return JsonResponse({
        'return': 'http://localhost:8000'})


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'GET':
        user = Profile.objects.get(newusername=user)
        profile = user.to_dict()
        return JsonResponse(
            {
                'profile': profile
            }
        )
        # return JsonResponse({
        #     'profile': [edit.newusername, edit.birth, edit.email, edit.proimage.url]})
    # if request.method == 'GET':
    #     edit = Profile.objects.get(newusername=user)
    #     return JsonResponse({
    #         'profile':[ edit.newusername, edit.birth, edit.email]})

    if request.method == 'POST':
        profile = Profile.objects.get(newusername=user)
        print(request.POST.get('email'))
        profile.email = request.POST.get('email')
        profile.birth = request.POST.get('birth')
        if (len(request.FILES) != 0):
            profile.proimage = request.FILES['proimage']
        profile.save()
        return JsonResponse({
            'message': 'success'
        })


@login_required
def api_search(request):
    products = []
    data = json.loads(request.body)
    query = data['query']
    fproducts = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query))
    for fproduct in fproducts:
        obj = {
            'id': fproduct.id,
            'title': fproduct.title,
            'description': fproduct.description,
            'price': fproduct.price,
        }
        products.append(obj)

    return JsonResponse({'products': products})


@login_required
def product_view(request):
    if request.method == 'POST':
        products = []
        data = json.loads(request.body)
        edit = Product.objects.get(id=data['object'])
        image = edit.to_dict()['image']
        obj = {
            'id': edit.id,
            'title': edit.title,
            'description': edit.description,
            'price': edit.price,
            'bidend': edit.bidend.strftime("%d/%m/%Y %H:%M:%S"),
            'winbid': edit.winbid,
            'bidstate': "",
            'image': image,
        }
        products.append(obj)

        return JsonResponse({'products': products})


@login_required
def bid_view(request):
    user = request.user
    products = []
    now = timezone.now()
    data = json.loads(request.body)
    bidder = Profile.objects.get(newusername=user)
    edit = Product.objects.get(id=data['object'])
    image = edit.to_dict()['image']
    if data['bid'] > edit.price and edit.bidend > now:
        obj = {
            'id': edit.id,
            'title': edit.title,
            'description': edit.description,
            'price': data['bid'],
            'bidend': edit.bidend,
            'winbid': bidder.newusername,
            'bidstate': "Your bid was successful",
            'image': image,
        }
        edit.price = data['bid']
        edit.winbid = bidder.newusername
        edit.save()
        products.append(obj)
    else:
        obj = {
            'id': edit.id,
            'title': edit.title,
            'description': edit.description,
            'price': edit.price,
            'bidend': edit.bidend,
            'winbid': edit.winbid,
            'bidstate': "Your bid was unsuccessful",
            'image': image,
        }
        products.append(obj)

    return JsonResponse({'products': products})


@login_required
def question_view(request):
    data = json.loads(request.body)
    questioned = []
    question = Rquestion.objects.filter(Q(productid__icontains=data['object']))
    print(question)
    for questions in question:
        obj = {
            'id': questions.id,
            'question': questions.question,
            'answer': questions.answer,
        }
        questioned.append(obj)
    return JsonResponse({
        'questions': questioned})


@login_required
def post_question(request):
    data = json.loads(request.body)
    questioned = []
    new_question = Rquestion.objects.create(
        question=data['question'], productid=data['object'])
    new_question.save()
    question = Rquestion.objects.filter(Q(productid__icontains=data['object']))
    print(question)
    for questions in question:
        obj = {
            'id': questions.id,
            'question': questions.question,
            'answer': questions.answer,
        }
        questioned.append(obj)
    return JsonResponse({
        'questions': questioned})


@login_required
def post_answer(request):
    data = json.loads(request.body)
    questioned = []
    answer = Rquestion.objects.get(id=data['id'])
    if answer.answer == "No answer":
        answer.answer = data['answer']
        answer.save()
    question = Rquestion.objects.filter(Q(productid__icontains=data['object']))
    for questions in question:
        obj = {
            'id': questions.id,
            'question': questions.question,
            'answer': questions.answer,
        }
        questioned.append(obj)
    return JsonResponse({
        'questions': questioned})


@login_required
def upload_product(request):
    if request.method == 'POST':
        if (len(request.FILES) != 0):
            product = Product(title=request.POST.get('title'), price=request.POST.get(
                'price'), description=request.POST.get('description'), image=request.FILES['image'], bidend=request.POST.get('bidend'),)
        else:
            product = Product(title=request.POST.get('title'), price=request.POST.get(
                'price'), description=request.POST.get('description'), bidend=request.POST.get('bidend'),)
        product.save()
        return JsonResponse({
            'message': 'success'
        })


def test_api(request):
    for product in Product.objects.all():
        print(product)
        now = timezone.now()
        print(now > product.bidend)
        if now > product.bidend:
            if (product.winbid == 'No bids'):
                product.delete()
                continue
            winner = Profile.objects.get(newusername=product.winbid)
            print("WINNER EMAIL", winner.email)
            winnerEmail = [winner.email]
            body = 'Congratulations, ' + winner.newusername + \
                ' you are the winner of the auction for product ' + product.title
            send_mail(
                'CONGRATULATIONS, YOU ARE THE AUCTION WINNER',
                body,
                'auctionappgroupcw@gmail.com',
                winnerEmail,
                fail_silently=True,
            )
            product.delete()
    return HttpResponse("SUCCESS")
