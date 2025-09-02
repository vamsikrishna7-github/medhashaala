from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.serializers import Serializer, CharField, ValidationError
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class EmailOrPhoneLoginSerializer(Serializer):
    email = CharField(required=False, allow_blank=True)
    phone = CharField(required=False, allow_blank=True)
    password = CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '').strip()
        phone = attrs.get('phone', '').strip()
        password = attrs.get('password')

        if not email and not phone:
            raise ValidationError('Either email or phone must be provided')

        try:
            if email:
                user = User.objects.get(email=email)
            else:
                user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise ValidationError('Invalid credentials')

        if not user.check_password(password):
            raise ValidationError('Invalid credentials')

        if not getattr(user, 'is_active', True):
            raise ValidationError('User account is disabled')

        attrs['user'] = user
        return attrs


class CustomTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        serializer = EmailOrPhoneLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': str(user.id),
                'email': user.email,
                'phone': user.phone,
                'name': user.name,
                'role': user.role,
                'subscription_plan': {
                    'id': user.subscription_plan.id if user.subscription_plan else None,
                    'name': user.subscription_plan_name,
                    'features': user.subscription_plan_features,
                } if user.subscription_plan else None,
                'subscription_plan_name': user.subscription_plan_name,
                'enabled_features': user.enabled_features,
            },
        }
        return Response(data, status=status.HTTP_200_OK)

# Create your views here.
