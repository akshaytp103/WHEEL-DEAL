from django.shortcuts import render
from rest_framework.views import APIView
from accounts.serializers import AccountSerializer
from rest_framework.response import Response
from accounts.models import Account
from rest_framework.exceptions import APIException,AuthenticationFailed
from rest_framework.response import Response



# Create your views here.

class RegisternewView(APIView):

    def post(self,request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):

    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = Account.objects.filter(email=email).first()

        if user is None:
            raise APIException('User not found')

        if not user.check_password(password):
            raise APIException('Incorrect password')
        response = Response()


        return response

class UserView(APIView):

    def get(self,request):
        user = Account.objects.filter(id=id).first()
        # raise AuthenticationFailed('Not authenticated')
        return Response(AccountSerializer(user).data)

class LogoutView(APIView): 

    def post(self, _):

        response = Response()
        response.delete_cookie(key='RefreshToken')   
        response.data = {
            'message' : 'Logout success'
        }

        return response