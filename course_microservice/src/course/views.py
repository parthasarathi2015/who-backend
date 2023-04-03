# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# import requests
# import json
# import jwt
# from config import settings
# from .authservice import CustomTokenAuthentication, authenticate

# @api_view(['GET'])
# @authentication_classes([CustomTokenAuthentication])
# @permission_classes([IsAuthenticated])
# def course_list(request):

#     # url = 'http://localhost:8000/token/'
#     # resp = requests.post(url,data=({'username':"User001","password":"CU@123456"}))
#     # data = json.loads(resp.text)
#     # print("data:",data)
#     # token = None
#     # if "access" in  data:
#     #     token = data["access"]
#     #     t = jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256'])
#     #     print("ttttttt:",t)
#     # else:
#     #     print("invalid credential")
        
    
#     # headers = {'Authorization': 'Token {}'.format(auth_token)}

#     # response = requests.get(url, headers=headers)
#     return Response({"message":"ok"})


# def authenticate_user(request):
#     user = authenticate(request, token='mytoken')
#     return True if user is not None else False



import requests
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from config import settings
import json
# import jwt
from rest_framework.permissions import IsAuthenticated, AllowAny
from course.permission import AuthTokenPermission
from course.authservice import CustomTokenAuthentication

class CourseListView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [AuthTokenPermission]

    def get(self, request):
        params = {}
        if request.GET['page']:
            params["page"] = request.GET['page']
        if request.GET['page_size']:
            params["page_size"] = request.GET['page_size']
        if request.GET['fields']:
            params["fields"] = request.GET['fields']
        re, status_code = self.get_courses(params)
        return Response(re, status=status_code)

    def get_courses(self, params):
        param_list = ""
        for k,v in params.items():
            param_list += f"?{k}={v}" if param_list=='' else f"&{k}={v}"
        filed_list = []
        if "fields" in params:
            filed_list = params["fields"].split(",")

        course_url = settings.COURSES_END_POINT+param_list
        resp = requests.get(course_url)
        status_code = resp.status_code
        resp = json.loads(resp.text)
        result = {}
        result["results"] = []
        result["pagination"] = resp["pagination"] if "pagination" in resp else {}
        if "results" in resp and len(resp["results"])>0:
            for row in resp["results"]:
                data = {}
                if filed_list:
                    for fld in filed_list:
                        data[fld] = row[fld]
                else: data = {k:v for k,v in row.items() }
                if data:
                    result["results"].append(data)
        return result, status_code

# class LoginView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [AllowAny]

#     def post(self, request):

#         token_url = settings.AUTH_END_POINT+'token/'
#         username = request.GET['username']
#         password = request.GET['password']
#         response = requests.post(token_url, data={'username': username, 'password': password})
#         if response.status_code == 200:
#             resp = json.loads(response.text)
#             if "access" in resp:
#                 token = resp['access']
#                 headers = {'Authorization': f'Token {token}'}