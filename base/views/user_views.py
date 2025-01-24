from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.contrib.auth.models import User
from base.models import UserProfile

from ..permissions import IsOwnerUser


from base.serializers import UserSerializer, UserSerializerWithToken, UserProfileSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.core.exceptions import ValidationError


#for tokens

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k,v  in serializer.items():
            data[k] = v
        
        return data
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# User Registration 
@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        if data['username'] == '':
            username = data['email']
        else:
            username = data['username']

        user = User.objects.create(
            first_name=data['name'],
            username=username,
            email=data['email'],
            password=make_password(data['password'])
        )

        user_profile = UserProfile.objects.create(user=user, user_type=data['user_type'])

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    except ValidationError as e:
        message = {'detail': str(e)}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

# User Profile Update
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    
    data = request.data

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)
    
# User Profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

# To view Owner / Employee Profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEmployeeProfile(request):
    user_profile = request.user.userprofile
    serializer = UserProfileSerializer(user_profile, many=False)
    return Response(serializer.data)

# To update employee profile 
@api_view(['PUT'])
@permission_classes([IsOwnerUser])
def updateEmployeeProfile(request, pk):

    try:
        user_profile = UserProfile.objects.get(pk=int(pk))

        if request.user.userprofile.user_type == 'owner':
          
            user_profile.user_type = request.data.get('user_type')
            if user_profile.restaurant == "":
                user_profile.restaurant = request.user.userprofile.restaurant
            else:
                return Response({'detail': 'User associated with another restaurant'}, status=status.HTTP_403_FORBIDDEN)
            
            user_profile.save()

            serializer = UserProfileSerializer(user_profile, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({'detail': 'You do not have permission to update'}, status=status.HTTP_403_FORBIDDEN)

    except UserProfile.DoesNotExist:
        return Response({'detail': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

# All User details for Admin
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# User details for Admin
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
