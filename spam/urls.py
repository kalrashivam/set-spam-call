from rest_framework.routers import DefaultRouter
from .views import SpamView

router = DefaultRouter()
router.register(r'spam', SpamView, base_name='spam')
urlpatterns = router.urls
