from asyncio.windows_events import NULL
from turtle import title
from django.shortcuts import render

from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.views.decorators.csrf import csrf_protect 
from django.views.decorators.csrf import csrf_exempt


import json
from django.conf.urls.static import static

# loads formula from local json file
json_data = open('static/formulas.json')   
formulas_data = json.load(json_data) # deserialises it
json_data.close()


# receives data from user and send back response
@csrf_protect
def postData(request):
    if request.method == 'POST':
        userdata = {
            'bodyweight' : request.POST['bodyweight'],
            'f_level' : request.POST['f_level'],
            'pushups' : request.POST['pushups'],
            'squats' : request.POST['squats'],
            'pullups': request.POST['pullups'],
            'plank': request.POST['plank'],
        }
        formData = {
            'data': userdata,
            'calc_data': generateexercise(userdata)
        }
    return render(request, 'result.html', formData)


# calculates if a exercise valid for user
def calc(exercise, userdata):
    exercise['baseline_formula'] = exercise['baseline_formula'].lower()
    exercise['fsc_formula'] = exercise['fsc_formula'].lower()
    if userdata[exercise['type']] != '':
        expr = exercise['baseline_formula'].replace(exercise['type'], userdata[exercise['type']]).replace('bw', userdata['bodyweight']).replace(" ", "")
        code = compile(expr, "<string>", "eval")
        reps = eval(code)
    else:
        expr = exercise['fsc_formula'].replace('fsc', userdata['f_level']).replace('bw', userdata['bodyweight']).replace(" ", "")
        code = compile(expr, "<string>", "eval")
        reps = eval(code)
    if(6 <= int(reps) <= 12):
        finalreps = int(reps)
    else:
        finalreps = 'NA'
    return finalreps


# loops on available exercises to extract valid exercise
def generateexercise(userdata):
    newReturnList=[]
    for obj in formulas_data:
        calc_result = calc(obj, userdata)
        if(calc_result != 'NA'):
            newReturnList.append({'exercise': obj['exercise'], 'reps': calc_result})
    return newReturnList

# home page - user enters data
@csrf_protect
def homePageView(request):
    form = userInputForm()
    return render(request, "home.html", {"form": form})

# form class
class userInputForm(forms.Form):
    f_level = forms.IntegerField(initial=5, min_value=1, max_value=10, label='Enter your fitness level (1-10)')
    bodyweight = forms.IntegerField(label='Enter your body weight in lbs')
    pushups = forms.IntegerField(required=False, label="How many push-ups can you do?")
    squats = forms.IntegerField(required=False, label="How many squats can you do?")
    pullups = forms.IntegerField(required=False, label="How many pull ups can you do?")
    plank = forms.IntegerField(required=False, label="How long can you hold a plank in seconds?")