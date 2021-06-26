from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
User = get_user_model()


from .models import Student,LandLord


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


######################### Choose User serializer ###########################
class ChooseUserSerializer(serializers.Serializer):
    choose = serializers.CharField(max_length = 4)

################ register serializer #######################
class  RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 500)
    class Meta:
        model = User
        fields = ['email','phone','address','password']

        def save(self, commit=True):
            user = super(RegisterSerializer, self).save(commit=False)
            user.make_password(self.validated_data["password"])
            if commit:
                user.save()
            return user



######################## Student serializer #####################
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['full_name','gender','state_of_origin','university','facebook_handle','personal_interest','instagram_handle','department','twitter_handle']


############## Login serializer ####################
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length = 500)
    password = serializers.CharField(max_length = 500)


################## Landlord Serializer ###############
class LandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandLord
        fields = ['first_name','last_name','address','gender']
