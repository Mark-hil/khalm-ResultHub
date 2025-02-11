from django.db import models


class UserData(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    user_class = models.CharField(max_length=50)
    lab_serial = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class TestResult(models.Model):
    user = models.ForeignKey(
        UserData, on_delete=models.CASCADE, related_name="test_results"
    )
    test_name = models.CharField(max_length=100)
    result = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.test_name} - {self.result}"
