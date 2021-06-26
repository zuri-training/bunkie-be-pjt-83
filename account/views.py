from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from django.contrib.auth import authenticate,login
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from bunkie.permissions import IsOwnerOrReadOnlys, IsOwner
from .serializers import RegisterSerializer,ChooseUserSerializer,LoginSerializer,LandlordSerializer

from rest_framework import generics, serializers, status, views, permissions
from .serializers import (
    SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer,
    StudentSerializer
)
from rest_framework.response import Response
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.http import HttpResponsePermanentRedirect
import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,authentication_classes, permission_classes 
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Student, LandLord


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


User = get_user_model()


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'account:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)





############################# Choose User registration ########################
# @csrf_exempt
@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        serializer = ChooseUserSerializer(data = request.data)
        if serializer.is_valid():
            if serializer.validated_data.get('choose') == "1":
                return redirect('account:student_register')
            else:
                return redirect('account:landlord_register')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





######################## student register ####################
@csrf_exempt
@api_view(['POST'])
def student_register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            User.objects.create(student_status = True, 
            email = serializer.validated_data.get('email'),
            password = make_password(serializer.validated_data.get('password')))
            return HttpResponse("User created")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


######################## landlord register ####################
@csrf_exempt
@api_view(['POST'])
def landlord_register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            User.objects.create(landlord_status = True, 
            email = serializer.validated_data.get('email'),
            password = make_password(serializer.validated_data.get('password')))
            return HttpResponse("User created")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




######################### complete profile ########################
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['POST'])
def complete_profile(request):
    if request.method == 'POST':
        id_user = request.user
        print(id_user)
        if id_user.student_status == True:
            serializer = StudentSerializer(data = request.data)
            if serializer.is_valid():
                Student.objects.create(
                    user = request.user,
                    full_name = serializer.validated_data.get('full_name'),
                    gender = serializer.validated_data.get('gender'),
                    state_of_origin = serializer.validated_data.get('state_of_origin'),
                    university = serializer.validated_data.get('university'),
                    department = serializer.validated_data.get('department'),
                    facebook_handle = serializer.validated_data.get('facebook_handle'),
                    twitter_handle = serializer.validated_data.get('twitter_handle'),
                    instagram_handle = serializer.validated_data.get('instagram_handle'),
                    personal_interest = serializer.validated_data.get('personal_interest')
                )
                data = {
                    'status': 'OK',
                    'info':'student profile updated'
                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                ############################# Landlord complete profile #################333
        elif id_user.landlord_status == True:
            serializer = LandlordSerializer(data = request.data)
            if serializer.is_valid():
                LandLord.objects.create(
                    user = request.user,
                    first_name = serializer.validated_data.get('first_name'),
                    last_name = serializer.validated_data.get('last_name'),
                    address = serializer.validated_data.get('address'),
                    gender = serializer.validated_data.get('gender')
                    
                )
                data = {
                    'status': 'OK',
                    'info':'Lanlord profile updated'
                }
                return Response(data, status=status.HTTP_201_CREATED)

        else:
            data = {
                'info':'you\'re not a student'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)



########################################## Login View #############################
@api_view(['POST'])
def login_view(request):
    if request.method=='POST':
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = authenticate(request, email = serializer.validated_data.get('email'), password=serializer.validated_data.get('password'))
            if user is not None:
                login(request,user)
                data = {
                    'info': 'login successful'
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'info': 'email or password not correct'
                }
                return Response(data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

