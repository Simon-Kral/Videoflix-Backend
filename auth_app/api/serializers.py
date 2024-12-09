from rest_framework import serializers
from videoflix import settings
from ..models import CustomUser

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

        def save(self):
            pw = self.validated_data['password']
            repeated_pw = self.validated_data['repeated_password']

            if pw != repeated_pw:
                raise serializers.ValidationError({'error': 'passwords dont match'})
            
            account = CustomUser(email=self.validated_data['email'])
            account.set_password(pw)
            account.save()
            return account