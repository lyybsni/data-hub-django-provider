import json
import os
from django.forms.models import model_to_dict

import requests

from datahubApplicantService.demo.models import Applicant


def export_data_to_data_hub(from_date):
    if from_date is not None:
        new_data = Applicant.objects.filter(update_date__gte=from_date)
    else:
        new_data = Applicant.objects.all()

    data = []

    for item in list(new_data):
        data.append(model_to_dict(item))

    url = 'http://localhost:10086/data-ingest/raw?target=applicant'

    f = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), './mapping_applicant.json'))
    schema = json.load(f)
    raw_body = {'data': data, 'schema': schema['Applicant']}
    body = json.dumps(raw_body, default=str)
    print(body)

    requests.post(url=url, json=json.loads(body))
    f.close()
