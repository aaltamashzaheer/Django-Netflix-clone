from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ProfileForm
from .models import Profile,Movie

class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile_list')
        return render(request,"index.html")
    

@method_decorator(login_required,name='dispatch')
class ProfileList(View):
    def get(self, request, *args, **kwargs):
        profiles = request.user.profiles.all()
        context = {
            'profiles':profiles,
        }
        return render(request, 'profileList.html',context)
    

@method_decorator(login_required,name='dispatch')
class ProfileCreate(View):
    def get(self, request, *args, **kwargs):
        form = ProfileForm()
        context = {
            'form':form,
        }
        return render(request, 'profileCreate.html',context)
    
    def post(self, reqeust, *args, **kwargs):
        form = ProfileForm(reqeust.POST or None)

        if form.is_valid():
            # ** used bcz it's form data in dictionary 
            profile = Profile.objects.create(**form.cleaned_data)
            if profile:
                reqeust.user.profiles.add(profile)
                return redirect('profile_list')
        
        context = {
            'form':form,
        }
        
        return render(reqeust, 'profileCreate.html', context)
    
@method_decorator(login_required,name='dispatch')    
class Watch(View):
    def get(self, request,profile_id ,*args, **kwargs):
        try:
            profile = Profile.objects.get(uuid=profile_id)
            movies = Movie.objects.filter(age_limit=profile.age_limit)

            if profile not in request.user.profiles.all():
                return redirect(to='profile_list')
            
            context = {
                'movies':movies
            }
            return render(request, 'movieList.html', context)

        except Profile.DoesNotExist:
            return redirect('profile_List')


@method_decorator(login_required,name='dispatch')
class ShowMovieDetail(View):
    def get(self, request, movie_id ,*args, **kwargs):
        try:
            movie = Movie.objects.get(uuid=movie_id)
            # showmovie = Movie.objects.filter()

            return render(request, 'movieDetail.html', {
                'movie':movie
            })
        except Movie.DoesNotExist:
            return redirect('profileList')


@method_decorator(login_required,name='dispatch')
class ShowMovie(View):
    def get(self, request, movie_id ,*args, **kwargs):
        try:
            movie_object = Movie.objects.get(uuid=movie_id)
            movie = movie_object.videos.values()

            return render(request, 'showMovie.html', {
                'movie':list(movie)
            })
        except Movie.DoesNotExist:
            return redirect('profileList')

