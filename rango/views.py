from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from rango.models import Category
from rango.models import Page
from django.http import HttpResponse,HttpResponseRedirect
from rango.form import CategoryForm,PageForm,UserProfile,UserForm,UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.template.defaultfilters import slugify

def category(request, id_number):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}


    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(id=id_number)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.sl
        # Don't do anything - the template displays the "no category" message for us.
        pass
        # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)

    pages = Page.objects.filter(category=category).order_by('-views')


def index(request):


    # Consulta o banco de dados para uma lista de TODAS as categorias atualmente armazenadas.
    # Ordene as categorias por no. gosta em ordem decrescente.
    # Recupere somente os 5 primeiros - ou todos, se menores que 5.
    # Coloque a lista em nosso dicionário context_dict que será passado para o mecanismo de templates.
    category_list = Category.objects.all()
    category_list = Category.objects.order_by('-curtidas')
    context_dict = {'categories': category_list}
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, we default to zero and cast that.
    visits = int(request.COOKIES.get('visits', '1'))

    reset_last_visit_time = False
    response = render(request, 'rango/index.html', context_dict)
    # Does the cookie last_visit exist?
    if 'last_visit' in request.COOKIES:
        # Yes it does! Get the cookie's value.
        last_visit = request.COOKIES['last_visit']
        # Cast the value to a Python date/time object.
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        # If it's been more than a day since the last visit...
        if (datetime.now() - last_visit_time).seconds > 3:
            visits = visits + 1
            # ...and flag that the cookie last visit needs to be updated
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so flag that it should be set.
        reset_last_visit_time = True

        context_dict['visits'] = visits

        # Obtain our Response object early so we can add cookie information.
        response = render(request, 'rango/index.html', context_dict)

    if reset_last_visit_time:
        response.set_cookie('last_visit', datetime.now())
        response.set_cookie('visits', visits)

    # Return response back to the user, updating any cookies that need changed.
    return response
    # Render the response and send it back!
    return render(request, 'rango/index.html', context_dict)


def base(request):


    # Consulta o banco de dados para uma lista de TODAS as categorias atualmente armazenadas.
    # Ordene as categorias por no. gosta em ordem decrescente.
    # Recupere somente os 5 primeiros - ou todos, se menores que 5.
    # Coloque a lista em nosso dicionário context_dict que será passado para o mecanismo de templates.
    category_list = Category.objects.order_by('-curtidas')
    context_dict = {'categories': category_list}

    # Render the response and send it back!
    return render(request, 'rango/base.html', context_dict)

def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print (form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})



def add_page(request):



    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():

                page = form.save(commit=False)
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request)
        else:
            print (form.errors)
    else:
        form = PageForm()

    context_dict = {'form':form}

    return render(request, 'rango/add_page.html', context_dict)

# validação do usuário

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors), profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
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
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}").format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})

    # Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.

    return HttpResponseRedirect('/')

def about(request):
    return render(request,'rango/about.html')




"""
def search(request):
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Execute nossa função Bing para obter a lista de resultados!

            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})
"""
def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)