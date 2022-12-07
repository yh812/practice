from django.shortcuts import render, redirect
from django.views.generic.base import View
import logging
from django.http.response import HttpResponse
from django.template import loader
from board.models import Board
from django.utils.dateformat import DateFormat
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)

class ListView(View):
    
    def get(self, request):
        template = loader.get_template("list.html")
        count = Board.objects.all().count()
        pagenum = request.GET.get("pagenum")    # get()은 null이 넘어와도 오류 x
        pagesize = 10       # 원래 변경 가능한 변수는 setting에서 선언해서 import해서 사용하는게 맞다
        pageblock = 3       # 원래는 10
        if not pagenum :
            pagenum = "1"
        pagenum = int(pagenum)
        start = (pagenum -1) * pagesize     # (5 -1) * 10 + 1    41 
        end = start + pagesize              # 41 + 10 -1         50
        if end > count :
            end = count
        
        dtos =  Board.objects.order_by("-ref", "restep")[start:end]
        number = count - (pagenum -1) * int(pagesize)
        
        pagecount = count // int(pagesize)  # 글 갯수 51 // 10    5
        if count % int(pagesize) > 0 :
            pagecount += 1                  # 6
        startpage = pagenum // int(pageblock) * int(pageblock) + 1
        #    5 // 10 * 10 + 1        1
        if pagenum % pageblock == 0 :
            startpage -= pageblock
        
        endpage = startpage + pageblock -1
        #    1 + 10 -1        10
        if endpage > pagecount :
            endpage = pagecount
        pages = range(startpage, endpage+1)
            
        context = {
            "count" : count,
            "dtos" : dtos,
            "number" : number,
            "pagenum" : pagenum,
            "pagecount" : pagecount,
            "startpage" : startpage,
            "endpage" : endpage,
            "pages" : pages,
            "pageblock" : pageblock,
            }
        return HttpResponse(template.render(context, request))
    
class BWriteView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    def get(self, request):
        template = loader.get_template("bwrite.html")
        # 제목글
        ref = 1
        restep = 0
        relevel = 0
        num = request.GET.get("num")
        if num == None :
            # 제목글
            try :
                maxnum = Board.objects.order_by("-num").values()[0]["num"]
                ref = maxnum + 1        # 그룹화아이디 = 글번호최대값 + 1
            except IndexError :
                # 글이 없는 경우
                ref = 1
        else :
            # 답변글
            ref = request.GET["ref"]
            restep = request.GET["restep"]
            relevel = request.GET["relevel"]
            res = Board.objects.filter(ref__exact=ref).filter(restep__gt=restep)
            for re in res :
                re.restep = re.restep + 1
                re.save()
            restep = int(restep) + 1
            relevel = int(relevel) + 1
            
        context = {
            "num" : num,
            "ref" : ref,
            "restep" : restep,
            "relevel" : relevel,
            }
        return HttpResponse(template.render(context, request))
    
    def post(self, request):
        dto = Board(
            writer = request.POST["writer"],
            subject = request.POST["subject"],
            passwd = request.POST["passwd"],
            content = request.POST["content"],
            readcount = 0,
            ref = request.POST["ref"],
            restep = request.POST["restep"],
            relevel = request.POST["relevel"],
            regdate = DateFormat(datetime.now()).format("Ymd"),
            ip = request.META.get("REMOTE_ADDR")
            )
        dto.save()
        return redirect("board:list")
    
class DetailView(View):
    def get(self, request):
        template = loader.get_template("detail.html")
        num = request.GET["num"]
        pagenum = request.GET["pagenum"]
        number = request.GET["number"]
        dto = Board.objects.get(num=num)
        if dto.ip != request.META.get("REMOTE_ADDR") :
            dto.readcount += 1
            dto.save()
        context = {
            "dto" : dto,
            "num" : num,
            "pagenum" : pagenum,
            "number" : number,
            }
        return HttpResponse(template.render(context, request))
    
class BDeleteView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)
    def get(self, request):
        template = loader.get_template("bdelete.html")
        num = request.GET["num"]
        pagenum = request.GET["pagenum"]
        context = {
            "num" : num,
            "pagenum" : pagenum,
            }
        return HttpResponse(template.render(context, request))
    
    def post(self, request):
        num = request.POST["num"]
        pagenum = request.POST["pagenum"]
        passwd = request.POST["passwd"]
        dto = Board.objects.get(num=num)
        if passwd == dto.passwd :
            # 비밀번호가 같다
            res = Board.objects.filter(ref__exact=dto.ref).filter(restep__exact=dto.restep+1).filter(relevel__gt=dto.relevel)
            if len(res) == 0 :
                # 답글이 없다
                logger.info("답글이 없다")
            else :
                # 답글이 있다
                logger.info("답글이 있다")
            return redirect("board:list")
        else :
            # 비밀번호가 다르다
            template = loader.get_template("bdelete.html")
            context = {
                "num" : num,
                "pagenum" : pagenum,
                "message" : "비밀번호가 다릅니다",
                }
            return HttpResponse(template.render(context, request))
    
    
    
    