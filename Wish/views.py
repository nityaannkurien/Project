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
        items = List.objects.all()
        variable = {'name': username.first_name, 'listname' : items}
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
# Mobile Phones
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

    # Scrape product names
    names = soup.find_all("div", class_="KzDlHZ")
    for name in names:
        Product_name.append(name.text)

    # Scrape product prices
    prices = soup.find_all("div", class_="Nx9bqj _4b5DiR")
    for price in prices:
        Prices.append(price.text)

    # Scrape product descriptions
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

#Bedsheets
    Product_name1 = []
    Prices1 = []
    Description1 = []
    Images1 = []

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
    url4 = "https://www.flipkart.com/search?q=earphone+with+power+bank&sid=0pm%2Cfcn%2C821%2Ca7x%2C2si&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&as-pos=2&as-type=RECENT&suggestionId=earphone+with+power+bank%7CTrue+Wireless&requestId=1c7ae1bd-ed21-4897-9fb6-ebadcee2fabf&as-searchtext=powerbank%20and%20earphones"
    r4 = requests.get(url4)
    soup4 = BeautifulSoup(r4.text, "lxml")
     # Scrape product names
    names4 = soup.find_all("a", class_="wjcEIp")
    # for name in names4:
    #     Product_name4.append(name.text)

    # # Scrape product prices
    # prices4 = soup.find_all("div", class_="Nx9bqj")
    # for price in prices4:
    #     Prices4.append(price.text)


    # # Scrape images
    # img_items4 = soup.find_all("div", class_="_4WELSP WH5SS-")
    # for img_item in img_items4:
    #     img_tag = img_item.find("img")
    #     img_src = img_tag.get('src')
    #     Images4.append(img_src)


    # Product_name4 = []
    # Prices4 = []
    # Images4=[]
    # url4 = "https://www.flipkart.com/search?q=earphone+with+power+bank&sid=0pm%2Cfcn%2C821%2Ca7x%2C2si&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&as-pos=2&as-type=RECENT&suggestionId=earphone+with+power+bank%7CTrue+Wireless&requestId=1c7ae1bd-ed21-4897-9fb6-ebadcee2fabf&as-searchtext=powerbank%20and%20earphones"
    # r4 = requests.get(url4)
    # soup4 = BeautifulSoup(r4.text, "lxml")
    # names4 = soup4.find_all("a", class_="wjcEIp")
    for i in names4:
        name4 = i.text
        Product_name4.append(name4)
        # Indian Rupee symbol
    prices4 = soup4.find_all("div", class_="Nx9bqj")
    for i in prices4:
         price4 = i.text  # Add the Indian Rupee symbol to each price
         Prices4.append(price4)

    print(Product_name4)
    print(Prices4)

        # The rest of your code for processing images
    url4 = "https://www.flipkart.com/search?q=earphone+with+power+bank&sid=0pm%2Cfcn%2C821%2Ca7x%2C2si&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_23_sc_na_na&as-pos=2&as-type=RECENT&suggestionId=earphone+with+power+bank%7CTrue+Wireless&requestId=1c7ae1bd-ed21-4897-9fb6-ebadcee2fabf&as-searchtext=powerbank%20and%20earphones"
    page4 = urllib.request.urlopen(url4)
    page_soup4 = BeautifulSoup(page4, "html.parser")
    img_items4 = page_soup4.find("div", {"class": "DOjaWF YJG4Cf"})
    img_div4 = img_items4.find_all(class_="_4WELSP")
    i=0
    for img in img_div4:
        img_tag4 = img.find("img")
        img_src4 = img_tag4.get('src')
        if img_src4[:1] == '/':
            image4 = 'https:' + img_src4
        else:
            image4 = img_src4
            print(image4)
            file_name4=str(i)
            i+=1
            img_file4=open(file_name4 + '.jpeg' , 'wb' )
            img_file4.write(urllib.request.urlopen(image4).read())
            img_file4.close()
            Images4.append(image4)

    context = {
        'products': zip(Product_name, Prices, Description, Images),
        'products1': zip(Product_name1, Prices1,Description1, Images1),
        'products2': zip(Product_name2, Prices2, Images2),
        'products4': zip(Product_name4, Prices4, Images4),
    }
    print("Context",Product_name2)
    
    return render(request, 'scraped_data.html', context)


