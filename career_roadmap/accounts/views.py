from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer, 
    ProfileSerializer,
    ProfileUpdateSerializer
)
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Please provide both email and password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authenticate user
        user = authenticate(username=email, password=password)
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, 
                          status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid token'}, 
                          status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ProfileDetailView(APIView):
    """Get or update the current user's profile"""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Get current user's profile"""
        try:
            profile = request.user.profile
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request):
        """Update current user's profile"""
        try:
            profile = request.user.profile
            serializer = ProfileUpdateSerializer(
                profile, 
                data=request.data, 
                partial=True
            )
            
            if serializer.is_valid():
                serializer.save()
                # Return full profile data
                response_serializer = ProfileSerializer(profile)
                return Response(
                    response_serializer.data, 
                    status=status.HTTP_200_OK
                )
            
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def patch(self, request):
        """Partially update current user's profile"""
        return self.put(request)


class AddSkillView(APIView):
    """Add a skill to user's profile"""
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        skill = request.data.get('skill', '').strip()
        
        if not skill:
            return Response(
                {'error': 'Skill name is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profile = request.user.profile
        
        if skill not in profile.skills:
            profile.skills.append(skill)
            profile.save()
            return Response(
                {'message': 'Skill added', 'skills': profile.skills}, 
                status=status.HTTP_200_OK
            )
        
        return Response(
            {'message': 'Skill already exists', 'skills': profile.skills}, 
            status=status.HTTP_200_OK
        )


class RemoveSkillView(APIView):
    """Remove a skill from user's profile"""
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        skill = request.data.get('skill', '').strip()
        
        if not skill:
            return Response(
                {'error': 'Skill name is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profile = request.user.profile
        
        if skill in profile.skills:
            profile.skills.remove(skill)
            profile.save()
            return Response(
                {'message': 'Skill removed', 'skills': profile.skills}, 
                status=status.HTTP_200_OK
            )
        
        return Response(
            {'error': 'Skill not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )