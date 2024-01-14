from django.shortcuts import render
from templates.models import Person

def index_page(request):
    persons = Person.objects.all()
    s = ""
    for person in persons:
        s += f"<h3>{person}: возраст - {person.age}, должность - {person.job.lower()}</h3>"
    return render(request, 'index.html', context={"person_list": s})


def add_page(request):
    return render(request, 'add.html')


def add_person(request):
    fname, lname = request.POST.get("first_name"), request.POST.get("last_name")
    age, job = request.POST.get("age"), request.POST.get("job")

    if fname and lname and age and job:
        try:
            Person.objects.create(
                first_name=fname, last_name=lname,
                age=age, job=job
            )
        except:
            print("[ERROR]: Form was not filled correctly")

    return request(index_page)