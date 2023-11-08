from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateAccount, LoginView, UserProfileView, ChangePassword, ForgotPassword, ResetPassword



router = DefaultRouter()
# router.register('signup', CreateAccount, basename='signup')


urlpatterns = [
    # path('', include(router.urls)),
    path("signup/", CreateAccount.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path('ChangePassword/', ChangePassword.as_view(), name="ChangePassword"),
    path("forgot/", ForgotPassword.as_view(), name="reset"),
    path("reset/<uid>/<token>/", ResetPassword.as_view(), name="reset"),
]
