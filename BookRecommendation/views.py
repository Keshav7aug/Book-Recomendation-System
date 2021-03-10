from django.shortcuts import render
from django import forms
#import floppyforms as forms
import BookRecomender 
# Create your views here.
All_Books = BookRecomender.getBookList()
class NewbookForms(forms.Form):
    #book = forms.CharField(label="Book Name")
    book = forms.ChoiceField(label="Book Name",choices = All_Books)
def index(request):
    book_name=""
    if request.method=="POST":
        form = NewbookForms(request.POST)
        if form.is_valid():
            book_name  = All_Books[int(form.cleaned_data["book"])][1]
    if book_name!="":
        #print('aaaa',book_name)
        pred = BookRecomender.get_recommendations([book_name])
    else:
        pred=""
    return render(request,"BookRecommendation/index.html",{
        "pred":pred,"book":NewbookForms(),"bookName":book_name,
    })
