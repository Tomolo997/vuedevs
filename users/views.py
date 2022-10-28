from django.urls import reverse
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
import stripe
import os
from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Business, Conversation,Customer, Developer ,Verifications, RoleType, RoleLevel, Availability, Message
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib import messages
from .forms import BusinessForm, CustomUserCreationForm, DeveloperForm, MessageForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .utils_mail import Mailer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import generate_random_code , get_business,get_customer ,get_developer, changetimezone
# Create your views here.
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY  if settings.DEBUG else settings.STRIPE_LIVE_SECRET_KEY
endpoint_secret = 'whsec_de78d3463a00ce9df2b085fe6f4521bd5b4dc1745b34c38b04dc8ed0d66cdbbf'
def index(request):
    developers = Developer.objects.all().order_by('-created')[:10]
    data = []
    for developer in developers:
        developer_object = {}
        available = Availability.objects.get(developer_id=developer)
        developer_object['available'] = available.available
        developer_object['hero'] = developer.hero
        developer_object['bio'] = developer.bio
        developer_object['profile_image'] = developer.imageURL
        developer_object['id'] = developer.id
        data.append(developer_object)
        
    ctx = {'developers': data}
    return render(request, 'index.html',ctx)

def aboutPage(request):
    return render(request, 'pages/about.html')

def createCheckoutSession(request):
    if request.user.is_anonymous:
        return redirect('login')
    if not get_business(request.user):
        return redirect('create-business')
    req_user = request.user
    if get_customer(req_user) and get_business(req_user):
        return redirect('index')
    price_id = request.GET['priceId']
    session = stripe.checkout.Session.create(
    success_url='https://djangodevs.com/success?session_id={CHECKOUT_SESSION_ID}' if not settings.DEBUG else 'http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='https://djangodevs.com/cancel',
    mode='subscription',
    payment_method_types=['card'],
    line_items=[{
        'price': price_id,
            # For metered billing, do not pass quantity
        'quantity': 1
    }],
        )
    return redirect(session.url, code=303)


def successurl(request):
    user = request.user
    if request.method == 'GET' and 'session_id' in request.GET:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'])
        customer = Customer()
        customer.user = user
        customer.stripe_customer_id = session.customer
        customer.stripe_subscription_id = session.subscription
        customer.save()
        business= Business.objects.get(user=user)
        business.is_payed=True;
        business.save()

    return render(request,'pages/success.html')

def cancelurl(request):
    return redirect('index')


def developersPage(request):
    developers = Developer.objects.all().order_by('-created')
    allDevs = len(developers)
    data = []
    filtering_parameters = []
    if request.GET.get('role_level'):
        for el in request.GET.getlist('role_level'):
            filtering_parameters.append(el)
    if request.GET.get('timezone'):
        for el in request.GET.getlist('timezone'):
            filtering_parameters.append(changetimezone(el))
    if request.GET.get('role_type'):
        for el in request.GET.getlist('role_type'):
            filtering_parameters.append(el)
    for developer in developers:
        developer_object = {}
        available = Availability.objects.get(developer_id=developer)
        role_level = RoleLevel.objects.get(developer_id=developer)
        role_type = RoleType.objects.get(developer_id=developer)
        developer_object['available'] = available.available
        developer_object['open'] = available.open
        developer_object['not_available'] = available.not_available
        developer_object['junior'] = role_level.junior
        developer_object['senior'] = role_level.senior
        developer_object['mid'] = role_level.mid
        developer_object['principal'] = role_level.principal
        developer_object['c_level'] = role_level.c_level
        developer_object['full_time_job'] = role_type.full_time_job
        developer_object['part_time_contract'] = role_type.part_time_contract
        developer_object['full_time_contract'] = role_type.full_time_contract
        developer_object['hero'] = developer.hero
        developer_object['bio'] = developer.bio
        developer_object['timezone'] = developer.timezone
        developer_object['profile_image'] = developer.imageURL
        developer_object['id'] = developer.id
        data.append(developer_object)
    for developer in data: 
        developer_filtering =[]
        if(developer['available']):
            developer_filtering.append('available')
        if(developer['open']):
            developer_filtering.append('open')
        if(developer['not_available']):
            developer_filtering.append('not_available')
        if(developer['junior']):
            developer_filtering.append('junior')
        if(developer['mid']):
            developer_filtering.append('mid')
        if(developer['senior']):
            developer_filtering.append('senior')
        if(developer['principal']):
            developer_filtering.append('principal')
        if(developer['full_time_job']):
            developer_filtering.append('full_time_job')
        if(developer['full_time_contract']):
            developer_filtering.append('full_time_contract')
        if(developer['part_time_contract']):
            developer_filtering.append('part_time_contract')
        if(developer['timezone']):
            developer_filtering.append(developer['timezone'])
        developer['filtering_params'] = developer_filtering
    if(len(filtering_parameters) > 0):
        for developer in data:
            developer['show'] = False
            for params in filtering_parameters:
                if(params in developer['filtering_params']):
                    developer['show'] = True
            if developer['show'] == False:
                data.pop(data.index(developer))
    page = request.GET.get('page', 1)
    paginator = Paginator(data,5)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    return render(request, 'pages/developers.html', {'developers': data , 'allDevs':allDevs})  