def scrape_flipkart1(request):
    Product_name = []
    Prices = []
    Description = []
    Images = []
    url = "https://www.flipkart.com/search?q=tops+for+women&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=4"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    names = soup.find_all("div", class_="syl9yP")
    for i in names:
        name = i.text
        Product_name.append(name)
    # Indian Rupee symbol
    prices = soup.find_all("div", class_="Nx9bqj")
    for i in prices:
        price = i.text  # Add the Indian Rupee symbol to each price
        Prices.append(price)
    desc = soup.find_all("a", class_="WKTcLC")
    for i in desc:
        description = i.text
        Description.append(description)
    # print(Product_name)
    # print(Prices)
    # print(Description)
    # The rest of your code for processing images
    url = "https://www.flipkart.com/search?q=tops+for+women&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=4"
    page = urllib.request.urlopen(url)
    page_soup = BeautifulSoup(page, "html.parser")
    img_items = page_soup.find("div", {"class": "DOjaWF YJG4Cf"})
    img_div = img_items.find_all(class_="gqcSqV YGE0gZ")
    i=0
    for img in img_div:
        img_tag = img.find("img")
        img_src = img_tag.get('src')
        if img_src[:1] == '/':
            image = 'https:' + img_src
        else:
            image = img_src
        print(image)
        file_name=str(i)
        i+=1
        img_file=open(file_name + '.jpeg' , 'wb' )
        img_file.write(urllib.request.urlopen(image).read())
        img_file.close()
        Images.append(image)
    

    # Define Images1 for the second set of products
    Images1 = []
    Product_name1=[]
    Prices1=[]
    Description1=[]
    url1 = "https://www.flipkart.com/search?q=men%20t%20shirt%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    r1 = requests.get(url1)
    soup1 = BeautifulSoup(r1.text, "lxml")
    names1 = soup1.find_all("div", class_="syl9yP")
    for i in names1:
        name1 = i.text
        Product_name1.append(name1)
    # Indian Rupee symbol
    prices1 = soup1.find_all("div", class_="Nx9bqj")
    for i in prices1:
        price1 = i.text  # Add the Indian Rupee symbol to each price
        Prices1.append(price1)
    desc1 = soup1.find_all("a", class_="WKTcLC")
    for i in desc1:
        description1 = i.text
        Description1.append(description1)
    print(Product_name1)
    print(Prices1)
    print(Description1)

    url1 = "https://www.flipkart.com/search?q=men%20t%20shirt%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    page1 = urllib.request.urlopen(url1)
    page_soup1 = BeautifulSoup(page1, "html.parser")
    img_items1 = page_soup1.find("div", {"class": "DOjaWF YJG4Cf"})
    img_div1 = img_items1.find_all(class_="gqcSqV YGE0gZ")
    i=0
    for img in img_div1:
        img_tag1 = img.find("img")
        img_src1 = img_tag1.get('src')
        if img_src1[:1] == '/':
            image1 = 'https:' + img_src1
        else:
            image1 = img_src1
        print(image1)
        file_name1=str(i)
        i+=1
        img_file1=open(file_name1 + '.jpeg' , 'wb' )
        img_file1.write(urllib.request.urlopen(image1).read())
        img_file1.close()
        Images1.append(image1)
        
        
    Product_name2 = []
    Prices2 = []
    Images2=[]
    Description2=[]
    url2 = "https://www.flipkart.com/search?q=boys+t+shirt+12%2F13+years&sid=clo%2Cash%2Cank%2Cpgi&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&as-pos=1&as-type=RECENT&suggestionId=boys+t+shirt+12%2F13+years%7CKids%27+T-shirts&requestId=4760a67d-8bf7-4c4e-adab-d9accf664d73&as-searchtext=boys%20t%20shirt%20"
    r2 = requests.get(url2)
    soup2 = BeautifulSoup(r2.text, "lxml")
    names2 = soup2.find_all("div", class_="syl9yP")
    for i in names2:
        name2 = i.text
        Product_name2.append(name2)
    # Indian Rupee symbol
    prices2 = soup2.find_all("div", class_="Nx9bqj")
    for i in prices2:
        price2 = i.text  # Add the Indian Rupee symbol to each price
        Prices2.append(price2)
    desc2 = soup2.find_all("a", class_="WKTcLC")
    for i in desc2:
        description2 = i.text
        Description2.append(description2)
    print(Product_name2)
    print(Prices2)
    print(Description2)

    # The rest of your code for processing images
    url2 = "https://www.flipkart.com/search?q=boys+t+shirt+12%2F13+years&sid=clo%2Cash%2Cank%2Cpgi&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&as-pos=1&as-type=RECENT&suggestionId=boys+t+shirt+12%2F13+years%7CKids%27+T-shirts&requestId=4760a67d-8bf7-4c4e-adab-d9accf664d73&as-searchtext=boys%20t%20shirt%20"
    page2 = urllib.request.urlopen(url2)
    page_soup2 = BeautifulSoup(page2, "html.parser")
    img_items2 = page_soup2.find("div", {"class": "DOjaWF YJG4Cf"})
    img_div2 = img_items2.find_all(class_="gqcSqV YGE0gZ")
    i=0
    for img in img_div2:
        img_tag2 = img.find("img")
        img_src2 = img_tag2.get('src')
        if img_src2[:1] == '/':
            image2 = 'https:' + img_src2
        else:
            image2 = img_src2
        print(image2)
        file_name2=str(i)
        i+=1
        img_file2=open(file_name2 + '.jpeg' , 'wb' )
        img_file2.write(urllib.request.urlopen(image2).read())
        img_file2.close()
        Images2.append(image2)
        
    Product_name4 = []
    Prices4 = []
    Images4=[]
    Description4=[]
    url4 = "https://www.flipkart.com/search?q=girls%20dress%2011%2F12years%20frock%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    r4 = requests.get(url4)
    soup4 = BeautifulSoup(r4.text, "lxml")
    names4 = soup4.find_all("div", class_="syl9yP")
    for i in names4:
        name4 = i.text
        Product_name4.append(name4)
        # Indian Rupee symbol
    prices4 = soup4.find_all("div", class_="Nx9bqj")
    for i in prices4:
         price4 = i.text  # Add the Indian Rupee symbol to each price
         Prices4.append(price4)
    desc4 = soup4.find_all("a", class_="WKTcLC BwBZTg")
    for i in desc4:
        description4 = i.text
        Description4.append(description4)
    print(Product_name4)
    print(Prices4)
    print(Description4)

    # The rest of your code for processing images
    url4 = "https://www.flipkart.com/search?q=girls%20dress%2011%2F12years%20frock%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    page4 = urllib.request.urlopen(url4)
    page_soup4 = BeautifulSoup(page4, "html.parser")
    img_items4 = page_soup4.find("div", {"class": "DOjaWF YJG4Cf"})
    img_div4 = img_items4.find_all(class_="gqcSqV YGE0gZ")
    i=0
    for img in img_div4:
        img_tag4 = img.find("img")
        img_src4 = img_tag4.get('src')
        if img_src4[:1] == '/':
            image4 = 'https:' + img_src4
        else:
            image4 = img_src4
            print(image4)
            file_name4=str(i)
            i+=1
            img_file4=open(file_name4 + '.jpeg' , 'wb' )
            img_file4.write(urllib.request.urlopen(image4).read())
            img_file4.close()
            Images4.append(image4)

    context = {
        'products': zip(Product_name, Prices, Description, Images),
        'products1': zip(Product_name1, Prices1, Description1, Images1),
        'products2': zip(Product_name2, Prices2, Description2, Images2),
        'products4': zip(Product_name4, Prices4, Description4, Images4),
    }
    
    return render(request, 'scraped_data1.html', context)

