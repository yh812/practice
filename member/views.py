import logging
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse
from member.models import Member
from django.utils.dateformat import DateFormat
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)

class MainView(View):
    def get(self, request):
        template = loader.get_template("main.html")
        memid = request.session.get("memid")
        if memid :
            context = {
                "memid" : memid
                }
        else :
            context = {
                }
        return HttpResponse(template.render(context, request))

class MWriteView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    def get(self, request):
        template = loader.get_template("mwrite.html")
        context = {}
        logger.info("mwrite.html")
        return HttpResponse(template.render(context, request))
        
    def post(self, request):
        email = request.POST["email1"] + "@" + request.POST["email2"]
        tel = ""
        tel1 = request.POST["tel1"]
        tel2 = request.POST["tel2"]
        tel3 = request.POST["tel3"]
        if tel1 and tel2 and tel3 :
            tel = tel1 + "-" + tel2 + "-" + tel3
        
        dto = Member(
            id = request.POST["id"],
            passwd = request.POST["passwd"],
            name = request.POST["name"],
            email = email,
            tel = tel,
            depart = request.POST["depart"],
            logtime = DateFormat(datetime.now()).format("Y-m-d")
            )
        dto.save()
        return redirect("login")
    
class LoginView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    def get(self, request):
        template = loader.get_template("login.html")
        context = {}
        return HttpResponse(template.render(context, request))
    def post(self, request):
        id = request.POST["id"]
        passwd = request.POST["passwd"]
        mesaage = ""
        try :
            dto = Member.objects.get(id=id)
            if passwd == dto.passwd :
                request.session["memid"] = id
                return redirect("main")
            else :
                message = "입력하신 비밀번호가 다릅니다"                
        except  ObjectDoesNotExist :
            message = "입력하신 아이디가 없습니다"
        
        template = loader.get_template("login.html")
        context = {
            "message" : message,
            }
        return HttpResponse(template.render(context, request))
        
    
class ConfirmView(View):
    def get(self, request):
        template = loader.get_template("confirm.html")
        id = request.GET["id"]
        result = 0
        try :
            # 아이디가 있다
            Member.objects.get(id = id)
            result = 1
        except ObjectDoesNotExist :
            # 아이디가 없다
            result = 0
        context = {
            "id" : id,
            "result" : result,
            }
        return HttpResponse(template.render(context, request))
    
    
class LogoutView(View):
    def get(self, request):
        del(request.session["memid"])
        return redirect("main")
    

class MDeleteView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    def get(self, request):
        template = loader.get_template("mdelete.html")
        context = {}
        return HttpResponse(template.render(context, request))
    def post(self, request):
        id = request.session.get("memid")
        passwd = request.POST["passwd"]
        dto = Member.objects.get(id=id)
        if passwd == dto.passwd:
            dto.delete()
            del(request.session["memid"])
            return redirect("main")
        else :
            template = loader.get_template("mdelete.html")
            context = {
                "message" : "비밀번호가 다릅니다",
                }
            return HttpResponse(template.render(context, request))
        

# 회원정보 수정
class MModifyView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    def get(self, request):
        template = loader.get_template("mmodify.html")
        context = {}
        return HttpResponse(template.render(context, request))
    def post(self, request):
        id = request.session.get("memid")
        passwd = request.POST["passwd"]
        dto = Member.objects.get(id=id)
        if passwd == dto.passwd:
            template = loader.get_template("mmodifyPro.html")
            e = dto.email.split("@")
            if dto.tel :
                t = dto.tel.split("-")
                context = {
                    "dto" : dto,
                    "e" : e,
                    "t" : t,
                    }
            else :
                context = {
                    "dto" : dto,
                    "e" : e,
                }
            return HttpResponse(template.render(context, request))
        else :
            template = loader.get_template("mmodify.html")
            context = {
                "message" : "비밀번호가 다릅니다",
                }
            return HttpResponse(template.render(context, request))
        

class MModifyProView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    def post(self, request):
        id = request.session.get("memid")
        passwd = request.POST["passwd"]
        email = request.POST["email1"] + "@" + request.POST["email2"]
        tel = ""
        tel1 = request.POST["tel1"]
        tel2 = request.POST["tel2"]
        tel3 = request.POST["tel3"]
        if(tel1 and tel2 and tel3) :
            tel = tel1 + "-" + tel2 + "-" + tel3
        depart = request.POST["depart"]
        
        dto = Member.objects.get(id=id)
        dto.passwd = passwd
        dto.email = email
        dto.tel = tel
        dto.depart = depart
        dto.save()
        return redirect("main")
