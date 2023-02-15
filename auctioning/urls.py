from django.urls import path
from auctioning import views


app_name = 'auctioning'


urlpatterns = [

    # signup page
    path('signup/', views.signup_view, name='signup'),
    # login page
    path('', views.login_view, name='login'),

    path('login/', views.login_view, name='login'),

    path('api/profile', views.profile_view),

    path('api/productsearch', views.api_search),

    path('api/logout', views.logout_view),

    path('api/product', views.product_view),

    path('api/questionsearch', views.question_view),

    path('api/bidview', views.bid_view),

    path('api/postquestion', views.post_question),

    path('api/postanswer', views.post_answer),

    path('api/upload', views.upload_product),

    path('api/test', views.test_api),

]
