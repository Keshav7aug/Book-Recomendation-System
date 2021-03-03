from django.shortcuts import render
from django import forms
import BookRecomender 
# Create your views here.
class NewbookForms(forms.Form):
    book = forms.CharField(label="Book Name")
def index(request):
    book_name=""
    if request.method=="POST":
        form = NewbookForms(request.POST)
        if form.is_valid():
            book_name  = form.cleaned_data["book"]
    if book_name!="":
        #print('aaaa',book_name)
        pred = BookRecomender.get_recommendations([book_name])
    else:
        pred=""
    return render(request,"BookRecommendation/index.html",{
        "pred":pred,"book":NewbookForms(),"bookName":book_name
    })
