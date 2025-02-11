from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import UserData, TestResult
from .forms import UserDataForm, TestResultForm
import os


def user_data_list(request):
    users = UserData.objects.all()
    return render(request, "data_handler/user_data_list.html", {"users": users})


def user_detail(request, user_id):
    user = get_object_or_404(UserData, id=user_id)
    return render(request, "data_handler/user_detail.html", {"user": user})


def collect_user_data(request):
    if request.method == "POST":
        user_form = UserDataForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()

            # Get test results dynamically from POST request
            test_names = request.POST.getlist("test_name[]")
            results = request.POST.getlist("result[]")

            # Save each test result
            for test_name, result in zip(test_names, results):
                if test_name and result:  # Ensure fields are not empty
                    TestResult.objects.create(
                        user=user, test_name=test_name, result=result
                    )

            return redirect("user_data_list")
    else:
        user_form = UserDataForm()

    return render(
        request, "data_handler/collect_user_data.html", {"user_form": user_form}
    )


def add_test_results(request, user_id):
    user = get_object_or_404(UserData, id=user_id)

    if request.method == "POST":
        form = TestResultForm(request.POST)
        if form.is_valid():
            test_result = form.save(commit=False)
            test_result.user = user
            test_result.save()
            return redirect("choose_transmission", user_id=user.id)
    else:
        form = TestResultForm()

    return render(
        request, "data_handler/add_test_results.html", {"form": form, "user": user}
    )


def choose_transmission(request, user_id):
    return render(
        request, "data_handler/choose_transmission.html", {"user_id": user_id}
    )


def generate_pdf(request, user_id):
    user = get_object_or_404(UserData, id=user_id)
    test_results = TestResult.objects.filter(user=user)

    letterhead_url = request.build_absolute_uri("/static/images/letterhead.jpg")

    html_content = render_to_string(
        "data_handler/report_template.html",
        {"user": user, "test_results": test_results, "letterhead_url": letterhead_url},
    )

    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="lab_report.pdf"'
    return response


from django.shortcuts import render
from django.http import HttpResponse
from weasyprint import HTML
from .models import UserData, TestResult


def generate_all_pdfs(request):
    users = UserData.objects.all()
    letterhead_url = request.build_absolute_uri("/static/images/letterhead.jpg")

    html_content = render_to_string(
        "data_handler/all_reports_template.html",
        {"users": users, "letterhead_url": letterhead_url},
    )

    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="all_lab_reports.pdf"'
    return response


def landing_page(request):
    # Fetch statistics for the dashboard
    total_users = UserData.objects.count()
    total_tests = TestResult.objects.count()
    total_reports = total_tests  # Assuming each test generates a report

    context = {
        "total_users": total_users,
        "total_tests": total_tests,
        "total_reports": total_reports,
    }

    return render(request, "data_handler/landing.html", context)


from django.shortcuts import render
from .models import UserData, TestResult
from collections import Counter


def dashboard(request):
    # General Statistics
    total_users = UserData.objects.count()
    total_tests = TestResult.objects.count()
    total_reports = total_tests  # Assuming each test generates a report

    # Gender Distribution
    gender_counts = UserData.objects.values_list("sex", flat=True)
    gender_data = dict(Counter(gender_counts))

    # Age Distribution
    age_groups = {
        "Under 18": UserData.objects.filter(age__lt=18).count(),
        "18-30": UserData.objects.filter(age__gte=18, age__lte=30).count(),
        "31-50": UserData.objects.filter(age__gte=31, age__lte=50).count(),
        "Above 50": UserData.objects.filter(age__gt=50).count(),
    }

    # User distribution by class
    user_classes = UserData.objects.values_list("user_class", flat=True)
    class_counts = dict(Counter(user_classes))

    # Most common tests
    test_names = TestResult.objects.values_list("test_name", flat=True)
    test_counts = dict(Counter(test_names))

    # Recent users & test results
    recent_users = UserData.objects.order_by("-id")[:5]
    recent_tests = TestResult.objects.order_by("-id")[:5]

    # Prepare data for Chart.js
    context = {
        "total_users": total_users,
        "total_tests": total_tests,
        "total_reports": total_reports,
        "gender_labels": list(gender_data.keys()),
        "gender_values": list(gender_data.values()),
        "age_labels": list(age_groups.keys()),
        "age_values": list(age_groups.values()),
        "class_labels": list(class_counts.keys()),
        "class_values": list(class_counts.values()),
        "test_labels": list(test_counts.keys()),
        "test_values": list(test_counts.values()),
        "recent_users": recent_users,
        "recent_tests": recent_tests,
    }

    return render(request, "data_handler/dashboard.html", context)


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

# from .models import user


def delete_user(request, user_id):
    user = get_object_or_404(UserData, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect("user_data_list")


from django.shortcuts import render, get_object_or_404, redirect
from .models import UserData, TestResult
from .forms import UserDataForm


def update_user(request, user_id):
    user = get_object_or_404(UserData, id=user_id)
    test_results = TestResult.objects.filter(user=user)  # Fetch user's test results

    if request.method == "POST":
        user_form = UserDataForm(request.POST, instance=user)

        if user_form.is_valid():
            user_form.save()

            # Clear existing test results and add new ones
            TestResult.objects.filter(user=user).delete()
            test_names = request.POST.getlist("test_name[]")
            results = request.POST.getlist("result[]")

            for test_name, result in zip(test_names, results):
                if test_name and result:
                    TestResult.objects.create(
                        user=user, test_name=test_name, result=result
                    )

            return redirect("user_detail", user_id=user.id)

    else:
        user_form = UserDataForm(instance=user)

    return render(
        request,
        "data_handler/update_user.html",
        {"user_form": user_form, "test_results": test_results, "user": user},
    )
