
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import ImageUploadForm, LoginForm, RegisterForm, PreferencesForm, PasswordForm
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


from .models import Picture, Profile, Preferences
from PIL import Image


# new
def settings_(request):
    user = request.user
    if request.method == 'POST':
        #form1 = PreferencesForm(request.POST)
        form2 = PasswordForm(request.POST)
        form1 = PreferencesForm(request.POST)

        if form1.is_valid():
            username = form1.cleaned_data['username']
            email = form1.cleaned_data['email']
            bio = form1.cleaned_data['bio']

            if bool(Preferences.objects.all().filter(user=user)):

                if username != '':
                    user.preferences.username = username
                else:
                    user.preferences.username = user.preferences.username

                if email != '':
                    user.preferences.email = email
                else:
                    user.preferences.email = user.preferences.email

                if bio != '':
                    user.preferences.bio = bio
                else:
                    user.preferences.bio = user.preferences.bio

                user.preferences.save()
                user.username = user.preferences.username
                user.save()

            else:
                Preferences.objects.create(user=user, username=username, email=email, bio=bio)

            messages.success(request, 'Account has been updated')


    else:
        form1 = PreferencesForm(request.POST)

    form1 = PreferencesForm()
    form2 = PasswordForm(user)
    context = {
        'form1': form1,
        'user': user,
        'form2': form2,
    }
    return render(request, 'settings.html', context)

def delete_account(request):
    user = request.user
    User.objects.get(id=user.id).delete()
    return redirect('/')

def home_page(request):
    return redirect('chat')



# one_day = timedelta(days=1)
# first_day = datetime.date.today()
# second_day = first_day + one_day
# third_day = second_day + one_day
# forth_day = third_day + one_day
# fifth_day = forth_day + one_day
# sixth_day = fifth_day + one_day
# seventh_day = sixth_day + one_day
#
#
# def home_page(request):
#     today = datetime.datetime.today()
#     weekday = today.strftime('%A')
#     weekday_abr = today.strftime('%a')
#     month = today.strftime('%B')
#     day = today.strftime('%d')
#     year = today.strftime('%Y')
#
#     first_day_avg = []
#     second_day_avg = []
#     third_day_avg = []
#     forth_day_avg = []
#     fifth_day_avg = []
#
#
#     city = 'Warsaw'
#     url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid=10e88ba16af591351dde98a3b8254127&units=metric'
#     r = requests.get(url).json()
#     lists = r['list']
#     for i in lists:
#         day_ = i['dt_txt'].split()[0].split('-')[2]
#         month_ = i['dt_txt'].split()[0].split('-')[1]
#         year_ = i['dt_txt'].split()[0].split('-')[0]
#         if datetime.date(day=int(day_), month=int(month_), year=int(year_)) == first_day:
#             first_day_avg.append(i['main']['temp'])
#         elif datetime.date(day=int(day_), month=int(month_), year=int(year_)) == second_day:
#             second_day_avg.append(i['main']['temp'])
#         elif datetime.date(day=int(day_), month=int(month_), year=int(year_)) == third_day:
#             third_day_avg.append(i['main']['temp'])
#         elif datetime.date(day=int(day_), month=int(month_), year=int(year_)) == forth_day:
#             forth_day_avg.append(i['main']['temp'])
#         elif datetime.date(day=int(day_), month=int(month_), year=int(year_)) == fifth_day:
#             fifth_day_avg.append(i['main']['temp'])
#
#     temperature = r['list'][0]['main']['temp']
#     description = r['list'][0]['weather'][0]['description']
#     icon = r['list'][0]['weather'][0]['icon']
#     src_link = f"http://openweathermap.org/img/wn/{icon}@2x.png"
#
#     context = {
#         'weekday': weekday,
#         'month': month,
#         'day': day,
#         'year': year,
#         'temperature': int(temperature),
#         'description': description,
#         'weekday_abr': weekday_abr,
#         'first_day': first_day.strftime('%a'),
#         'second_day': second_day.strftime('%a'),
#         'third_day': third_day.strftime('%a'),
#         'forth_day': forth_day.strftime('%a'),
#         'fifth_day': fifth_day.strftime('%a'),
#         'sixth_day': sixth_day.strftime('%a'),
#         'seventh_day': seventh_day.strftime('%a'),
#         # 'temp1': sum(first_day_avg) / len(first_day_avg),
#         #'temp2': int(sum(second_day_avg)/ len(second_day_avg)),
#         'temp3': int(sum(third_day_avg) / len(third_day_avg)),
#         'temp4': int(sum(forth_day_avg) / len(forth_day_avg)),
#         'temp5': int(sum(fifth_day_avg) / len(fifth_day_avg)),
#         'icon': src_link,
#     }
#     #url = 'api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}'
#     return render(request, 'home.html', context)

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            validate_password(password2)

            User.objects.create_user(username=username, password=password1, is_active=True)
            obj = User.objects.get(username=username)
            Picture.objects.create(user=obj)


            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        #form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
            #user = User.objects.get(username=username, password=password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')

        else:
            messages.error(request, "This account doesn't exist, Please sign up")

    form = LoginForm()
    return render(request, 'login.html', {'form': form})

