from django.http import Http404
from django.db.models import FieldDoesNotExist

# from django.urls import reverse # for room_detail
# from django.http import Http404 # for room_detail

# from math import ceil #for first one
from django.shortcuts import render, redirect, reverse  # for second one
from django.core.paginator import Paginator

# from django.core.paginator import Paginator, EmptyPage # for second one
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    View,
    UpdateView,
    FormView,
    DeleteView,
)
from django_countries import countries
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from users import mixins as user_mixins
from . import models, forms

# 수동으로 만들기
"""
def all_rooms(request):
    page = request.GET.get("page", 1)  # 0는 default 값
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count + 1),
        },
    )
"""

"""
# django Paginator로 빠르게 만들기
def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = (
        models.Room.objects.all()
    )  # 쿼리셋을 만들 때 모든 요소를 즉시 불러오지는 않는다. 호출 할 경우에 DB에서 불러온다. 이는 DB에 부담이 된다.
    paginator = Paginator(room_list, 10, orphans=5)  # object list, page number

    try:
        rooms = paginator.page(page)  # get_page return the page object
        return render(request, "rooms/home.html", {"page": rooms})
    except EmptyPage:
        return redirect("/")
"""


class HomeView(ListView):
    """ HomeView Definition """

    model = models.Room  # CBV(class based view)는 보여줄 model이 필요하다.
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        # 기본 구현을 호출해 context를 가져온다.
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        # now를 context 객체에 추가한다.
        context["now"] = now
        return context


"""
def room_detail(request, pk): # FBV(funtion base view)
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        raise Http404() # 에러가 뜨게 하려면 raise를 해야한다.
        # return redirect(reverse("core:home")) home으로 가고 싶을 때
"""


class RoomDetail(DetailView):
    """ Room Detail Definition """

    model = models.Room


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")
                house_rules = form.cleaned_data.get("house_rules")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country  # [" "] 안에는 foreign key를 집어넣는다.

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price  # lte = less than equal

                if guests is not None:
                    filter_args["guests__gte"] = guests  # gte = greater than equal

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                for house_rule in house_rules:
                    filter_args["house_rules"] = ihouse_rule

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)
                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )
        else:
            form = forms.SearchForm()
        return render(request, "rooms/search.html", {"form": form})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):
    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete this photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated"
    fields = ("caption",)

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):
    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class DeleteRoomView(user_mixins.LoggedInOnlyView, DeleteView):
    model = models.Room
    template_name = "rooms/room_delete.html"

    def get_success_url(self):
        pk = self.request.user.pk
        return self.request.user.get_absolute_url()


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):
    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()
        messages.success(self.request, "Room created")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))

