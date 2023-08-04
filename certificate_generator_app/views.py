import uuid
from datetime import date
from django.http import JsonResponse
from django.middleware.csrf import get_token
import json
from .models import Certificate, CertificateDetails

'''The following operations are the request and response engine 
   for the application which recieves request according to the desired operation'''


def generate_certificate(request):
    if request.method == 'POST':
        payload = json.loads(request.body.decode('utf-8'))
        name = payload.get('name')
        course_name = payload.get('course_name')
        certificate_award_date = payload.get('certificate_award_date')
        

        '''Generate a unique ID for the certificate'''

        certificate_id = str(uuid.uuid4()).upper()

        '''Set the certificate generation date to today's date'''
        
        certificate_generation_date = date.today().strftime('%Y-%m-%d')

        ''' creates an object to save the details such as id and date of generation in the database 
            with the help of Foreign Key of certificate id and certificate generated date '''

        cert = Certificate.objects.create(certificate_unique_id = certificate_id, 
                                          certificate_generation_date = certificate_generation_date)


        '''Create a dictionary containing the certificate details'''

        certificate = {
            'name': name,
            'course-name': course_name,
            'certificate_award_date': certificate_award_date,
            'certificate_generation_date': certificate_generation_date,
            'certificate_id': certificate_id,
        }

        ''' creates an object to save all the details of the certificate in the database 
            with the help of Foreign Key of certificate id and certificate generated date '''
        
        certificate_details = CertificateDetails.objects.create(
        certificate_id=cert,
        name= name,
        course_name=course_name,
        certificate_award_date= certificate_award_date 
        )
        certificate_details.save()
        
        return JsonResponse(certificate)

    '''If the request method is not POST, return a 405 Method Not Allowed response'''

    return JsonResponse({'error': 'Method Not Allowed'})


def verify_certificate(request):
    
    payload = json.loads(request.body.decode('utf-8'))
    certificate_generation_date = payload.get('certificate_generation_date')
    certificate_id = payload.get('certificate_id')
    is_valid_certificate = False
    try:
        '''get function to detect the id and the date from the database to validate the certificate'''

        Certificate.objects.get(certificate_unique_id=certificate_id, certificate_generation_date=certificate_generation_date)
        is_valid_certificate = True
    except Exception as e:
        print(f"Some exception occured - {e}")
    return JsonResponse({'is_valid_certificate': is_valid_certificate})


def fetch_certificate(request):
    payload = json.loads(request.body.decode('utf-8'))
    certificate_id = payload.get('certificate_id')
    certificate_generation_date = payload.get('certificate_generation_date')
    try:
        certificate_1 = CertificateDetails.objects.get(certificate_id__certificate_unique_id=certificate_id, certificate_id__certificate_generation_date=certificate_generation_date)

        '''Create a dictionary containing the certificate details'''

        certificate_details = {
                'name': certificate_1.name,
                'course-name': certificate_1.course_name,
                'certificate_award_date': certificate_1.certificate_award_date,
                'certificate_generation_date': certificate_1.certificate_id.certificate_generation_date,
                'certificate_id': certificate_1.certificate_id.certificate_unique_id,
            }
    except CertificateDetails.DoesNotExist:
        return JsonResponse({'error': 'Certificate not found'}) 
    
    return JsonResponse(certificate_details)