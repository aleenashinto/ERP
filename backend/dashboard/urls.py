from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DashboardSummaryView, AnnouncementViewSet

router = DefaultRouter()
router.register("announcements", AnnouncementViewSet, basename="announcement")

urlpatterns = [
    path("summary/", DashboardSummaryView.as_view(), name="dashboard-summary"),
] + router.urls
