from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.http import Http404
from .models import Movie,Myrating
from django.contrib import messages
from .forms import UserForm
from django.db.models import Case, When
from .recommendation import Myrecommend
import numpy as np 
import pandas as pd


# for recommendation
def recommend(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404

    # Lấy dữ liệu đánh giá
    df = pd.DataFrame(list(Myrating.objects.all().values()))
    current_user_id = request.user.id

    # Nếu user chưa có rating nào, thêm mặc định
    if df.empty or not Myrating.objects.filter(user=request.user).exists():
        movie = Movie.objects.first()
        if movie:
            Myrating.objects.get_or_create(user=request.user, movie=movie, rating=0)
        messages.info(request, "Bạn chưa có dữ liệu đánh giá. Hãy đánh giá vài phim để hệ thống học!")
        return redirect("index")

    # 🔹 Lấy ma trận dự đoán + mapping
    prediction_matrix, Ymean, user_mapping, movie_mapping = Myrecommend()

    # Kiểm tra user có trong mô hình chưa
    if current_user_id not in user_mapping:
        messages.error(
            request,
            "Không thể tạo gợi ý vì tài khoản của bạn chưa có dữ liệu trong mô hình. "
            "Hãy đánh giá thêm một vài phim!"
        )
        return redirect("index")

    # Lấy chỉ số user trong ma trận
    user_idx = user_mapping[current_user_id]
    my_predictions = prediction_matrix[:, user_idx] + Ymean.flatten()
    pred_idxs_sorted = np.argsort(my_predictions)[::-1]

    # Lấy id phim theo mapping ngược
    reverse_movie_map = {v: k for k, v in movie_mapping.items()}
    movie_ids_sorted = [reverse_movie_map[i] for i in pred_idxs_sorted]

    # Lọc và hiển thị top phim
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(movie_ids_sorted)])
    movie_list = list(Movie.objects.filter(id__in=movie_ids_sorted).order_by(preserved)[:10])

    if not movie_list:
        messages.info(request, "Hiện chưa có gợi ý phù hợp. Hãy thử đánh giá thêm vài phim!")
        return redirect("index")

    return render(request, 'web/recommend.html', {'movie_list': movie_list})

# List view
def index(request):
	movies = Movie.objects.all()
	query  = request.GET.get('q')
	if query:
		movies = Movie.objects.filter(Q(title__icontains=query)).distinct()
		return render(request,'web/list.html',{'movies':movies})
	return render(request,'web/list.html',{'movies':movies})


# detail view
def detail(request,movie_id):
	if not request.user.is_authenticated:
		return redirect("login")
	if not request.user.is_active:
		raise Http404
	movies = get_object_or_404(Movie,id=movie_id)
	#for rating
	if request.method == "POST":
		rate = request.POST['rating']
		ratingObject = Myrating()
		ratingObject.user   = request.user
		ratingObject.movie  = movies
		ratingObject.rating = rate
		ratingObject.save()
		messages.success(request,"Đánh giá của bạn đã được ghi nhận!")
		return redirect("index")
	return render(request,'web/detail.html',{'movies':movies})


# Register user
def signUp(request):
	form =UserForm(request.POST or None)
	if form.is_valid():
		user      = form.save(commit=False)
		username  =	form.cleaned_data['username']
		password  = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect("index")
	context ={
		'form':form
	}
	return render(request,'web/signUp.html',context)				


# Login User
def Login(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		user     = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect("index")
			else:
				return render(request,'web/login.html',{'error_message':'Your account disable'})
		else:
			return render(request,'web/login.html',{'error_message': 'Invalid Login'})
	return render(request,'web/login.html')

#Logout user
def Logout(request):
	logout(request)
	return redirect("login")




