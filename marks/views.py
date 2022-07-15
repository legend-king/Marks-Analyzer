from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from marks.forms import StudentForm
from marks.data import getData
from marks.functions import handle_uploaded_file
from wsgiref.util import FileWrapper
import mimetypes
import os

temp=None
temp1=None
th, min1, min2, min3 = 60, 0.8, 0.7, 0.6
x=None
# Create your views here.
def index(request):
    if request.method == 'POST':  
        student = StudentForm(request.POST, request.FILES)  
        if student.is_valid():
            global temp, temp1,x, th, min1, min2, min3
            handle_uploaded_file(request.FILES['file'])
            name1 = request.FILES['file']
            x=name1
            temp, temp1 = getData("static/upload/"+name1.name)
            context={'data':temp.to_html(), 'data1':temp1.to_html, 'th':60, 'min3':0.8, 'min2':0.7, 'min1':0.6}
            return render(request, "form.html", context)
        th = request.POST.get("threshold")
        min3 = request.POST.get("min3")
        min2 = request.POST.get("min2")
        min1 = request.POST.get("min1")
        if th.isdigit():
            th=int(th)
        else:
            th=60
        min3=float(min3)
        if float(min2)>float(min3):
            min2=round(min3-0.1,1)
        else:
            min2=float(min2)
        if float(min1)>float(min2):
            min1=round(min2-0.1,1)
        else:
            min1=float(min1)
        temp, temp1 = getData("static/upload/"+x.name, th, min3, min2, min1)
        context={'data':temp.to_html(), 'data1':temp1.to_html, 'th':th, 'min3':min3, 'min2':min2, 'min1':min1}
        return render(request, "form.html", context)
    # if request.method=='POST' and 'download' in request.POST:
    #     temp1.to_excel("Attainment.xlsx")
    #     temp.to_excel("Marks.xlsx")
    #     context={'data':temp.to_html(), 'data1':temp1.to_html, 'th':th, 'min3':min3, 'min2':min2, 'min1':min1}
    #     return render(request, "another.html", context)

        
    student = StudentForm()
    return render(request, "index.html", {'form':student})


def downloadAttainment(request):
    if not(temp1 is None):
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename="Attainment.xlsx"
        filepath = base_dir+'/Files/'+filename
        temp1.to_excel(filepath)
        thefile=filepath
        filename=os.path.basename(thefile)
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(open(thefile, 'rb'), chunk_size),content_type=mimetypes.guess_type(thefile)[0])
        response['Content-Length']=os.path.getsize(thefile)
        response['Content-Disposition']="Attachment;filename=%s" % filename
        return response
    return HttpResponse("Cannot download")


def downloadMarks(request):
    if not(temp is None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename="Marks.xlsx"
        filepath = base_dir+'/Files/'+filename
        temp.to_excel(filepath)
        thefile=filepath
        filename=os.path.basename(thefile)
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(open(thefile, 'rb'), chunk_size),content_type=mimetypes.guess_type(thefile)[0])
        response['Content-Length']=os.path.getsize(thefile)
        response['Content-Disposition']="Attachment;filename=%s" % filename
        return response
    return HttpResponse("Cannot download")