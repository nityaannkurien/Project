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
import requests
from .models import List,ListItem
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import pyrebase
from bs4 import BeautifulSoup
import urllib.request
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from urllib.parse import unquote
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore
cred = credentials.Certificate("C:\Django\WISHSTACK12\Project\wishstack-db-firebase-adminsdk-nqcon-fe31740038.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

# Create your views here.
firebaseConfig = {
  'apiKey': "AIzaSyDsyFTYrxJ4KOGEkGZ7ZZiJzIigvqhULMU",
  'authDomain': "wishstack-db.firebaseapp.com",
  'databaseURL': "https://wishstack-db-default-rtdb.firebaseio.com",
  'projectId': "wishstack-db",
  'storageBucket': "wishstack-db.appspot.com",
  'messagingSenderId': "809425693364",
  'appId': "1:809425693364:web:908ca30fc4f9f6194485e1",
  'measurementId': "G-T0FJ57Y7CY"
}
firebase=pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
database=firebase.database()

def index(request):
    return render(request, 'index.html')


def loginUser(request):
    print("hi", request.method)
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('pass')
        
        try:
            # Authenticate user using your custom method
            user = authe.sign_in_with_email_and_password(email, password)
            print(user)
            firebase_user = auth.get_user(user['localId'])
            print("Firebase user data:")
            print(f"Email: {firebase_user.email}")
            print(f"User ID: {firebase_user.uid}")
            print(f"Firebase user data: {firebase_user}")

            # Store user data in session
            request.session['user_email'] = firebase_user.email
            request.session['user_uid'] = firebase_user.uid

            # For simplicity, ensure the user exists in Django's User model or create one
            django_user, created = User.objects.get_or_create(username=email, defaults={'email': email})
            if created:
                django_user.set_password(password)
                django_user.save()

            # Log the user in
            login(request, django_user)

            return redirect('/create/')
        except Exception as e:
            messages.error(request, 'An unexpected error occurred: ' + str(e))
            
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/")

def signup(request):
    fname=request.POST.get('firstname')
    lname=request.POST.get('lastname')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    user=authe.create_user_with_email_and_password(email,password)
    data={"first name":fname,"last name":lname,"email":email}
    db.collection('user').document(email).set(data)

    return render(request, 'login.html')

"""if request.method == "POST":
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
    return render(request, 'login.html')  """

def create(request):
    print("dhoiusfoiefgofgfhsifhiurfreuhbfc",request)
    print("Full request object:", request)
    print("Request method:", request.method)
    print("Request GET parameters:", request.GET)
    print("Request POST parameters:", request.POST)
    print("Request user:", request.user)
     
    if request.user.is_authenticated:
        print("User is authenticated")
        username = request.user
        user_email = request.session.get('user_email')
        user_uid = request.session.get('user_uid')
        print("User email from session:", user_email)
        print("User UID from session:", user_uid)
        items = List.objects.all()
        variable = {
            'name': username.first_name,
            'listname': items,
            'email': user_email,
            'uid': user_uid
        }
        return render(request, 'create.html', variable)
    else:
        print("User is not authenticated")
        return redirect('/login/')
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
        if wishlist_name.strip() == "":
            messages.error(request, 'Please enter a wishlist name.')
        else:
            messages.success(request, f'Wishlist "{wishlist_name}" created! Start adding your wishes.')
    return render(request, 'wishing.html')



def index(request):
    return render(request, 'index.html')

def main(request):
    if request.method=="GET":
        # wishname = request.POST.get('wishname')
        # wishdesc = request.POST.get('wishdesc')
        
        # namew=List( wishlist_name = wishname,description = wishdesc, user=request.user)
        # namew.save()
        # Assuming 'a' is the user_id and 'product' is the wishlist_id
        user_email=str(request.user)
        user_ref = db.collection('user').document(user_email)
        wishlist_ref = user_ref.collection('wishlist').document('birthday')
        products_ref = wishlist_ref.collection('products')
        print(user_ref)

        # Get all products in the wishlist
        products = products_ref.get()
        product_data_list = []
        for product in products:
           product_data = product.to_dict()
           product_data_list.append(product_data)

        context = {
        'username': request.user,
        }

    # Check if product_data_list is not empty before adding it to the context
    if product_data_list:
        context['product_data_list'] = product_data_list

    return render(request, 'main.html', context)

def main4(request):
    if request.method=="GET":
        # wishname = request.POST.get('wishname')
        # wishdesc = request.POST.get('wishdesc')
        
        # namew=List( wishlist_name = wishname,description = wishdesc, user=request.user)
        # namew.save()
        # Assuming 'a' is the user_id and 'product' is the wishlist_id
        user_email=str(request.user)
        user_ref = db.collection('user').document(user_email)
        wishlist_ref = user_ref.collection('wishlist').document('anniversary')
        products_ref = wishlist_ref.collection('products')
        print(user_ref)

        # Get all products in the wishlist
        products = products_ref.get()
        product_data_list = []
        for product in products:
           product_data = product.to_dict()
           product_data_list.append(product_data)

        context = {
        'username': request.user,
        }

    # Check if product_data_list is not empty before adding it to the context
    if product_data_list:
        context['product_data_list'] = product_data_list

    return render(request, 'main4.html', context)

def main1(request):
    if request.method=="GET":
        # wishname = request.POST.get('wishname')
        # wishdesc = request.POST.get('wishdesc')
        
        # namew=List( wishlist_name = wishname,description = wishdesc, user=request.user)
        # namew.save()
        # Assuming 'a' is the user_id and 'product' is the wishlist_id
        user_email=str(request.user)
        user_ref = db.collection('user').document(user_email)
        wishlist_ref = user_ref.collection('wishlist').document('house_warming')
        products_ref = wishlist_ref.collection('products')
        print(user_ref)

        # Get all products in the wishlist
        products = products_ref.get()
        product_data_list = []
        for product in products:
           product_data = product.to_dict()
           product_data_list.append(product_data)

        context = {
        'username': request.user,
        }

    # Check if product_data_list is not empty before adding it to the context
    if product_data_list:
        context['product_data_list'] = product_data_list

    return render(request, 'main1.html', context)

   

def main2(request):
    if request.method=="GET":
        # wishname = request.POST.get('wishname')
        # wishdesc = request.POST.get('wishdesc')
        
        # namew=List( wishlist_name = wishname,description = wishdesc, user=request.user)
        # namew.save()
        # Assuming 'a' is the user_id and 'product' is the wishlist_id
        user_email=str(request.user)
        user_ref = db.collection('user').document(user_email)
        wishlist_ref = user_ref.collection('wishlist').document('wedding')
        products_ref = wishlist_ref.collection('products')
        print(user_ref)

        # Get all products in the wishlist
        products = products_ref.get()
        product_data_list = []
        for product in products:
           product_data = product.to_dict()
           product_data_list.append(product_data)

        context = {
        'username': request.user,
        }

    # Check if product_data_list is not empty before adding it to the context
    if product_data_list:
        context['product_data_list'] = product_data_list

    return render(request, 'main2.html', context)

def main3(request):
    if request.method=="GET":
        # wishname = request.POST.get('wishname')
        # wishdesc = request.POST.get('wishdesc')
        
        # namew=List( wishlist_name = wishname,description = wishdesc, user=request.user)
        # namew.save()
        # Assuming 'a' is the user_id and 'product' is the wishlist_id
        user_email=str(request.user)
        user_ref = db.collection('user').document(user_email)
        wishlist_ref = user_ref.collection('wishlist').document('baptism')
        products_ref = wishlist_ref.collection('products')
        print(user_ref)

        # Get all products in the wishlist
        products = products_ref.get()
        product_data_list = []
        for product in products:
           product_data = product.to_dict()
           product_data_list.append(product_data)

        context = {
        'username': request.user,
        }

    # Check if product_data_list is not empty before adding it to the context
    if product_data_list:
        context['product_data_list'] = product_data_list

    return render(request, 'main3.html', context)



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
    if request.method=="POST":
        username = request.POST.get("username")
        print("US",username)
    Product_name = []
    Prices = []
    Description = []
    Images = []
    url = "https://www.flipkart.com/search?q=mobiles+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+str(1)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    names = soup.find_all("div", class_="KzDlHZ")
    for name in names:
        Product_name.append(name.text)

    # Scrape product prices
    prices = soup.find_all("div", class_="Nx9bqj _4b5DiR")
    for price in prices:
        Prices.append(price.text)
    desc = soup.find_all("ul", class_="G4BRas")
    for d in desc:
        description = d.text
        Description.append(description)
   
     # Scrape images
    img_items = soup.find_all("div", class_="_4WELSP")
    for img_item in img_items:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images.append(img_src)
    

    # Define Images1 for the second set of products
    Images1 = []
    Product_name1=[]
    Prices1=[]
    Description1 = []
    url1 = "https://www.flipkart.com/search?q=bedsheet&sid=jra%2Cknw%2Cqcw&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_9_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_9_na_na_na&as-pos=2&as-type=RECENT&suggestionId=bedsheet%7CBedsheets&requestId=04de54c5-e4a5-4e25-af98-1629d4706010&as-backfill=on&page=2"
    r = requests.get(url1)
    soup = BeautifulSoup(r.text, "html.parser")
     # Scrape product names
    names = soup.find_all("a", class_="wjcEIp")
    for name in names:
        Product_name1.append(name.text)
    # Scrape product prices
    prices = soup.find_all("div", class_="Nx9bqj")
    for price in prices:
        Prices1.append(price.text)

    # Scrape product descriptions
    desc = soup.find_all("div", class_="NqpwHC")
    for d in desc:
        Description1.append(d.text)

    # Scrape images
    img_items = soup.find_all("div", class_="_4WELSP WH5SS-")
    for img_item in img_items:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images1.append(img_src)
        
        
    
# #Home Decor 

    Product_name2 = []
    Prices2 = []
    Images2=[]
    Description2=[]
    url2 = "https://www.flipkart.com/search?q=home+decorate+items&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=5"
    r2 = requests.get(url2)
    soup2 = BeautifulSoup(r2.text, "lxml")
     # Scrape product names
    names2 = soup2.find_all("a", class_="wjcEIp")
    for name in names2:
        Product_name2.append(name.text)

    # Scrape product prices
    prices2 = soup2.find_all("div", class_="Nx9bqj")
    for price in prices2:
        Prices2.append(price.text)
    desc = soup.find_all("div", class_="NqpwHC")
    for d in desc:
        Description2.append(d.text)

    # Scrape images
    img_items2 = soup2.find_all("div", class_="_4WELSP WH5SS-")
    for img_item in img_items2:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images2.append(img_src)
        
   #Earphones        
    Product_name4 = []
    Prices4 = []
    Images4=[]
    Description4=[]
    url4 = "https://www.flipkart.com/search?q=earphone+with+power+bank&sid=0pm%2Cfcn%2C821%2Ca7x%2C2si&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&as-pos=2&as-type=RECENT&suggestionId=earphone+with+power+bank%7CTrue+Wireless&requestId=1c7ae1bd-ed21-4897-9fb6-ebadcee2fabf&as-searchtext=powerbank%20and%20earphones"
    r4 = requests.get(url4)
    soup4 = BeautifulSoup(r4.text, "lxml")
    names4 = soup.find_all("a", class_="wjcEIp")
    for name in names4:
        Product_name4.append(name.text)
    prices4 = soup4.find_all("div", class_="Nx9bqj")
    for price in prices4:
        Prices4.append(price.text)
    desc = soup.find_all("div", class_="UkUFwK")
    for d in desc:
        Description4.append(d.text)

    img_items4 = soup4.find_all("div", class_="_4WELSP")
    for img_item in img_items4:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images4.append(img_src)

    context = {
        'products': zip(Product_name, Prices, Description, Images),
        'products1': zip(Product_name1, Prices1,Description1, Images1),
        'products2': zip(Product_name2, Prices2, Description2, Images2),
        'products4': zip(Product_name4, Prices4,Description4, Images4),
    }
    \
    return render(request, 'scraped_data.html', context)
    


def scrape_clothing(request):
    if request.method=="POST":
        username = request.POST.get("username")
        print("US",username)
    print("test")
    Product_name = []
    Prices = []
    Description = []
    Images = []
    url = "https://www.flipkart.com/search?q=tops+for+women&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=4"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    names = soup.find_all("div", class_="syl9yP")
    for name in names:
        Product_name.append(name.text)
    # Indian Rupee symbol
    prices = soup.find_all("div", class_="Nx9bqj")
    for price in prices:
        Prices.append(price.text)
    desc = soup.find_all("a", class_="WKTcLC")
    for d in desc:
        description = d.text
        Description.append(description)
   
    # The rest of your code for processing imagespage = urllib.request.urlopen(url)
    
    img_div = soup.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div:
        img_tag = img.find("img")
        img_src = img_tag.get('src')
        Images.append(img_src)
    

    # Define Images1 for the second set of products
    Images1 = []
    Product_name1=[]
    Prices1=[]
    Description1=[]
    url1 = "https://www.flipkart.com/search?q=men%20t%20shirt%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    r1 = requests.get(url1)
    soup1 = BeautifulSoup(r1.text, "html.parser")
    names1 = soup1.find_all("div", class_="syl9yP")
    for name in names1:
        Product_name1.append(name.text)
    # Indian Rupee symbol
    prices1 = soup1.find_all("div", class_="Nx9bqj")
    for price in prices1:
        Prices1.append(price.text)
    desc1 = soup1.find_all("a", class_="WKTcLC")
    for d in desc1:
        Description1.append(d.text)
    
    img_div1 = soup1.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div1:
        img_tag1 = img.find("img")
        img_src1 = img_tag1.get('src')
        Images1.append(img_src1)
        
        
    Product_name2 = []
    Prices2 = []
    Images2=[]
    Description2=[]
    url2 = "https://www.flipkart.com/search?q=boys+t+shirt+12%2F13+years&sid=clo%2Cash%2Cank%2Cpgi&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&as-pos=1&as-type=RECENT&suggestionId=boys+t+shirt+12%2F13+years%7CKids%27+T-shirts&requestId=4760a67d-8bf7-4c4e-adab-d9accf664d73&as-searchtext=boys%20t%20shirt%20"
    r2 = requests.get(url2)
    soup2 = BeautifulSoup(r2.text, "lxml")
    names2 = soup2.find_all("div", class_="syl9yP")
    for name in names2:
        Product_name2.append(name.text)
        print("Boys Clothing",name.text,"\n")
    # Indian Rupee symbol
    prices2 = soup2.find_all("div", class_="Nx9bqj")
    for price in prices2:
        Prices2.append(price.text)
    desc2 = soup2.find_all("a", class_="WKTcLC")
    for d in desc2:
        Description2.append(d.text)
        

    img_div2 = soup2.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div2:
        img_tag2 = img.find("img")
        img_src2 = img_tag2.get('src')
        Images2.append(img_src2)
        
    Product_name4 = []
    Prices4 = []
    Images4=[]
    Description4=[]
    url4 = "https://www.flipkart.com/search?q=girls%20dress%2011%2F12years%20frock%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    r4 = requests.get(url4)
    soup4 = BeautifulSoup(r4.text, "lxml")
    names4 = soup4.find_all("div", class_="syl9yP")
    for name in names4:
        Product_name4.append(name.text)
        # Indian Rupee symbol
    prices4 = soup4.find_all("div", class_="Nx9bqj")
    for price in prices4:
        Prices4.append(price.text)
    desc4 = soup4.find_all("a", class_="WKTcLC BwBZTg")
    for d in desc4:
        Description4.append(d.text)
   
    img_div4 = soup4.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div4:
        img_tag4 = img.find("img")
        img_src4 = img_tag4.get('src')
        Images4.append(img_src4)

    context = {
        'products': zip(Product_name, Prices, Description, Images,),
        'products1': zip(Product_name1, Prices1, Description1, Images1,),
        'products2': zip(Product_name2, Prices2, Description2, Images2,),
        'products4': zip(Product_name4, Prices4, Description4, Images4,),
    }
    
    return render(request, 'scraped_clothing.html', context)


def deleteList(request, wishlist_id):
        # Assuming you have a List model and each wishlist has a unique ID
        # Retrieve the wishlist object
        wishlist = get_object_or_404(List, wishlist_id=wishlist_id)
        print(wishlist_id)

        # Perform deletion logic here, for example:
        wishlist.delete()

        # Return a success response
        return redirect('/create/')
    #else:
        # Return a failure response if the request is not POST or not AJAX
        #return redirect('/create')


def scrape_flipkart1(request):
    if request.method=="POST":
        username = request.POST.get("username")
        print("US",username)
    print("test")
    Product_name = []
    Prices = []
    Description = []
    Images = []
    url = "https://www.flipkart.com/search?q=mobiles+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+str(1)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    names = soup.find_all("div", class_="KzDlHZ")
    for name in names:
        Product_name.append(name.text)

    # Scrape product prices
    prices = soup.find_all("div", class_="Nx9bqj _4b5DiR")
    for price in prices:
        Prices.append(price.text)
    desc = soup.find_all("ul", class_="G4BRas")
    for d in desc:
        description = d.text
        Description.append(description)
   
     # Scrape images
    img_items = soup.find_all("div", class_="_4WELSP")
    for img_item in img_items:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images.append(img_src)
    

    # Define Images1 for the second set of products
    Images1 = []
    Product_name1=[]
    Prices1=[]
    Description1 = []
    url1 = "https://www.flipkart.com/search?q=bedsheet&sid=jra%2Cknw%2Cqcw&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_9_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_9_na_na_na&as-pos=2&as-type=RECENT&suggestionId=bedsheet%7CBedsheets&requestId=04de54c5-e4a5-4e25-af98-1629d4706010&as-backfill=on&page=2"
    r = requests.get(url1)
    soup = BeautifulSoup(r.text, "html.parser")
     # Scrape product names
    names = soup.find_all("a", class_="wjcEIp")
    for name in names:
        Product_name1.append(name.text)
    # Scrape product prices
    prices = soup.find_all("div", class_="Nx9bqj")
    for price in prices:
        Prices1.append(price.text)

    # Scrape product descriptions
    desc = soup.find_all("div", class_="NqpwHC")
    for d in desc:
        Description1.append(d.text)

    # Scrape images
    img_items = soup.find_all("div", class_="_4WELSP WH5SS-")
    for img_item in img_items:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images1.append(img_src)
        
        
    
# #Home Decor 

    Product_name2 = []
    Prices2 = []
    Images2=[]
    Description2=[]
    url2 = "https://www.flipkart.com/search?q=home+decorate+items&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=5"
    r2 = requests.get(url2)
    soup2 = BeautifulSoup(r2.text, "lxml")
     # Scrape product names
    names2 = soup2.find_all("a", class_="wjcEIp")
    for name in names2:
        Product_name2.append(name.text)
        print("Home Decor",name.text,"\n")

    # Scrape product prices
    prices2 = soup2.find_all("div", class_="Nx9bqj")
    for price in prices2:
        Prices2.append(price.text)
    desc = soup.find_all("div", class_="NqpwHC")
    for d in desc:
        Description2.append(d.text)

    # Scrape images
    img_items2 = soup2.find_all("div", class_="_4WELSP WH5SS-")
    for img_item in img_items2:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images2.append(img_src)
        
   #Earphones        
    Product_name4 = []
    Prices4 = []
    Images4=[]
    Description4=[]
    url4 = "https://www.flipkart.com/search?q=earphone+with+power+bank&sid=0pm%2Cfcn%2C821%2Ca7x%2C2si&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&as-pos=2&as-type=RECENT&suggestionId=earphone+with+power+bank%7CTrue+Wireless&requestId=1c7ae1bd-ed21-4897-9fb6-ebadcee2fabf&as-searchtext=powerbank%20and%20earphones"
    r4 = requests.get(url4)
    soup4 = BeautifulSoup(r4.text, "lxml")
    names4 = soup.find_all("a", class_="wjcEIp")
    for name in names4:
        Product_name4.append(name.text)
        print("Earbuds",name.text,"\n")
    prices4 = soup4.find_all("div", class_="Nx9bqj")
    for price in prices4:
        Prices4.append(price.text)
    desc = soup.find_all("div", class_="UkUFwK")
    for d in desc:
        Description4.append(d.text)

    img_items4 = soup4.find_all("div", class_="_4WELSP")
    for img_item in img_items4:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images4.append(img_src)

    context = {
        'products': zip(Product_name, Prices, Description, Images),
        'products1': zip(Product_name1, Prices1,Description1, Images1),
        'products2': zip(Product_name2, Prices2,Description2, Images2),
        'products4': zip(Product_name4, Prices4,Description4, Images4),
    }
    
    return render(request, 'scraped_data1.html', context)
    


def scrape_clothing1(request):
    if request.method=="POST":
        username = request.POST.get("username")
        print("US",username)
    print("test")
    Product_name = []
    Prices = []
    Description = []
    Images = []
    url = "https://www.flipkart.com/search?q=tops+for+women&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=4"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    names = soup.find_all("div", class_="syl9yP")
    for name in names:
        Product_name.append(name.text)
    # Indian Rupee symbol
    prices = soup.find_all("div", class_="Nx9bqj")
    for price in prices:
        Prices.append(price.text)
    desc = soup.find_all("a", class_="WKTcLC")
    for d in desc:
        description = d.text
        Description.append(description)
   
    # The rest of your code for processing imagespage = urllib.request.urlopen(url)
    
    img_div = soup.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div:
        img_tag = img.find("img")
        img_src = img_tag.get('src')
        Images.append(img_src)
    

    # Define Images1 for the second set of products
    Images1 = []
    Product_name1=[]
    Prices1=[]
    Description1=[]
    url1 = "https://www.flipkart.com/search?q=men%20t%20shirt%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    r1 = requests.get(url1)
    soup1 = BeautifulSoup(r1.text, "html.parser")
    names1 = soup1.find_all("div", class_="syl9yP")
    for name in names1:
        Product_name1.append(name.text)
    # Indian Rupee symbol
    prices1 = soup1.find_all("div", class_="Nx9bqj")
    for price in prices1:
        Prices1.append(price.text)
    desc1 = soup1.find_all("a", class_="WKTcLC")
    for d in desc1:
        Description1.append(d.text)
    
    img_div1 = soup1.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div1:
        img_tag1 = img.find("img")
        img_src1 = img_tag1.get('src')
        Images1.append(img_src1)
        
        
    Product_name2 = []
    Prices2 = []
    Images2=[]
    Description2=[]
    url2 = "https://www.flipkart.com/search?q=boys+t+shirt+12%2F13+years&sid=clo%2Cash%2Cank%2Cpgi&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&as-pos=1&as-type=RECENT&suggestionId=boys+t+shirt+12%2F13+years%7CKids%27+T-shirts&requestId=4760a67d-8bf7-4c4e-adab-d9accf664d73&as-searchtext=boys%20t%20shirt%20"
    r2 = requests.get(url2)
    soup2 = BeautifulSoup(r2.text, "lxml")
    names2 = soup2.find_all("div", class_="syl9yP")
    for name in names2:
        Product_name2.append(name.text)
        print("Boys Clothing",name.text,"\n")
    # Indian Rupee symbol
    prices2 = soup2.find_all("div", class_="Nx9bqj")
    for price in prices2:
        Prices2.append(price.text)
    desc2 = soup2.find_all("a", class_="WKTcLC")
    for d in desc2:
        Description2.append(d.text)
        

    img_div2 = soup2.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div2:
        img_tag2 = img.find("img")
        img_src2 = img_tag2.get('src')
        Images2.append(img_src2)
        
    Product_name4 = []
    Prices4 = []
    Images4=[]
    Description4=[]
    url4 = "https://www.flipkart.com/search?q=girls%20dress%2011%2F12years%20frock%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    r4 = requests.get(url4)
    soup4 = BeautifulSoup(r4.text, "lxml")
    names4 = soup4.find_all("div", class_="syl9yP")
    for name in names4:
        Product_name4.append(name.text)
        # Indian Rupee symbol
    prices4 = soup4.find_all("div", class_="Nx9bqj")
    for price in prices4:
        Prices4.append(price.text)
    desc4 = soup4.find_all("a", class_="WKTcLC BwBZTg")
    for d in desc4:
        Description4.append(d.text)
   
    img_div4 = soup4.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div4:
        img_tag4 = img.find("img")
        img_src4 = img_tag4.get('src')
        Images4.append(img_src4)

    context = {
        'products': zip(Product_name, Prices, Description, Images,),
        'products1': zip(Product_name1, Prices1, Description1, Images1,),
        'products2': zip(Product_name2, Prices2, Description2, Images2,),
        'products4': zip(Product_name4, Prices4, Description4, Images4,),
    }
    
    return render(request, 'scraped_clothing1.html', context)


def scrape_flipkart2(request):
    if request.method=="POST":
        username = request.POST.get("username")
        print("US",username)
    print("test")
    Product_name = []
    Prices = []
    Description = []
    Images = []
    url = "https://www.flipkart.com/search?q=mobiles+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+str(1)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    names = soup.find_all("div", class_="KzDlHZ")
    for name in names:
        Product_name.append(name.text)

    # Scrape product prices
    prices = soup.find_all("div", class_="Nx9bqj _4b5DiR")
    for price in prices:
        Prices.append(price.text)
    desc = soup.find_all("ul", class_="G4BRas")
    for d in desc:
        description = d.text
        Description.append(description)
   
     # Scrape images
    img_items = soup.find_all("div", class_="_4WELSP")
    for img_item in img_items:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images.append(img_src)
    

    # Define Images1 for the second set of products
    Images1 = []
    Product_name1=[]
    Prices1=[]
    Description1 = []
    url1 = "https://www.flipkart.com/search?q=bedsheet&sid=jra%2Cknw%2Cqcw&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_9_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_9_na_na_na&as-pos=2&as-type=RECENT&suggestionId=bedsheet%7CBedsheets&requestId=04de54c5-e4a5-4e25-af98-1629d4706010&as-backfill=on&page=2"
    r = requests.get(url1)
    soup = BeautifulSoup(r.text, "html.parser")
     # Scrape product names
    names = soup.find_all("a", class_="wjcEIp")
    for name in names:
        Product_name1.append(name.text)
    # Scrape product prices
    prices = soup.find_all("div", class_="Nx9bqj")
    for price in prices:
        Prices1.append(price.text)

    # Scrape product descriptions
    desc = soup.find_all("div", class_="NqpwHC")
    for d in desc:
        Description1.append(d.text)

    # Scrape images
    img_items = soup.find_all("div", class_="_4WELSP WH5SS-")
    for img_item in img_items:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images1.append(img_src)
        
        
    
# #Home Decor 

    Product_name2 = []
    Prices2 = []
    Images2=[]
    Description2=[]
    url2 = "https://www.flipkart.com/search?q=home+decorate+items&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=5"
    r2 = requests.get(url2)
    soup2 = BeautifulSoup(r2.text, "lxml")
     # Scrape product names
    names2 = soup2.find_all("a", class_="wjcEIp")
    for name in names2:
        Product_name2.append(name.text)
        print("Home Decor",name.text,"\n")

    # Scrape product prices
    prices2 = soup2.find_all("div", class_="Nx9bqj")
    for price in prices2:
        Prices2.append(price.text)
    desc = soup.find_all("div", class_="NqpwHC")
    for d in desc:
        Description2.append(d.text)

    # Scrape images
    img_items2 = soup2.find_all("div", class_="_4WELSP WH5SS-")
    for img_item in img_items2:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images2.append(img_src)
        
   #Earphones        
    Product_name4 = []
    Prices4 = []
    Images4=[]
    Description4=[]
    url4 = "https://www.flipkart.com/search?q=earphone+with+power+bank&sid=0pm%2Cfcn%2C821%2Ca7x%2C2si&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&as-pos=2&as-type=RECENT&suggestionId=earphone+with+power+bank%7CTrue+Wireless&requestId=1c7ae1bd-ed21-4897-9fb6-ebadcee2fabf&as-searchtext=powerbank%20and%20earphones"
    r4 = requests.get(url4)
    soup4 = BeautifulSoup(r4.text, "lxml")
    names4 = soup.find_all("a", class_="wjcEIp")
    for name in names4:
        Product_name4.append(name.text)
        print("Earbuds",name.text,"\n")
    prices4 = soup4.find_all("div", class_="Nx9bqj")
    for price in prices4:
        Prices4.append(price.text)
    desc = soup.find_all("div", class_="UkUFwK")
    for d in desc:
        Description4.append(d.text)

    img_items4 = soup4.find_all("div", class_="_4WELSP")
    for img_item in img_items4:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images4.append(img_src)

    context = {
        'products': zip(Product_name, Prices, Description, Images),
        'products1': zip(Product_name1, Prices1,Description1, Images1),
        'products2': zip(Product_name2, Prices2,Description2, Images2),
        'products4': zip(Product_name4, Prices4,Description1, Images4),
    }
    
    return render(request, 'scraped_data2.html', context)
    


def scrape_clothing2(request):
    if request.method=="POST":
        username = request.POST.get("username")
        print("US",username)
    print("test")
    Product_name = []
    Prices = []
    Description = []
    Images = []
    url = "https://www.flipkart.com/search?q=tops+for+women&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=4"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    names = soup.find_all("div", class_="syl9yP")
    for name in names:
        Product_name.append(name.text)
    # Indian Rupee symbol
    prices = soup.find_all("div", class_="Nx9bqj")
    for price in prices:
        Prices.append(price.text)
    desc = soup.find_all("a", class_="WKTcLC")
    for d in desc:
        description = d.text
        Description.append(description)
   
    # The rest of your code for processing imagespage = urllib.request.urlopen(url)
    
    img_div = soup.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div:
        img_tag = img.find("img")
        img_src = img_tag.get('src')
        Images.append(img_src)
    

    # Define Images1 for the second set of products
    Images1 = []
    Product_name1=[]
    Prices1=[]
    Description1=[]
    url1 = "https://www.flipkart.com/search?q=men%20t%20shirt%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    r1 = requests.get(url1)
    soup1 = BeautifulSoup(r1.text, "html.parser")
    names1 = soup1.find_all("div", class_="syl9yP")
    for name in names1:
        Product_name1.append(name.text)
    # Indian Rupee symbol
    prices1 = soup1.find_all("div", class_="Nx9bqj")
    for price in prices1:
        Prices1.append(price.text)
    desc1 = soup1.find_all("a", class_="WKTcLC")
    for d in desc1:
        Description1.append(d.text)
    
    img_div1 = soup1.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div1:
        img_tag1 = img.find("img")
        img_src1 = img_tag1.get('src')
        Images1.append(img_src1)
        
        
    Product_name2 = []
    Prices2 = []
    Images2=[]
    Description2=[]
    url2 = "https://www.flipkart.com/search?q=boys+t+shirt+12%2F13+years&sid=clo%2Cash%2Cank%2Cpgi&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&as-pos=1&as-type=RECENT&suggestionId=boys+t+shirt+12%2F13+years%7CKids%27+T-shirts&requestId=4760a67d-8bf7-4c4e-adab-d9accf664d73&as-searchtext=boys%20t%20shirt%20"
    r2 = requests.get(url2)
    soup2 = BeautifulSoup(r2.text, "lxml")
    names2 = soup2.find_all("div", class_="syl9yP")
    for name in names2:
        Product_name2.append(name.text)
        print("Boys Clothing",name.text,"\n")
    # Indian Rupee symbol
    prices2 = soup2.find_all("div", class_="Nx9bqj")
    for price in prices2:
        Prices2.append(price.text)
    desc2 = soup2.find_all("a", class_="WKTcLC")
    for d in desc2:
        Description2.append(d.text)
        

    img_div2 = soup2.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div2:
        img_tag2 = img.find("img")
        img_src2 = img_tag2.get('src')
        Images2.append(img_src2)
        
    Product_name4 = []
    Prices4 = []
    Images4=[]
    Description4=[]
    url4 = "https://www.flipkart.com/search?q=girls%20dress%2011%2F12years%20frock%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    r4 = requests.get(url4)
    soup4 = BeautifulSoup(r4.text, "lxml")
    names4 = soup4.find_all("div", class_="syl9yP")
    for name in names4:
        Product_name4.append(name.text)
        # Indian Rupee symbol
    prices4 = soup4.find_all("div", class_="Nx9bqj")
    for price in prices4:
        Prices4.append(price.text)
    desc4 = soup4.find_all("a", class_="WKTcLC BwBZTg")
    for d in desc4:
        Description4.append(d.text)
   
    img_div4 = soup4.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div4:
        img_tag4 = img.find("img")
        img_src4 = img_tag4.get('src')
        Images4.append(img_src4)

    context = {
        'products': zip(Product_name, Prices, Description, Images,),
        'products1': zip(Product_name1, Prices1, Description1, Images1,),
        'products2': zip(Product_name2, Prices2, Description2, Images2,),
        'products4': zip(Product_name4, Prices4, Description4, Images4,),
    }
    
    return render(request, 'scraped_clothing2.html', context)



def scrape_flipkart3(request):
    if request.method=="POST":
        username = request.POST.get("username")
        print("US",username)
    print("test")
    Product_name = []
    Prices = []
    Description = []
    Images = []
    url = "https://www.flipkart.com/search?q=mobiles+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+str(1)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    names = soup.find_all("div", class_="KzDlHZ")
    for name in names:
        Product_name.append(name.text)

    # Scrape product prices
    prices = soup.find_all("div", class_="Nx9bqj _4b5DiR")
    for price in prices:
        Prices.append(price.text)
    desc = soup.find_all("ul", class_="G4BRas")
    for d in desc:
        description = d.text
        Description.append(description)
   
     # Scrape images
    img_items = soup.find_all("div", class_="_4WELSP")
    for img_item in img_items:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images.append(img_src)
    

    # Define Images1 for the second set of products
    Images1 = []
    Product_name1=[]
    Prices1=[]
    Description1 = []
    url1 = "https://www.flipkart.com/search?q=bedsheet&sid=jra%2Cknw%2Cqcw&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_9_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_9_na_na_na&as-pos=2&as-type=RECENT&suggestionId=bedsheet%7CBedsheets&requestId=04de54c5-e4a5-4e25-af98-1629d4706010&as-backfill=on&page=2"
    r = requests.get(url1)
    soup = BeautifulSoup(r.text, "html.parser")
     # Scrape product names
    names = soup.find_all("a", class_="wjcEIp")
    for name in names:
        Product_name1.append(name.text)
    # Scrape product prices
    prices = soup.find_all("div", class_="Nx9bqj")
    for price in prices:
        Prices1.append(price.text)

    # Scrape product descriptions
    desc = soup.find_all("div", class_="NqpwHC")
    for d in desc:
        Description1.append(d.text)

    # Scrape images
    img_items = soup.find_all("div", class_="_4WELSP WH5SS-")
    for img_item in img_items:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images1.append(img_src)
        
        
    
# #Home Decor 

    Product_name2 = []
    Prices2 = []
    Images2=[]
    Description2=[]
    url2 = "https://www.flipkart.com/search?q=home+decorate+items&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=5"
    r2 = requests.get(url2)
    soup2 = BeautifulSoup(r2.text, "lxml")
     # Scrape product names
    names2 = soup2.find_all("a", class_="wjcEIp")
    for name in names2:
        Product_name2.append(name.text)
        print("Home Decor",name.text,"\n")

    # Scrape product prices
    prices2 = soup2.find_all("div", class_="Nx9bqj")
    for price in prices2:
        Prices2.append(price.text)
    desc = soup.find_all("div", class_="NqpwHC")
    for d in desc:
        Description2.append(d.text)

    # Scrape images
    img_items2 = soup2.find_all("div", class_="_4WELSP WH5SS-")
    for img_item in img_items2:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images2.append(img_src)
        
   #Earphones        
    Product_name4 = []
    Prices4 = []
    Images4=[]
    Description4=[]
    url4 = "https://www.flipkart.com/search?q=earphone+with+power+bank&sid=0pm%2Cfcn%2C821%2Ca7x%2C2si&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&as-pos=2&as-type=RECENT&suggestionId=earphone+with+power+bank%7CTrue+Wireless&requestId=1c7ae1bd-ed21-4897-9fb6-ebadcee2fabf&as-searchtext=powerbank%20and%20earphones"
    r4 = requests.get(url4)
    soup4 = BeautifulSoup(r4.text, "lxml")
    names4 = soup.find_all("a", class_="wjcEIp")
    for name in names4:
        Product_name4.append(name.text)
        print("Earbuds",name.text,"\n")
    prices4 = soup4.find_all("div", class_="Nx9bqj")
    for price in prices4:
        Prices4.append(price.text)
    desc = soup.find_all("div", class_="UkUFwK")
    for d in desc:
        Description4.append(d.text)

    img_items4 = soup4.find_all("div", class_="_4WELSP")
    for img_item in img_items4:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images4.append(img_src)

    context = {
        'products': zip(Product_name, Prices, Description, Images),
        'products1': zip(Product_name1, Prices1,Description1, Images1),
        'products2': zip(Product_name2, Prices2, Description2, Images2),
        'products4': zip(Product_name4, Prices4,Description4, Images4),
    }
    
    return render(request, 'scraped_data3.html', context)
    


def scrape_clothing3(request):
    if request.method=="POST":
        username = request.POST.get("username")
        print("US",username)
    print("test")
    Product_name = []
    Prices = []
    Description = []
    Images = []
    url = "https://www.flipkart.com/search?q=tops+for+women&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=4"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    names = soup.find_all("div", class_="syl9yP")
    for name in names:
        Product_name.append(name.text)
    # Indian Rupee symbol
    prices = soup.find_all("div", class_="Nx9bqj")
    for price in prices:
        Prices.append(price.text)
    desc = soup.find_all("a", class_="WKTcLC")
    for d in desc:
        description = d.text
        Description.append(description)
   
    # The rest of your code for processing imagespage = urllib.request.urlopen(url)
    
    img_div = soup.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div:
        img_tag = img.find("img")
        img_src = img_tag.get('src')
        Images.append(img_src)
    

    # Define Images1 for the second set of products
    Images1 = []
    Product_name1=[]
    Prices1=[]
    Description1=[]
    url1 = "https://www.flipkart.com/search?q=men%20t%20shirt%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    r1 = requests.get(url1)
    soup1 = BeautifulSoup(r1.text, "html.parser")
    names1 = soup1.find_all("div", class_="syl9yP")
    for name in names1:
        Product_name1.append(name.text)
    # Indian Rupee symbol
    prices1 = soup1.find_all("div", class_="Nx9bqj")
    for price in prices1:
        Prices1.append(price.text)
    desc1 = soup1.find_all("a", class_="WKTcLC")
    for d in desc1:
        Description1.append(d.text)
    
    img_div1 = soup1.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div1:
        img_tag1 = img.find("img")
        img_src1 = img_tag1.get('src')
        Images1.append(img_src1)
        
        
    Product_name2 = []
    Prices2 = []
    Images2=[]
    Description2=[]
    url2 = "https://www.flipkart.com/search?q=boys+t+shirt+12%2F13+years&sid=clo%2Cash%2Cank%2Cpgi&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&as-pos=1&as-type=RECENT&suggestionId=boys+t+shirt+12%2F13+years%7CKids%27+T-shirts&requestId=4760a67d-8bf7-4c4e-adab-d9accf664d73&as-searchtext=boys%20t%20shirt%20"
    r2 = requests.get(url2)
    soup2 = BeautifulSoup(r2.text, "lxml")
    names2 = soup2.find_all("div", class_="syl9yP")
    for name in names2:
        Product_name2.append(name.text)
        print("Boys Clothing",name.text,"\n")
    # Indian Rupee symbol
    prices2 = soup2.find_all("div", class_="Nx9bqj")
    for price in prices2:
        Prices2.append(price.text)
    desc2 = soup2.find_all("a", class_="WKTcLC")
    for d in desc2:
        Description2.append(d.text)
        

    img_div2 = soup2.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div2:
        img_tag2 = img.find("img")
        img_src2 = img_tag2.get('src')
        Images2.append(img_src2)
        
    Product_name4 = []
    Prices4 = []
    Images4=[]
    Description4=[]
    url4 = "https://www.flipkart.com/search?q=girls%20dress%2011%2F12years%20frock%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    r4 = requests.get(url4)
    soup4 = BeautifulSoup(r4.text, "lxml")
    names4 = soup4.find_all("div", class_="syl9yP")
    for name in names4:
        Product_name4.append(name.text)
        # Indian Rupee symbol
    prices4 = soup4.find_all("div", class_="Nx9bqj")
    for price in prices4:
        Prices4.append(price.text)
    desc4 = soup4.find_all("a", class_="WKTcLC BwBZTg")
    for d in desc4:
        Description4.append(d.text)
   
    img_div4 = soup4.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div4:
        img_tag4 = img.find("img")
        img_src4 = img_tag4.get('src')
        Images4.append(img_src4)

    context = {
        'products': zip(Product_name, Prices, Description, Images,),
        'products1': zip(Product_name1, Prices1, Description1, Images1,),
        'products2': zip(Product_name2, Prices2, Description2, Images2,),
        'products4': zip(Product_name4, Prices4, Description4, Images4,),
    }
    
    return render(request, 'scraped_clothing3.html', context)


def scrape_flipkart4(request):
    if request.method=="POST":
        username = request.POST.get("username")
        print("US",username)
    print("test")
    Product_name = []
    Prices = []
    Description = []
    Images = []
    url = "https://www.flipkart.com/search?q=mobiles+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+str(1)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    names = soup.find_all("div", class_="KzDlHZ")
    for name in names:
        Product_name.append(name.text)

    # Scrape product prices
    prices = soup.find_all("div", class_="Nx9bqj _4b5DiR")
    for price in prices:
        Prices.append(price.text)
    desc = soup.find_all("ul", class_="G4BRas")
    for d in desc:
        description = d.text
        Description.append(description)
   
     # Scrape images
    img_items = soup.find_all("div", class_="_4WELSP")
    for img_item in img_items:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images.append(img_src)
    

    # Define Images1 for the second set of products
    Images1 = []
    Product_name1=[]
    Prices1=[]
    Description1 = []
    url1 = "https://www.flipkart.com/search?q=bedsheet&sid=jra%2Cknw%2Cqcw&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_9_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_9_na_na_na&as-pos=2&as-type=RECENT&suggestionId=bedsheet%7CBedsheets&requestId=04de54c5-e4a5-4e25-af98-1629d4706010&as-backfill=on&page=2"
    r = requests.get(url1)
    soup = BeautifulSoup(r.text, "html.parser")
     # Scrape product names
    names = soup.find_all("a", class_="wjcEIp")
    for name in names:
        Product_name1.append(name.text)
    # Scrape product prices
    prices = soup.find_all("div", class_="Nx9bqj")
    for price in prices:
        Prices1.append(price.text)

    # Scrape product descriptions
    desc = soup.find_all("div", class_="NqpwHC")
    for d in desc:
        Description1.append(d.text)

    # Scrape images
    img_items = soup.find_all("div", class_="_4WELSP WH5SS-")
    for img_item in img_items:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images1.append(img_src)
        
        
    
# #Home Decor 

    Product_name2 = []
    Prices2 = []
    Images2=[]
    Description2=[]
    url2 = "https://www.flipkart.com/search?q=home+decorate+items&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=5"
    r2 = requests.get(url2)
    soup2 = BeautifulSoup(r2.text, "lxml")
     # Scrape product names
    names2 = soup2.find_all("a", class_="wjcEIp")
    for name in names2:
        Product_name2.append(name.text)
        print("Home Decor",name.text,"\n")

    # Scrape product prices
    prices2 = soup2.find_all("div", class_="Nx9bqj")
    for price in prices2:
        Prices2.append(price.text)
    desc = soup.find_all("div", class_="NqpwHC")
    for d in desc:
        Description2.append(d.text)

    # Scrape images
    img_items2 = soup2.find_all("div", class_="_4WELSP WH5SS-")
    for img_item in img_items2:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images2.append(img_src)
        
   #Earphones        
    Product_name4 = []
    Prices4 = []
    Images4=[]
    Description4=[]
    url4 = "https://www.flipkart.com/search?q=earphone+with+power+bank&sid=0pm%2Cfcn%2C821%2Ca7x%2C2si&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&as-pos=2&as-type=RECENT&suggestionId=earphone+with+power+bank%7CTrue+Wireless&requestId=1c7ae1bd-ed21-4897-9fb6-ebadcee2fabf&as-searchtext=powerbank%20and%20earphones"
    r4 = requests.get(url4)
    soup4 = BeautifulSoup(r4.text, "lxml")
    names4 = soup.find_all("a", class_="wjcEIp")
    for name in names4:
        Product_name4.append(name.text)
        print("Earbuds",name.text,"\n")
    prices4 = soup4.find_all("div", class_="Nx9bqj")
    for price in prices4:
        Prices4.append(price.text)
    desc = soup.find_all("div", class_="UkUFwK")
    for d in desc:
        Description4.append(d.text)

    img_items4 = soup4.find_all("div", class_="_4WELSP")
    for img_item in img_items4:
        img_tag = img_item.find("img")
        img_src = img_tag.get('src')
        Images4.append(img_src)

    context = {
        'products': zip(Product_name, Prices, Description, Images),
        'products1': zip(Product_name1, Prices1,Description1, Images1),
        'products2': zip(Product_name2, Prices2, Description2, Images2),
        'products4': zip(Product_name4, Prices4, Description4, Images4),
    }
    
    return render(request, 'scraped_data4.html', context)
    


def scrape_clothing4(request):
    if request.method=="POST":
        username = request.POST.get("username")
        print("US",username)
    print("test")
    Product_name = []
    Prices = []
    Description = []
    Images = []
    url = "https://www.flipkart.com/search?q=tops+for+women&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=4"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    names = soup.find_all("div", class_="syl9yP")
    for name in names:
        Product_name.append(name.text)
    # Indian Rupee symbol
    prices = soup.find_all("div", class_="Nx9bqj")
    for price in prices:
        Prices.append(price.text)
    desc = soup.find_all("a", class_="WKTcLC")
    for d in desc:
        description = d.text
        Description.append(description)
   
    # The rest of your code for processing imagespage = urllib.request.urlopen(url)
    
    img_div = soup.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div:
        img_tag = img.find("img")
        img_src = img_tag.get('src')
        Images.append(img_src)
    

    # Define Images1 for the second set of products
    Images1 = []
    Product_name1=[]
    Prices1=[]
    Description1=[]
    url1 = "https://www.flipkart.com/search?q=men%20t%20shirt%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    r1 = requests.get(url1)
    soup1 = BeautifulSoup(r1.text, "html.parser")
    names1 = soup1.find_all("div", class_="syl9yP")
    for name in names1:
        Product_name1.append(name.text)
    # Indian Rupee symbol
    prices1 = soup1.find_all("div", class_="Nx9bqj")
    for price in prices1:
        Prices1.append(price.text)
    desc1 = soup1.find_all("a", class_="WKTcLC")
    for d in desc1:
        Description1.append(d.text)
    
    img_div1 = soup1.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div1:
        img_tag1 = img.find("img")
        img_src1 = img_tag1.get('src')
        Images1.append(img_src1)
        
        
    Product_name2 = []
    Prices2 = []
    Images2=[]
    Description2=[]
    url2 = "https://www.flipkart.com/search?q=boys+t+shirt+12%2F13+years&sid=clo%2Cash%2Cank%2Cpgi&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&as-pos=1&as-type=RECENT&suggestionId=boys+t+shirt+12%2F13+years%7CKids%27+T-shirts&requestId=4760a67d-8bf7-4c4e-adab-d9accf664d73&as-searchtext=boys%20t%20shirt%20"
    r2 = requests.get(url2)
    soup2 = BeautifulSoup(r2.text, "lxml")
    names2 = soup2.find_all("div", class_="syl9yP")
    for name in names2:
        Product_name2.append(name.text)
        print("Boys Clothing",name.text,"\n")
    # Indian Rupee symbol
    prices2 = soup2.find_all("div", class_="Nx9bqj")
    for price in prices2:
        Prices2.append(price.text)
    desc2 = soup2.find_all("a", class_="WKTcLC")
    for d in desc2:
        Description2.append(d.text)
        

    img_div2 = soup2.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div2:
        img_tag2 = img.find("img")
        img_src2 = img_tag2.get('src')
        Images2.append(img_src2)
        
    Product_name4 = []
    Prices4 = []
    Images4=[]
    Description4=[]
    url4 = "https://www.flipkart.com/search?q=girls%20dress%2011%2F12years%20frock%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    r4 = requests.get(url4)
    soup4 = BeautifulSoup(r4.text, "lxml")
    names4 = soup4.find_all("div", class_="syl9yP")
    for name in names4:
        Product_name4.append(name.text)
        # Indian Rupee symbol
    prices4 = soup4.find_all("div", class_="Nx9bqj")
    for price in prices4:
        Prices4.append(price.text)
    desc4 = soup4.find_all("a", class_="WKTcLC BwBZTg")
    for d in desc4:
        Description4.append(d.text)
   
    img_div4 = soup4.find_all(class_="gqcSqV YGE0gZ")
    for img in img_div4:
        img_tag4 = img.find("img")
        img_src4 = img_tag4.get('src')
        Images4.append(img_src4)

    context = {
        'products': zip(Product_name, Prices, Description, Images,),
        'products1': zip(Product_name1, Prices1, Description1, Images1,),
        'products2': zip(Product_name2, Prices2, Description2, Images2,),
        'products4': zip(Product_name4, Prices4, Description4, Images4,),
    }
    
    return render(request, 'scraped_clothing4.html', context)

def addtocartb(request,product,price,image):
    product = unquote(product)
    price = unquote(price)
    image = unquote(image)
    
    product = str(product)
    price = str(price)
    image = str(image)
    
    a=str(request.user)
    print(a)
    user_ref = db.collection('user').document(a)
    wishlist_ref = user_ref.collection('wishlist').document('birthday')
    product_ref = wishlist_ref.collection('products').document()

    data={"product_name": product,"price":price,"image":image,"status":"not bought"}

    product_ref.set(data)
    print(image)
    return redirect('/scrape/')

def addtocartb(request,product,price,image):
    product = unquote(product)
    price = unquote(price)
    image = unquote(image)
    
    product = str(product)
    price = str(price)
    image = str(image)
    
    a=str(request.user)
    print(a)
    user_ref = db.collection('user').document(a)
    wishlist_ref = user_ref.collection('wishlist').document('birthday')
    product_ref = wishlist_ref.collection('products').document()

    data={"product_name": product,"price":price,"image":image,"status":"not bought"}

    product_ref.set(data)
    print(image)
    return redirect('/scrape_clothing/')


def addtocarth(request,product,price,image):
    product = unquote(product)
    price = unquote(price)
    image = unquote(image)
    
    product = str(product)
    price = str(price)
    image = str(image)
    
    a=str(request.user)
    print(a)
    user_ref = db.collection('user').document(a)
    wishlist_ref = user_ref.collection('wishlist').document('house_warming')
    product_ref = wishlist_ref.collection('products').document()

    data={"product_name": product,"price":price,"image":image,"status":"not bought"}

    product_ref.set(data)
    print(image)
    return redirect('/scrape1/')

def addtocarth(request,product,price,image):
    product = unquote(product)
    price = unquote(price)
    image = unquote(image)
    
    product = str(product)
    price = str(price)
    image = str(image)
    
    a=str(request.user)
    print(a)
    user_ref = db.collection('user').document(a)
    wishlist_ref = user_ref.collection('wishlist').document('house_warming')
    product_ref = wishlist_ref.collection('products').document()

    data={"product_name": product,"price":price,"image":image,"status":"not bought"}

    product_ref.set(data)
    print(image)
    return redirect('/scrape_clothing1/')


def addtocartw(request,product,price,image):
    product = unquote(product)
    price = unquote(price)
    image = unquote(image)
    
    product = str(product)
    price = str(price)
    image = str(image)
    
    a=str(request.user)
    print(a)
    user_ref = db.collection('user').document(a)
    wishlist_ref = user_ref.collection('wishlist').document('wedding')
    product_ref = wishlist_ref.collection('products').document()

    data={"product_name": product,"price":price,"image":image,"status":"not bought"}

    product_ref.set(data)
    print(image)
    return redirect('/scrape2/')

def addtocartw(request,product,price,image):
    product = unquote(product)
    price = unquote(price)
    image = unquote(image)
    
    product = str(product)
    price = str(price)
    image = str(image)
    
    a=str(request.user)
    print(a)
    user_ref = db.collection('user').document(a)
    wishlist_ref = user_ref.collection('wishlist').document('wedding')
    product_ref = wishlist_ref.collection('products').document()

    data={"product_name": product,"price":price,"image":image,"status":"not bought"}

    product_ref.set(data)
    print(image)
    return redirect('/scrape_clothing2/')

def addtocartbm(request,product,price,image):
    product = unquote(product)
    price = unquote(price)
    image = unquote(image)
    
    product = str(product)
    price = str(price)
    image = str(image)
    
    a=str(request.user)
    print(a)
    user_ref = db.collection('user').document(a)
    wishlist_ref = user_ref.collection('wishlist').document('baptism')
    product_ref = wishlist_ref.collection('products').document()

    data={"product_name": product,"price":price,"image":image,"status":"not bought"}

    product_ref.set(data)
    print(image)
    return redirect('/scrape3/')

def addtocartbm(request,product,price,image):
    product = unquote(product)
    price = unquote(price)
    image = unquote(image)
    
    product = str(product)
    price = str(price)
    image = str(image)
    
    a=str(request.user)
    print(a)
    user_ref = db.collection('user').document(a)
    wishlist_ref = user_ref.collection('wishlist').document('baptism')
    product_ref = wishlist_ref.collection('products').document()

    data={"product_name": product,"price":price,"image":image,"status":"not bought"}

    product_ref.set(data)
    print(image)
    return redirect('/scrape_clothing3/')

def addtocartan(request,product,price,image):
    product = unquote(product)
    price = unquote(price)
    image = unquote(image)
    
    product = str(product)
    price = str(price)
    image = str(image)
    
    a=str(request.user)
    print(a)
    user_ref = db.collection('user').document(a)
    wishlist_ref = user_ref.collection('wishlist').document('anniversary')
    product_ref = wishlist_ref.collection('products').document()

    data={"product_name": product,"price":price,"image":image,"status":"not bought"}

    product_ref.set(data)
    print(image)
    return redirect('/scrape4/')

def addtocartan(request,product,price,image):
    product = unquote(product)
    price = unquote(price)
    image = unquote(image)
    
    product = str(product)
    price = str(price)
    image = str(image)
    
    a=str(request.user)
    print(a)
    user_ref = db.collection('user').document(a)
    wishlist_ref = user_ref.collection('wishlist').document('anniversary')
    product_ref = wishlist_ref.collection('products').document()

    data={"product_name": product,"price":price,"image":image,"status":"not bought"}

    product_ref.set(data)
    print(image)
    return redirect('/scrape_clothing4/')
