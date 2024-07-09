from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Customizing the response data here
    custom_data = {
        'error': True,
        'message': 'An error occurred.',
        'details': response.data,
        'status_code': response.status_code
    }
    response.data = custom_data

    return response
