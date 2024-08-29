from django.shortcuts import render
from .forms import ParametersForm
import joblib

modelo = joblib.load("./testmodel/modelos/modelo_clasi.pkl")

def index(request):
    if request.method == "POST":
        form = ParametersForm(request.POST)
        if form.is_valid():

            parameter_one = form.cleaned_data["petal_length"]
            parameter_two = form.cleaned_data["petal_width"]
            parameter_three = form.cleaned_data["sepal_length"]
            parameter_four = form.cleaned_data["sepal_width"]
            prediccion = modelo.predict([[parameter_one,parameter_two,parameter_three,parameter_four]])

            form = ParametersForm()

            contexto = {
                "form":form,
                "prediccion":prediccion,
                "parameter_one":parameter_one,
                "parameter_two":parameter_two,
                "parameter_three":parameter_three,
                "parameter_four":parameter_four,
            }

            return render(request,"testmodel/index.html",contexto)
    else: 
        form = ParametersForm()
    return render(request,"testmodel/index.html",{"form":form})