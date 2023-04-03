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
        if 'page' in request.GET:
            params["page"] = request.GET['page']
        if 'page_size' in request.GET:
            params["page_size"] = request.GET['page_size']
        if 'fields' in request.GET:
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