def add_to_wishlist(request):
    if request.method == 'POST' and request.is_ajax():
        # Get the product ID from the request
        product_id = request.POST.get('product_id')

        # Perform operations to add the product to the wishlist
        # You can save the product ID in the user's session, database, or any other storage mechanism

        # For demonstration purposes, let's assume we have a Product model
        # and we retrieve the product details to return in the response
        from .models import Product
        try:
            product = Product.objects.get(id=product_id)
            # Simulate adding the product to the wishlist
            # You should replace this with your actual logic
            # For example, you might save the product ID to the user's profile
            return JsonResponse({'success': True, 'product_name': product.name})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    else:
        # Handle invalid requests
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)



def scrape_flipkart1(request):
    Product_name = []
    Prices = []
    Description = []
    Images = []
    url = "https://www.flipkart.com/search?q=tops+for+women&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=4"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    names = soup.find_all("div", class_="syl9yP")
    for i in names:
        name = i.text
        Product_name.append(name)
    # Indian Rupee symbol
    prices = soup.find_all("div", class_="Nx9bqj")
    for i in prices:
        price = i.text  # Add the Indian Rupee symbol to each price
        Prices.append(price)
    desc = soup.find_all("a", class_="WKTcLC")
    for i in desc:
        description = i.text
        Description.append(description)
    print(Product_name)
    print(Prices)
    print(Description)
    # The rest of your code for processing images
    url = "https://www.flipkart.com/search?q=tops+for+women&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=4"
    page = urllib.request.urlopen(url)
    page_soup = BeautifulSoup(page, "html.parser")
    img_items = page_soup.find("div", {"class": "DOjaWF YJG4Cf"})
    img_div = img_items.find_all(class_="gqcSqV YGE0gZ")
    i=0
    for img in img_div:
        img_tag = img.find("img")
        img_src = img_tag.get('src')
        if img_src[:1] == '/':
            image = 'https:' + img_src
        else:
            image = img_src
        print(image)
        file_name=str(i)
        i+=1
        img_file=open(file_name + '.jpeg' , 'wb' )
        img_file.write(urllib.request.urlopen(image).read())
        img_file.close()
        Images.append(image)
    

    # Define Images1 for the second set of products
    Images1 = []
    Product_name1=[]
    Prices1=[]
    Description1=[]
    url1 = "https://www.flipkart.com/search?q=men%20t%20shirt%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    r1 = requests.get(url1)
    soup1 = BeautifulSoup(r1.text, "lxml")
    names1 = soup1.find_all("div", class_="syl9yP")
    for i in names1:
        name1 = i.text
        Product_name1.append(name1)
    # Indian Rupee symbol
    prices1 = soup1.find_all("div", class_="Nx9bqj")
    for i in prices1:
        price1 = i.text  # Add the Indian Rupee symbol to each price
        Prices1.append(price1)
    desc1 = soup1.find_all("a", class_="WKTcLC")
    for i in desc1:
        description1 = i.text
        Description1.append(description1)
    print(Product_name1)
    print(Prices1)
    print(Description1)

    url1 = "https://www.flipkart.com/search?q=men%20t%20shirt%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    page1 = urllib.request.urlopen(url1)
    page_soup1 = BeautifulSoup(page1, "html.parser")
    img_items1 = page_soup1.find("div", {"class": "DOjaWF YJG4Cf"})
    img_div1 = img_items1.find_all(class_="gqcSqV YGE0gZ")
    i=0
    for img in img_div1:
        img_tag1 = img.find("img")
        img_src1 = img_tag1.get('src')
        if img_src1[:1] == '/':
            image1 = 'https:' + img_src1
        else:
            image1 = img_src1
        print(image1)
        file_name1=str(i)
        i+=1
        img_file1=open(file_name1 + '.jpeg' , 'wb' )
        img_file1.write(urllib.request.urlopen(image1).read())
        img_file1.close()
        Images1.append(image1)
        
        
    Product_name2 = []
    Prices2 = []
    Images2=[]
    Description2=[]
    url2 = "https://www.flipkart.com/search?q=boys+t+shirt+12%2F13+years&sid=clo%2Cash%2Cank%2Cpgi&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&as-pos=1&as-type=RECENT&suggestionId=boys+t+shirt+12%2F13+years%7CKids%27+T-shirts&requestId=4760a67d-8bf7-4c4e-adab-d9accf664d73&as-searchtext=boys%20t%20shirt%20"
    r2 = requests.get(url2)
    soup2 = BeautifulSoup(r2.text, "lxml")
    names2 = soup2.find_all("div", class_="syl9yP")
    for i in names2:
        name2 = i.text
        Product_name2.append(name2)
    # Indian Rupee symbol
    prices2 = soup2.find_all("div", class_="Nx9bqj")
    for i in prices2:
        price2 = i.text  # Add the Indian Rupee symbol to each price
        Prices2.append(price2)
    desc2 = soup2.find_all("a", class_="WKTcLC")
    for i in desc2:
        description2 = i.text
        Description2.append(description2)
    print(Product_name2)
    print(Prices2)
    print(Description2)

    # The rest of your code for processing images
    url2 = "https://www.flipkart.com/search?q=boys+t+shirt+12%2F13+years&sid=clo%2Cash%2Cank%2Cpgi&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&as-pos=1&as-type=RECENT&suggestionId=boys+t+shirt+12%2F13+years%7CKids%27+T-shirts&requestId=4760a67d-8bf7-4c4e-adab-d9accf664d73&as-searchtext=boys%20t%20shirt%20"
    page2 = urllib.request.urlopen(url2)
    page_soup2 = BeautifulSoup(page2, "html.parser")
    img_items2 = page_soup2.find("div", {"class": "DOjaWF YJG4Cf"})
    img_div2 = img_items2.find_all(class_="gqcSqV YGE0gZ")
    i=0
    for img in img_div2:
        img_tag2 = img.find("img")
        img_src2 = img_tag2.get('src')
        if img_src2[:1] == '/':
            image2 = 'https:' + img_src2
        else:
            image2 = img_src2
        print(image2)
        file_name2=str(i)
        i+=1
        img_file2=open(file_name2 + '.jpeg' , 'wb' )
        img_file2.write(urllib.request.urlopen(image2).read())
        img_file2.close()
        Images2.append(image2)
        
    Product_name4 = []
    Prices4 = []
    Images4=[]
    Description4=[]
    url4 = "https://www.flipkart.com/search?q=girls%20dress%2011%2F12years%20frock%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    r4 = requests.get(url4)
    soup4 = BeautifulSoup(r4.text, "lxml")
    names4 = soup4.find_all("div", class_="syl9yP")
    for i in names4:
        name4 = i.text
        Product_name4.append(name4)
        # Indian Rupee symbol
    prices4 = soup4.find_all("div", class_="Nx9bqj")
    for i in prices4:
         price4 = i.text  # Add the Indian Rupee symbol to each price
         Prices4.append(price4)
    desc4 = soup4.find_all("a", class_="WKTcLC BwBZTg")
    for i in desc4:
        description4 = i.text
        Description4.append(description4)
    print(Product_name4)
    print(Prices4)
    print(Description4)

    # The rest of your code for processing images
    url4 = "https://www.flipkart.com/search?q=girls%20dress%2011%2F12years%20frock%20stylish&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    page4 = urllib.request.urlopen(url4)
    page_soup4 = BeautifulSoup(page4, "html.parser")
    img_items4 = page_soup4.find("div", {"class": "DOjaWF YJG4Cf"})
    img_div4 = img_items4.find_all(class_="gqcSqV YGE0gZ")
    i=0
    for img in img_div4:
        img_tag4 = img.find("img")
        img_src4 = img_tag4.get('src')
        if img_src4[:1] == '/':
            image4 = 'https:' + img_src4
        else:
            image4 = img_src4
            print(image4)
            file_name4=str(i)
            i+=1
            img_file4=open(file_name4 + '.jpeg' , 'wb' )
            img_file4.write(urllib.request.urlopen(image4).read())
            img_file4.close()
            Images4.append(image4)

    context = {
        'products': zip(Product_name, Prices, Description, Images),
        'products1': zip(Product_name1, Prices1, Description1, Images1),
        'products2': zip(Product_name2, Prices2, Description2, Images2),
        'products4': zip(Product_name4, Prices4, Description4, Images4),
    }
    
    return render(request, 'scraped_data1.html', context)

