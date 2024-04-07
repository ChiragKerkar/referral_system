from rest_framework import serializers
from .models import User, Referral

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'referral_code', 'registration_timestamp']

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ['referrer', 'referred_user', 'timestamp']