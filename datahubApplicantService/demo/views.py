import json
import string
import random

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Applicant
from .services.export_into_data_hub import export_data_to_data_hub


def display_applicants(request):
    applicants = Applicant.objects.all()
    content = {"applicants": applicants}
    return render(request, "applicants/applicants.html", content)


@csrf_exempt
def create_applicant(request):
    method = request.method
    body = json.loads(request.body.decode('utf-8'), object_hook=lambda d: Applicant(**d))
    if method == "POST":
        print(body)
        Applicant.save(body)
        return render(request, "applicants/applicants.html", {})


def applicant(request, applicant_id):
    result = Applicant.objects.filter(applicant_id=applicant_id)
    return render(request, "applicants/applicants.html", {"applicants": result})


def export_to_data_hub(request, from_date=None):
    export_data_to_data_hub(from_date)
    return render(request, 'applicants/applicants.html', context={"applicants":[]})


def generate_random_applicant(request):
    applicants = []
    print("asd", int(request.GET.get('number')))
    for _ in range(int(request.GET.get('number'))):
        applicant_id = _random_string(10)
        applicant_name = _random_string(int(request.GET.get('size')))
        phone_number = int(random.Random().random() * 1e9)
        graduate_date = '2024-07-15'
        new_applicant = Applicant(applicant_id=applicant_id,
                                  applicant_name=applicant_name,
                                  phone_number=phone_number,
                                  graduate_date=graduate_date)
        applicants.append(new_applicant)

    Applicant.objects.bulk_create(applicants)

    return render(request, "applicants/applicants.html", {"applicants": applicants})


def _random_string(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))