def pricingPage(request):
    priceId = 'price_1LesrLK8VMxCSHFy02SMvsKQ' if settings.DEBUG else 'price_1LiwXtK8VMxCSHFyEMX9kOkg'
    return render(request, 'pages/pricing.html',{'priceId':priceId})

def developerPage(request,pk):
    developer = Developer.objects.get(id=pk)
    role_type = developer.roletype_set.all()
    role_level = developer.rolelevel_set.all()
    available = developer.availability_set.all()
    role_type_object = []
    role_level_object = []
    available_object = []
    for role in role_type.iterator():
        if(role.full_time_job):
            role_type_object.append('Full time job')
        if(role.full_time_contract):
            role_type_object.append('Part time job')
        if(role.part_time_contract):
            role_type_object.append('Part time contract')
    for role in role_level.iterator():
        if(role.junior):
            role_level_object.append('junior')
        if(role.mid):
            role_level_object.append('mid')
        if(role.senior):
            role_level_object.append('senior')
        if(role.principal):
            role_level_object.append('principal')
        if(role.c_level):
            role_level_object.append('c_level')
    for role in available.iterator():
        if(role.available):
            available_object.append('available')
        if(role.open):
            available_object.append('open')
        if(role.not_available):
            available_object.append('not_available')

    is_there_customer=False
    if not  request.user.is_anonymous:
        customer = get_customer(user=request.user)
        if customer:
            is_there_customer=True
    ctx = {'developer':developer, "role_type" : role_type_object, 'role_level': role_level_object, 'availability': available_object,'is_there_customer':is_there_customer}
    return render(request, 'pages/developer.html',ctx)

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST': 
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.username = user.email
            user.save()
            verification_code = Verifications.objects.create(verification_code=generate_random_code(), user = user)
            verification_code.save()

            Mailer.sendVerificationMail(user.email,verification_code.verification_code,user.id)
            return redirect('verify-please')

    context = {'page': page, 'form': form}
    return render(request, 'pages/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active == False:
                return redirect("verify-please")
            login(request, user)
            developer = get_developer(user)
            business = get_business(user)
            if developer == False and business == False:
                return redirect('create-profile')
            return redirect("index")

            t

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'pages/login_register.html')

@login_required(login_url='login')
def editAccount(request):
    return render(request, 'pages/main-profile-form.html')

def verifyUser(request,token):
    user = request.GET["user"]
    user = User.objects.get(id=user)
    verification_code = Verifications.objects.get(user_id=user.id)
    if verification_code is not None:
        if token == verification_code.verification_code:
            user.is_active=True
            user.save()
    return render(request, 'pages/verification.html')

def verifyPlease(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'pages/verify-please.html')

def newDeveloperOrBusiness(request):
    user = request.user
    developer = get_developer(user)
    business = get_business(user)
    if developer or business:
        return redirect('index')
    return render(request, 'pages/new-developer-or-business.html')

