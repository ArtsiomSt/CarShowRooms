from rest_framework.exceptions import APIException
from rest_framework import status


class NoSuchObjectException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {"message": "there is no such object"}


class ObjectCanNotBeChanged(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {"message": "this object can't be changed"}
