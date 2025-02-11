from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("collect-user-data/", views.collect_user_data, name="collect_user_data"),
    path(
        "add-test-results/<int:user_id>/",
        views.add_test_results,
        name="add_test_results",
    ),
    path(
        "choose-transmission/<int:user_id>/",
        views.choose_transmission,
        name="choose_transmission",
    ),
    path("generate-pdf/<int:user_id>/", views.generate_pdf, name="generate_pdf"),
    path("users/", views.user_data_list, name="user_data_list"),
    path("users/<int:user_id>/", views.user_detail, name="user_detail"),
    path("generate-all-pdfs/", views.generate_all_pdfs, name="generate_all_pdfs"),
    path("user/<int:user_id>/delete/", views.delete_user, name="delete_user"),
    path("user/<int:user_id>/update/", views.update_user, name="update_user"),
]
