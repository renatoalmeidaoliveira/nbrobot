from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'nb_robot'

router = NetBoxRouter()


router.register('project', views.ProjectViewSet)
router.register('resource', views.ResourceViewSet)
router.register('variable', views.VariableViewSet)

urlpatterns = router.urls