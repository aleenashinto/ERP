from rest_framework.routers import DefaultRouter
from .views import LeaveRequestViewSet, LeaveBalanceViewSet

router = DefaultRouter()
router.register("balance", LeaveBalanceViewSet, basename="leave-balance")
router.register("", LeaveRequestViewSet, basename="leave")

urlpatterns = router.urls
