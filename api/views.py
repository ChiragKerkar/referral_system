from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import User, Referral
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, ReferralSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user_id': user.id,
            'token': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })

class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ReferralsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_referral_code = self.request.user.referral_code
        if user_referral_code:
            return User.objects.filter(referral_code=user_referral_code)
        return []
