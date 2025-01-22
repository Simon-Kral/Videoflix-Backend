from rest_framework import serializers
from videoflix import settings
from ..models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        """
        Validates the registration data, ensuring that:
        - The passwords match
        """

        pw = attrs.get('password')
        repeated_password = attrs.get('repeated_password')

        if pw != repeated_password:
            raise serializers.ValidationError('passwords don\'t match.')

        return attrs

    def create(self, validated_data):
        """
        Creates a new user account using the validated data, 
        including setting the password and saving the account.
        """

        account = self.Meta.model(email=validated_data['email'])
        account.set_password(self.validated_data['password'])
        account.save()

        return account


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login. Validates the email address and password for authentication.
    """
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, attrs):
        """
        Validates that the username exists and the password is correct.
        """

        email = attrs.get('email')
        password = attrs.get('password')

        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('user not found.')

        self.user = CustomUser.objects.get(email=email)

        if not self.user.check_password(password):
            raise serializers.ValidationError('wrong password.')

        return self.user

    def create(self, validated_data):
        """
        Returns the authenticated user after successful login.
        """

        return self.user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    Serializes the fields 'id', 'email', 'first_name', and 'last_name' for user data.
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']
