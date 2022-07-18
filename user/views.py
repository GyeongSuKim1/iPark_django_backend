import re
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

from user.serializers import UserSerializer

from user.models import User as UserModel


class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    
    # 회원가입
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 회원정보 수정
    def put(self, request):
        user = UserModel.objects.get(id=request.user.id)
        
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 회원탈퇴
    def delete(self, request):
        user = request.user
        
        if user:
            user.delete()
            return Response({"message": "회원탈퇴 성공"}, status=status.HTTP_200_OK)
        
        return Response({"message": "회원탈퇴 실패"}, status=status.HTTP_400_BAD_REQUEST)
    
    
class FindUserInfoView(APIView):
    # 아이디 찾기
    def post(self, request):
        correct_email = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        correct_phone = re.compile("\d{3}-\d{4}-\d{4}")
        
        email_input = correct_email.match(request.data["email"])
        phone_input = correct_phone.match(request.data["phone"])
        
        if email_input == None or phone_input == None:
            return Response({"message": "이메일 혹은 핸드폰 번호 양식이 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                searched_username = UserModel.objects.get(Q(email=request.data["email"]) & Q(phone=request.data["phone"])).username
                if searched_username:
                    return Response({"username" : searched_username}, status=status.HTTP_200_OK)
                
            except UserModel.DoesNotExist:
                return Response({"message": "사용자가 존재하지 않습니다"}, status=status.HTTP_404_NOT_FOUND)
        

class AlterPasswordView(APIView):
    # 비밀번호를 변경할 자격이 있는지 확인
    def post(self, request):
        """
        1. 비밀번호를 변경할 사용자의 username, email을 입력받는다.
        2. 해당 값을 통해 비밀번호를 변경할 user를 찾아준다. 
        3. 만약 user가 존재한다면 user 정보를 비밀번호 수정 페이지에서도 알 수 있도록 넘겨준다.
        4. user가 존재하지 않는다면 "존재하지 않는 사용자입니다." 라는 메세지를 반환한다.
        """
        
        correct_email = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        email_input = correct_email.match(request.data["email"])
        
        if request.data["username"] == "" or request.data["email"] == "":
            return Response({"message": "아이디 또는 이메일 값을 제대로 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if email_input == None:
                print(email_input)
                return Response({"message": "이메일 형식에 맞게 작성해주세요."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try: 
                    user = UserModel.objects.get(Q(username=request.data["username"]) & Q(email=request.data["email"]))
                    if user:
                        user_data = UserSerializer(user)
                        return Response(user_data.data, status=status.HTTP_200_OK)
                
                except UserModel.DoesNotExist:
                    return Response({"message": "존재하지 않는 사용자입니다."}, status=status.HTTP_404_NOT_FOUND)
    
    # 비밀번호 변경
    def put(self, request):
        """
        1. 사용자의 정보를 그대로 가져온다. 
        2. 새롭게 세팅할 비밀번호와 중복 확인용 비밀번호를 받는다. 
        3. 이 두 비밀번호가 정규표현식을 통과하고 일치한다면, UserSerializer에 request.data를 보내 custom updator를 통해 비밀번호를 update해준다.
        """
        
        correct_password = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
        
        if request.data["new_password"] == "" or request.data["rewrite_password"] == "":
            return Response({"message": "비밀번호를 제대로 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data["new_password"] == request.data["rewrite_password"]:
                password_input = correct_password.match(request.data["new_password"])
                
                if password_input == None:
                    return Response({"message": "비밀번호를 양식에 맞게 작성해주세요."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = UserModel.objects.get(Q(username=request.data["username"]) & Q(email=request.data["email"]))
                    user.set_password(request.data["new_password"])
                    user.save()
                
                    return Response({"message": "비밀번호 변경이 완료되었습니다! 다시 로그인해주세요."}, status=status.HTTP_200_OK)
            
            return Response({"message": "두 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
