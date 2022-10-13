from rest_framework.views import APIView
from .serializers import AccountSerializer
from rest_framework.response import Response
from rest_framework.exceptions import APIException,AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from .models import Account
from .authentication import create_access_token,create_refresh_token,decode_refresh_token,decode_access_token

# Create your views here.
class RegisterView(APIView):
  
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

        access_token  = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
         
        response = Response()

        response.set_cookie(key='RefreshToken', value=refresh_token, httponly=True)

        response.data = {
            'token' : access_token
        }

        return response

class UserView(APIView):

    def get(self,request):
        auth = get_authorization_header(request).split()
        print('test2')
        if auth and len(auth) == 2:
            print(auth[1])
            token = auth[1].decode('utf-8')
            id=decode_access_token(token)

            user = Account.objects.filter(id=id).first()

            return Response(AccountSerializer(user).data)

        raise AuthenticationFailed('Not authenticated')

class RefreshToken(APIView):
    def post(self,request):
        refresh_token = request.COOKIES.get('RefreshToken')
        id=decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'token' : access_token
        }) 

class LogoutView(APIView): 

    def post(self, _):

        response = Response()
        response.delete_cookie(key='RefreshToken')   
        response.data = {
            'message' : 'Logout success'
        }

        return response
