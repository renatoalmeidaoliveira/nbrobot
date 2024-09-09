from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'nb_robot'

router = NetBoxRouter()


urlpatterns = router.urls