from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
# from django.views import generic

from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from .models import Category, Page
from datetime import datetime


def visitor_cookie_handler(request, response):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(request.COOKIES.get('visits', '1'))
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # update the last visit cookie now that we have updated the count
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        visits = 1
        # set the last visit cookie
        response.set_cookie('last_visit', last_visit_cookie)

    # Update/set the visits cookie
    response.set_cookie('visits', visits)


# Create your views here.
def index(request):
    # запишем в сессию тестовую информацию
    request.session.set_test_cookie()

    # return HttpResponse('Rango says hey there partner!<br><a href="/rango/about/">about page</a>')
    # return render(request, 'rango/index.html', {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"})
    category_list = Category.objects.order_by('-likes')[:5]
    most_viewed_pages = Page.objects.order_by('-views')[:5]

    context_dict = {
        'categories': category_list,
        'most_viewed_pages': most_viewed_pages
    }
    # рендерим в переменную
    response = render(request, 'rango/index.html', context=context_dict)
    # устанавливаем куку
    visitor_cookie_handler(request, response)
    # отдаем ответ
    return response


def about(request):
    # если тестовая информация есть в сессии
    if request.session.test_cookie_worked():
        # выведем строку в консоли
        print("TEST COOKIE WORKED!")
        # удалим тестовую информацию из сессии
        request.session.delete_test_cookie()

    return render(request, 'rango/about.html', {'name': 'sanya'})


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        page = Page.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['pages'] = page
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved
            # We could give a confirmation message
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    # try:
    #     category = Category.objects.get(slug=category_name_slug)
    # except Category.DoesNotExist:
    #     category = None

    category = get_object_or_404(Category, slug=category_name_slug)

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {
        'form': form,
        'category': category
    }
    return render(request, 'rango/add_page.html', context_dict)


# class UserRegisterView(generic.CreateView):
#     form_class = UserForm
#     template_name = 'rango/register.html'


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                profile.save()
                registered = True
            else:
                print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
                  )


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))