@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    if bool(Profile.objects.all().filter(user=user)):
        user.profile.is_online = True
        user.profile.save()
    else:
        Profile.objects.create(user=user, is_online=True)

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.profile.is_online = False
    user.profile.save()

def logout(request):
    auth.logout(request)
    return redirect('/')

def profile(request, id):
    friend_profile = User.objects.get(id=id)
    friends = friend_profile.outbox.all()
    context = {
        'friend': friend_profile,
        'friends': friends
    }
    return render(request, 'profile.html', context)

@login_required
def my_profile(request):
    form = ImageUploadForm()
    user = request.user
    if bool(Picture.objects.all().filter(user=user)):
        obj = Picture.objects.get(user=user)
        pic = obj.pic
        return render(request, 'my_profile.html', {'form': form, 'pic': pic})
    else:
        return render(request, 'my_profile.html', {'form': form})

    # user = request.user
    # #user.picture.pic.name =
    # #pic_obj = Picture.objects.get(user=user)
    #
    #
    # # obj = Picture.objects.all().filter(user=user)
    # # if obj:
    # #     pic_obj = Picture.objects.get(user=user)
    # #     pic = pic_obj.pic
    # return render(request, 'my_profile.html', {'form': form})



def upload(request):
    user = request.user
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            if bool(Picture.objects.all().filter(user=user)):
                Picture.objects.get(user=user).delete()
                #user.picture.pic.delete()
            picture = form.save(commit=False)
            picture.user = user
            picture.save()
            # else:
            #     picture = form.save(commit=False)
            #     picture.user = user
            #     picture.save()


            print("success")

            return redirect('my_profile')

        else:
            print('not valid')
            return redirect('my_profile')

    else:
        print("not post")
        return redirect('my_profile')




#
# def send_login_email(request):
#     email = request.POST['email']
#     user = User.objects.get(email=email)
#     if not user:
#         user = User.objects.create(email=email)
#         url = request.build_absolute_uri(
#             reverse('login') + '?token=' + str(user.uid)
#         )
#         message_body = f"Your login link:\n\n{url}"
#         send_mail(
#             'Your login link to MailApp',
#             message_body,
#             'noreply@chatapp',
#             [email]
#         )
#         messages.success(request, f"Email link sent to {email}")
#         return redirect('/')
#     else:
#         auth.login(request, user)
#         return redirect('/')
#
# def login(request):
#     string_path = request.get_full_path()
#     uid = string_path.split('=')
#     uid = uid[1]
# #     user = User.objects.get(uid=token)
# #     email = user.email
#     # token = request.POST.get('token')
#     # uid = request.POST.get('token')
#     user = auth.authenticate(uid=uid)
#     if user:
#         auth.login(request, user)
#
#         return redirect('/')
#
#     return render(request, 'notlogged.html', {'user': user, 'uid': uid})
#
# def logout(request):
#     auth.logout(request)
#     return redirect('/')
#
#
#
#
#
#
#     #print(uid)
#     # user = auth.authenticate(uid=uid)
#     # if user is not None:
#     #     auth.login(request, user)
#     # return redirect('/')
#
