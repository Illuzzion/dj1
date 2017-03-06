from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from .models import Category, Page


# Create your views here.
def index(request):
    # return HttpResponse('Rango says hey there partner!<br><a href="/rango/about/">about page</a>')
    # return render(request, 'rango/index.html', {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"})
    category_list = Category.objects.order_by('-likes')[:5]
    most_viewed_pages = Page.objects.order_by('-views')[:5]

    context_dict = {
        'categories': category_list,
        'most_viewed_pages': most_viewed_pages
    }
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
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
