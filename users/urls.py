from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name="logout"),
    path('verify/<str:token>', views.verifyUser, name="verify"),
    path('verify-please/', views.verifyPlease, name="verify-please"),
    re_path(r'^robots\.txt', include('robots.urls')),
    path('', views.index, name='index'),
    path('edit-account/', views.editAccount, name="edit-account"),
    path('create-checkout-session', views.createCheckoutSession, name="create-checkout-session"),
    path('create-profile/', views.newDeveloperOrBusiness, name="create-profile"),
    path('create-developer/', views.createNewDeveloper, name="create-developer"),
    path('edit-developer/', views.editDeveloper, name="edit-developer"),
    path('create-business/', views.createNewBusiness, name="create-business"),
    path('edit-business/', views.editBusiness, name="edit-business"),
    path('about/', views.aboutPage, name='about_page'),
    path('pricing/', views.pricingPage, name='pricing_page'),
    path('developers/', views.developersPage, name='developers_page'),
    path('developer/<str:pk>', views.developerPage, name='developer_page'),
    path('conversations', views.conversationsPage, name='conversations_page'),
    path('conversations/<str:pk>', views.conversationsMessagePage, name='conversations_message'),
    path('conversations/new/<str:pk>', views.conversationsNewPage, name='conversations_new_page'),
    path('conversations/<str:pk>', views.conversationPage, name='conversation_page'),
    path('success/', views.successurl, name='success'),
    path('cancel/', views.cancelurl, name='cancel'),
]
