import requests
import json
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status


def github_auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        if 'github' not in request.path:
            github_token = request.headers.get('authorization')
            if not github_token:
                return JsonResponse({'error': 'Token is required to perform this action'},
                                    status=status.HTTP_403_FORBIDDEN)
            if 'Bearer' not in github_token:
                return JsonResponse({'error': 'add "Bearer" for token'}, status=status.HTTP_400_BAD_REQUEST)

        response = get_response(request)

        return response

    return middleware
