from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from slugify import slugify
from .forms import ProfileModelForm
from blog.models import BlogPost


@login_required(login_url="user:login_view")
def user_fav_view(request):
    ids = request.user.userpostfav_set.filter(is_deleted=False).values_list("post_id", flat=True).order_by("-at_updated")
    context = dict(
        title="Favorilerim",
        favs=BlogPost.objects.filter(id__in=ids, is_active=True)

    )
    return render(request, "blog/post_list.html", context)


@login_required(login_url="user:login_view")
def profile_edit_view(request):
    user = request.user
    initial_data = dict(
        first_name=user.first_name,
        last_name=user.last_name,
    )
    title = "Profil Düzenle"
    form = ProfileModelForm(instance=user.profile, initial=initial_data)
    if request.method == "POST":
        form = ProfileModelForm(
            request.POST or None,
            request.FILES or None,
            instance=user.profile
        )
        if form.is_valid():
            f = form.save(commit=False)
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.save()
            f.save()
            messages.success(request, "Profiliniz Güncellendi..")
            return redirect("user:profile_edit_view")

    context = dict(
        title=title,
        form=form
    )
    return render(request, "common_component/form.html", context)


def logout_view(request):
    messages.info(request, "Oturum kapatıldı")
    logout(request)
    return redirect("/")


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, f"Hi {request.user.username}, You are already logged in")
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if len(username) < 3 or len(password) < 4 :
            messages.warning(request, "Usename 3, password 4 karakterden az olamaz")
            return redirect("user_profile:login_view")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Hi! {}, Login succesful".format(request.user.username))
            return redirect("page:home_view")
        context = dict()
        messages.error(request, "Parola veya Username hatalı!")
        return render(request, "user_profile/login.html", context)

    context = dict()
    return render(request, "user_profile/login.html", context)


def register_view(request):
    context = dict()
    if request.method == "POST":
        post_info = request.POST
        first_name = post_info.get("first_name")
        last_name = post_info.get("last_name")
        username = post_info.get("username")
        email = post_info.get("email")
        email_confirm = post_info.get("email_confirm")
        password = post_info.get("password")
        re_password = post_info.get("re_password")
        instagram = post_info.get("instagram")

        if email != email_confirm:
            messages.warning(request, "Email adresleri eşleşmiyor!")
            redirect("user_profile:register_view")
        elif password != re_password:
            messages.warning(request, "Parolalar eşleşmiyor!")
            redirect("user_profile:register_view")
        elif len(username) < 3 or len(password) < 3 or len(first_name) < 3 or len(last_name) < 3:
            messages.warning(request, "3 karakterden kısa alanlar var")
            redirect("user_profile:register_view")

        user, created = User.objects.get_or_create(
            username=username,
            email = email,
            first_name = first_name,
            last_name = last_name,
        )

        if not created:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Daha önce kayıt oldunuz.. Anasayfa gidiyonuz...")
                return redirect("page:home_view")
            messages.warning(request, f"{username} Kullanıcı adı sistemde kayıtlı. Giriş Sayfasına yönlendiriliyorsunuz. ")
            return redirect("user_profile:login_view")

        user.set_password(password)
        user.save()
        Profile.objects.get_or_create(
            user=user,
            slug=slugify(username),
            instagram=instagram
            )
        user_login = authenticate(request, username=username, password=password)
        login(request, user_login)
        messages.success(request, "Kayıt başarılı.. Anasayfa gidiyonuz...")
        return redirect("page:home_view")

    return render(request, "user_profile/register.html", context)
