from django.urls import path
from socialapp import views


urlpatterns = [
   
    path('signup/',views.SignupView.as_view()),
    path('token/',views.ObtainAuthToken.as_view()),
    path('posts/',views.PostCreateListView.as_view()),
    path('posts/<int:pk>/',views.PostUpdateRetrieveDestroyView.as_view()),
    path('posts/<int:pk>/like/',views.PostLikeView.as_view()),
    path('posts/<int:pk>/comment/',views.PostCommentView.as_view()),
    path('profile/change/',views.UserProfileView.as_view()),
    

    
]