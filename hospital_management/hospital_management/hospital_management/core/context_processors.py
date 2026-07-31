from django.conf import settings

def hospital_info(request):
    return {
        'hospital_name': settings.HOSPITAL_CONFIG['NAME'],
        'hospital_address': settings.HOSPITAL_CONFIG['ADDRESS'],
        'hospital_phone': settings.HOSPITAL_CONFIG['PHONE'],
        'hospital_email': settings.HOSPITAL_CONFIG['EMAIL'],
    }