@login_required(login_url='login')
def createNewDeveloper(request):
    user = request.user
    developer = get_developer(user)
    #IF the user that has developer account want to get this page
    if developer:
        return redirect('edit-developer')

    form = DeveloperForm(instance=user)
    if request.method == 'POST':
        #create developer
        form = DeveloperForm(request.POST,request.FILES)
        if form.is_valid():
            developer = form.save(commit=False)
            developer.user = user
            developer.save()
            print(form.is_valid())
            developer_id = get_developer(developer.user)
            role_type = request.POST.getlist("role_type")
            role_level = request.POST.getlist("role_level")
            availability = request.POST.getlist("availability")
            if(availability):
                create_object = {}
                if('available' in availability):
                    create_object['available'] = True
                else:
                    create_object['available'] = False
                if('open' in availability):
                    create_object['open'] = True
                else:
                    create_object['open'] = False
                if('not_available' in availability):
                    create_object['not_available'] = True
                else:
                    create_object['not_available'] = False
                role_level_create = Availability.objects.create(available=create_object['available'],open=create_object['open'],not_available=create_object['not_available'], developer_id =developer_id)
                role_level_create.save()
            if(role_level):
                create_object = {}
                if('junior' in role_level):
                    create_object['junior'] = True
                else:
                    create_object['junior'] = False
                if('mid' in role_level):
                    create_object['mid'] = True
                else:
                    create_object['mid'] = False
                if('senior' in role_level):
                    create_object['senior'] = True
                else:
                    create_object['senior'] = False
                if('principal' in role_level):
                    create_object['principal'] = True
                else:
                    create_object['principal'] = False
                if('c_level' in role_level):
                    create_object['c_level'] = True
                else:
                    create_object['c_level'] = False
                role_level_create = RoleLevel.objects.create(junior=create_object['junior'],mid=create_object['mid'],senior=create_object['senior'],principal=create_object['principal'],c_level=create_object['c_level'], developer_id = developer_id)
                role_level_create.save()
            if(role_type):
                create_object = {}
                if('full_time_contract' in role_type):
                    create_object['full_time_contract'] = True
                else:
                    create_object['full_time_contract'] = False
                if('part_time_contract' in role_type):
                    create_object['part_time_contract'] = True
                else:
                    create_object['part_time_contract'] = False
                if('full_time_job' in role_type):
                    create_object['full_time_job'] = True
                else:
                    create_object['full_time_job'] = False
                role_type_create = RoleType.objects.create(full_time_contract=create_object['full_time_contract'],part_time_contract=create_object['part_time_contract'],full_time_job=create_object['full_time_job'], developer_id = developer_id)
                role_type_create.save()

            return redirect('index')
        else:
            print ('error')
            print (form.errors, len(form.errors))
    ctx = {'form': form}
    return render(request, 'pages/new-developer.html',ctx)

@login_required(login_url='login')
def editDeveloper(request):
    user = request.user
    developer = get_developer(user)
    #IF the user that has developer account want to get this page
    if not developer:
        return redirect('create-developer')

    userForm = DeveloperForm(instance=user)
    form = DeveloperForm(instance=developer)
    role_type_ctx = RoleType.objects.filter(developer_id=developer)
    role_level_ctx = RoleLevel.objects.filter(developer_id=developer)
    available_ctx = Availability.objects.filter(developer_id=developer)
    if request.method == 'POST':
        #create developer
        form = DeveloperForm(request.POST,request.FILES, instance=developer)
        if form.is_valid():
            file = request.FILES.getlist('profile_image')
            form.save()
            role_type = request.POST.getlist("role_type")
            role_level = request.POST.getlist("role_level")
            availability = request.POST.getlist("availability")
            if(availability):
                create_object = {}
                if('available' in availability):
                    create_object['available'] = True
                else:
                    create_object['available'] = False
                if('open' in availability):
                    create_object['open'] = True
                else:
                    create_object['open'] = False
                if('not_available' in availability):
                    create_object['not_available'] = True
                else:
                    create_object['not_available'] = False
                availability_create = Availability.objects.filter(developer_id=developer).update(available=create_object['available'],open=create_object['open'],not_available=create_object['not_available'])
            if(role_level):
                create_object = {}
                if('junior' in role_level):
                    create_object['junior'] = True
                else:
                    create_object['junior'] = False
                if('mid' in role_level):
                    create_object['mid'] = True
                else:
                    create_object['mid'] = False
                if('senior' in role_level):
                    create_object['senior'] = True
                else:
                    create_object['senior'] = False
                if('principal' in role_level):
                    create_object['principal'] = True
                else:
                    create_object['principal'] = False
                if('c_level' in role_level):
                    create_object['c_level'] = True
                else:
                    create_object['c_level'] = False
                role_level_create = RoleLevel.objects.filter(developer_id=developer).update(junior=create_object['junior'],mid=create_object['mid'],senior=create_object['senior'],principal=create_object['principal'],c_level=create_object['c_level'])
            if(role_type):
                create_object = {}
                if('full_time_contract' in role_type):
                    create_object['full_time_contract'] = True
                else:
                    create_object['full_time_contract'] = False
                if('part_time_contract' in role_type):
                    create_object['part_time_contract'] = True
                else:
                    create_object['part_time_contract'] = False
                if('full_time_job' in role_type):
                    create_object['full_time_job'] = True
                else:
                    create_object['full_time_job'] = False
                role_type_create = RoleType.objects.filter(developer_id=developer).update(full_time_contract=create_object['full_time_contract'],part_time_contract=create_object['part_time_contract'],full_time_job=create_object['full_time_job'])
            return redirect('index')

    ctx = {'form': form, 'userForm': userForm, 'developer':developer, 'role_type':role_type_ctx,'role_level':role_level_ctx,'availability':available_ctx}
    return render(request, 'pages/edit-developer.html',ctx)


