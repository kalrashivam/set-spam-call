from rest_framework.routers import DefaultRouter
from .views import ContactView

router = DefaultRouter()
router.register(r'contact', ContactView, base_name='contact')
urlpatterns = router.urls
