from django.shortcuts import render
from marks.forms import StudentForm
from marks.data import getData
from marks.functions import handle_uploaded_file

temp=None
temp1=None
x=None
# Create your views here.
def index(request):
    if request.method == 'POST':  
        student = StudentForm(request.POST, request.FILES)  
        if student.is_valid():
            global temp, temp1,x  
            handle_uploaded_file(request.FILES['file'])
            name1 = request.FILES['file']
            x=name1
            temp, temp1 = getData("static/upload/"+name1.name)
            context={'data':temp.to_html(), 'data1':temp1.to_html, 'th':60, 'min3':0.8, 'min2':0.7, 'min1':0.6}
            return render(request, "another.html", context)
        th = request.POST.get("threshold")
        min3 = request.POST.get("min3")
        min2 = request.POST.get("min2")
        min1 = request.POST.get("min1")
        if th.isdigit():
            th=int(th)
        else:
            th=60
        if min3.isdecimal():
            min3=float(min3)
        else:
            min3=0.8
        if min2.isdecimal():
            min2=float(min2)
        else:
            min2=round(min3-0.1,1)
        if min1.isdecimal():
            min1=float(min1)
        else:
            min1=round(min2-0.1,1)
        temp, temp1 = getData("static/upload/"+x.name, th, min3, min2, min1)
        context={'data':temp.to_html(), 'data1':temp1.to_html, 'th':th, 'min3':min3, 'min2':min2, 'min1':min1}
        return render(request, "another.html", context)
    student = StudentForm()
    return render(request, "index.html", {'form':student})