@login_required(login_url='login')
def createNewBusiness(request):
    user = request.user
    business = get_business(user)
    #IF the user that has business account want to get this page
    if business:
        return redirect('edit-business')
    form = BusinessForm(instance=user)
    if request.method == 'POST':
        form = BusinessForm(request.POST,request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = user
            business.save()
            url = reverse('create-checkout-session')
            return redirect(f'{url}?priceId=price_1LesrLK8VMxCSHFy02SMvsKQ') 
    return render(request, 'pages/new-business.html',{'form':form})

@login_required(login_url='login')
def editBusiness(request):
    user = request.user
    business = get_business(user)
    if not business:
        return redirect('create-business')
    form = BusinessForm(instance=business)
    userForm = BusinessForm(instance=user)
    if request.method == 'POST':
        form = BusinessForm(request.POST,request.FILES, instance=business)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'pages/edit-business.html',{'form':form, 'business' : business,'userForm':userForm})

@login_required(login_url='login')
def conversationsPage(request):
    user = request.user
    business = get_business(user)
    developer = get_developer(user)
    conversations = Conversation.objects.filter(Q (business_id=business) | Q(developer_id=developer))
    conversation_list=[]
    index = 0
    for conv in conversations:
        messages_from_convearsatison=Message.objects.filter(Q (conversation=conv)).first()
        conversation_object={}
        conversation_object['message'] = messages_from_convearsatison
        conversation_object['developer_id'] = conv.developer_id
        conversation_object['business_id'] = conv.business_id
        conversation_object['id'] = conv.id
        conversation_list.append(conversation_object)
        index = 1+ index
    # messages_list_businness = []
    # for message in business_messages:
    #     final_message = {}
    #     final_message['sender'] = get_developer_or_business_from_id(message['sender_id'])
    #     final_message['body'] = message['body']
    #     messages_list_businness.append(final_message)
    # print("messages_list_businness",messages_list_businness)
    return render(request, 'pages/conversations.html', {'conversations': conversation_list})


@login_required(login_url='login')
def conversationPage(request,pk):
    user = request.user
    # conversations as developer 
    developer = get_developer(user)
    conversations = Conversation.objects.filter(developer_id=developer)

    
    return render(request, 'pages/yea.html')

@login_required(login_url='login')
def conversationsMessagePage(request,pk):
    user = request.user
    conversation = Conversation.objects.get(id=pk)
    conversation_messages = Message.objects.filter(conversation=conversation).order_by('created')
    # Find out who is the sender here
    developer = get_developer(user)
    business = get_business(user)

    sender_id = ""
    sender_type = ""
    if (developer == conversation.developer_id):
        sender_id = developer.id
        sender_type = 'developer'
    elif (business == conversation.business_id):
        sender_id = business.id
        sender_type = 'business'

    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender_id=sender_id
            message.sender_type = sender_type
            message.conversation = conversation
            message.save()
            return redirect('conversations_message',pk=conversation.id)
    
    context = {'conversation':conversation,'conv_messages':conversation_messages, 'form':form}
    return render(request, 'pages/conversations-messages.html',context)

@login_required(login_url='login')
def conversationsNewPage(request,pk):
    user = request.user
    developer = Developer.objects.get(id=pk)
    business = get_business(user)
    if not business: 
        return redirect('create-business')
    if not business.is_payed: 
        return redirect('pricing_page')
    conversation = Conversation.objects.filter(Q(developer_id=developer) & Q(business_id=business)).first()
    if conversation:
        return redirect('conversations_message',pk=conversation.id)
    # if there is a conversation please redirect them to to the proper page
    # ------
    
    #If there is no business redirect them to the fucking create business 
    
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            conversation_create = Conversation.objects.create(developer_id=developer,business_id=business)
            conversation_create.save()
            message = form.save(commit=False)
            message.sender_id = business.id
            message.conversation = conversation_create
            message.sender_type = "business"
            message.save()
            return redirect('index')

    context = { 'form': form,'developer':developer}
    
    return render(request, 'pages/conversations-new.html',context)


def handleNotFound(request,exception):
    return render(request,'pages/notfound.html')


def my_custom_page_not_found_view(request,exception):
    return render(request,'pages/notfound.html')

def my_custom_error_view(request):
    return render(request,'pages/notfound_500.html')