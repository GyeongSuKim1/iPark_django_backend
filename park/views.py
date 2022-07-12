from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from park.models import Park as ParkModel
from park.models import ParkComment as ParkCommentModel

from park.serializers import ParkDetailSerializer
from park.serializers import ParkCommentSerializer


class ParkView(APIView):
    # 공원 상세 정보 조회
    def get(self, request, park_id):
        park = ParkModel.objects.get(id=park_id)
        serialized_data = ParkDetailSerializer(park).data
        
        return Response(serialized_data, status=status.HTTP_200_OK)
    

# 공원 상세 페이지의 댓글창    
class ParkCommentView(APIView):
    # 댓글 작성
    def post(self, request, park_id):
        park = ParkModel.objects.get(id=park_id)
        
        data = {
            "user" : request.user.id,
            "park" : park.id,
            "comment" : request.data["comment"]
        }
        
        comment_serializer = ParkCommentSerializer(data=data)

        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        
        return Response({"message" : "댓글 작성이 실패되었습니다"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 댓글 수정
    def put(self, request, park_id, comment_id):
        comment = ParkCommentModel.objects.get(id=comment_id)
        
        comment_serializer = ParkCommentSerializer(comment, data=request.data, partial=True)

        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        
        return Response({"message" : "댓글 수정이 실패되었습니다"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 댓글 삭제
    def delete(self, request, park_id, comment_id):
        comment = ParkCommentModel.objects.get(id=comment_id)
        comment.delete()
        
        return Response({"message" : "해당 댓글이 삭제되었습니다"}, status=status.HTTP_200_OK)