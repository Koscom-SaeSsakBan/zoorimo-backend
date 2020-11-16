from rest_framework import serializers

from zoorimo.app.models import User, Zoorimo, Quiz


class SignInSerializer(serializers.Serializer):
    input_password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    def validate(self, attrs):
        pw = attrs.get('input_password')
        un = attrs.get('username')
        u = User.objects.filter(username=un)
        if not u.exists():
            raise serializers.ValidationError({"email": "user is not existed"})
        u = u.first()
        r = u.check_password(pw)
        if not r:
            raise serializers.ValidationError({"input_password": "password is not matched"})
        return attrs


class SignUpSerializer(serializers.ModelSerializer):
    input_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'name',
            'input_password'
        ]

    def create(self, validated_data):
        print(validated_data)
        u = User()
        u.email = validated_data.get('email')
        u.username = validated_data.get('username')
        u.name = validated_data.get('name')

        input_password = validated_data.get('input_password')
        u.set_password(input_password)
        u.save()
        return u


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'name',
        ]


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ZoorimoInfoSerializer(serializers.ModelSerializer):
    # user = UserInfoSerializer(read_only=True)
    class Meta:
        model = Zoorimo
        fields = '__all__'


class QuizInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
