from rest_framework.routers import DefaultRouter
from .views import CreateUserView, UserView

router = DefaultRouter()
router.register(r'me', UserView, base_name='me')
router.register(r'signup', CreateUserView, base_name='create')
urlpatterns = router.urls
