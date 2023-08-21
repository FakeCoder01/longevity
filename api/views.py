from rest_framework import (
    permissions,
    status,
    views
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account
from .serializers import (
    AccountSerializer, 
    AccountCreateSerializer, 
    AccountLoginSerializer
)
from .tasks import send_otp_email
import logging, random, string, datetime
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.


logger = logging.getLogger(__name__)

class EmailOTPSendView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def generate_otp(self, length=6):
        return ''.join(random.choices(string.digits, k=length))

    def save_otp_to_account(self, email, otp_hash):
        account = Account.objects.filter(email=email).update(otp_hash=otp_hash)
        return

    def generate_otp_hash(self, otp):
        return hash(otp)

    def post(self, request):
        try:
            email = request.data.get("email")
            if email is None or not Account.objects.filter(email=email).exists():
                return Response({'message' : 'Email not vaild'}, status=status.HTTP_404_NOT_FOUND)
            
            otp = self.generate_otp()
            otp_hash = self.generate_otp_hash(otp)
            self.save_otp_to_account(email, otp_hash)
            send_otp_email.delay(email, otp)
            return Response({"message": "OTP Sent"}, status=status.HTTP_200_OK)
        except Exception as err:
            logger.error(err)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmailOTPLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def verify_otp(self, account, otp):
        return account.otp_hash == str(hash(otp))
    
    def post(self, request):
        try:
            serializer = AccountLoginSerializer(data=request.data)
            if serializer.is_valid():
                email = request.data.get('email')
                otp = request.data.get('otp')
                account = get_object_or_404(Account, email=email)
                if self.verify_otp(account, otp):
                    refresh = RefreshToken.for_user(account)
                    account.last_login = datetime.datetime.now()
                    account.otp_hash = ""
                    account.save()
                    return Response({'access' : str(refresh.access_token), 'refresh' : str(refresh)}, status=status.HTTP_200_OK)
                else:
                    return Response({'message' : 'otp mismatch'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message' : 'email & otp required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            logger.error(err)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AccountListCreateView(views.APIView):
    
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def get(self, request):
        try:
            accounts = Account.objects.all()
            serializer = AccountSerializer(accounts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            logger.error(err)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = AccountCreateSerializer(data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            logger.error(err)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AccountRetrieveUpdateDeleteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def get(self, request, id:str):
        try:
            account = get_object_or_404(Account, id=id)
            if account is None:
                return Response({'message' : 'account not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            logger.error(err)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id:str):
        try:
            account = get_object_or_404(Account, id=id)
            if account is None:
                return Response({'message' : 'account not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = AccountSerializer(account, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            logger.error(err)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id:str):
        try:
            account = get_object_or_404(Account, id=id)
            if account is None:
                return Response({'message' : 'account not found'}, status=status.HTTP_404_NOT_FOUND)
            account.delete()
            return Response({'message' : 'account deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            logger.error(err)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

