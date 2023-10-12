import debug_toolbar
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import (
    ConfirmEmailView,
    ManualConfirmEmailViewSet,
    ChangePasswordViewSet,
    ReportViewSet,
)

from .settings import DEBUG, SHOW_SWAGGER

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

api_v1_urls = (
    [
        path("sellers/", include("sellers.api.v1.urls")),
        path("cars/", include("cars.api.v1.urls")),
        path("customers/", include("customers.api.v1.urls")),
    ],
    "api_v1",
)

token_urls = (
    [
        path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        path(
            "verify-email/<str:token>", ConfirmEmailView.as_view(), name="email_confirm"
        ),
        path(
            "manual-email-verify/",
            ManualConfirmEmailViewSet.as_view({"get": "verify_email"}),
            name="manual_email_confirm",
        ),
        path(
            "send-change-creds/",
            ManualConfirmEmailViewSet.as_view({"get": "creds_change"}),
            name="change_creds",
        ),
        path(
            "forgot-pass/",
            ManualConfirmEmailViewSet.as_view({"post": "forgot_password"}),
            name="forgot_password",
        ),
        path(
            "change-creds/<str:token>",
            ChangePasswordViewSet.as_view({"put": "update", "patch": "partial_update"}),
            name="creds_change",
        ),
    ],
    "tokens",
)

report_urls = (
    [
        path("incomes-expenses/", ReportViewSet.as_view({"get": "turnover_reports"})),
        path("cars-stats/", ReportViewSet.as_view({"get": "car_reports"})),
    ],
    "reports",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_v1_urls)),
    path("auth/", include(token_urls)),
    path("reports/", include(report_urls)),
]

if DEBUG:
    urlpatterns = urlpatterns + [path("__debug__/", include(debug_toolbar.urls))]

if SHOW_SWAGGER:
    urlpatterns = urlpatterns + [
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
