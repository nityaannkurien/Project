from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
import requests


from bs4 import BeautifulSoup
import urllib.request
# Create your views here.

def index(request):
    return render(request, 'index.html')

def loginUser(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user =  authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/create')
        else:
            messages.error(request, 'Invalid Email or Password')
            return render(request, 'login.html')
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/")

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = email
        fname = request.POST.get("firstname")
        lname = request.POST.get("lastname")
        password = request.POST.get("pass")
        if not User.objects.filter(username=username).exists():
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, 'Account has been created')
        else:
            messages.error(request, 'User already exists')
    return render(request, 'login.html')  

def create(request):
    if request.user.is_authenticated:
        username = request.user
        variable = {'name': username.first_name}
        return render(request, 'create.html', variable)
    return redirect('/login')

def edit_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')
        user = request.user
        if user.check_password(current_password):
            if user.username != username:
                user.username = username
                user.save()
            if new_password and new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
            return redirect('/edit')
    return render(request, 'edit.html')

def create_wishlist(request):
    if request.method == 'POST':
        wishlist_name = request.POST.get('wishlistName')
        if wishlist_name.strip() == '':
            messages.error(request, 'Please enter a wishlist name.')
        else:
            messages.success(request, f'Wishlist "{wishlist_name}" created! Start adding your wishes.')
    return render(request, 'wishing.html')

def index(request):
    return render(request, 'index.html')

def main(request):
    return render(request, 'main.html')

def api_view(request):
    return render(request, 'api.html')
def start_wishing(request):
    wishlist_name = request.GET.get("wishlistName")
    if not wishlist_name:
        return redirect(reverse("home"))  # Redirect to the home page if no wishlist name is provided
    # Redirect to the API URL with the wishlist name as a query parameter
    return redirect(f"https://example.com/api?wishlistName={wishlist_name}")
    HttpResponseRedirect('/main')

def scrape_flipkart(request):
    Product_name = []
    Prices = []
    Description = []
    Images = []

    url = "https://www.flipkart.com/search?q=mobiles+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    names = soup.find_all("div", class_="KzDlHZ")
    for i in names:
        name = i.text
        Product_name.append(name)

    prices = soup.find_all("div", class_="Nx9bqj _4b5DiR")
    for i in prices:
        price = i.text
        Prices.append(price)

    desc = soup.find_all("ul", class_="G4BRas")
    for i in desc:
        description = i.text
        Description.append(description)

    img_items = soup.find("div", {"class": "DOjaWF gdgoEp"})
    img_div = img_items.find_all(class_="_4WELSP")
    i = 0
    for img in img_div:
        img_tag = img.find("img")
        img_src = img_tag.get('src')
        if img_src[:1] == '/':
            image = 'https:' + img_src
        else:
            image = img_src
        Images.append(image)
        file_name = str(i)
        i += 1
        img_file = open(file_name + '.jpeg', 'wb')
        img_file.write(urllib.request.urlopen(image).read())
        img_file.close()

    context = {
        'products': zip(Product_name, Prices, Description, Images)
    }
    return render(request, 'scraped_data.html', context)


