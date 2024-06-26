from django.urls import path, re_path
from test_polar import views

app_name = "test_polar"

urlpatterns = [
    # re_path(r"^add_ttype/$", views.add_ttype, name="addttype")
    path("", views.redirect_to_home, name="tohome"),
    path("home/", views.select_collections, name="selectcol"),
    path("summary/", views.show_polar, name="showpolar"),
    path(
        "summary/return_lapdata/<str:fname>",
        views.show_lapdata,
        name="showlapdata",
    ),
    path("adapt/", views.start_adapt, name="startadapt"),
    path("adapt/form/<str:fname>", views.show_adapt, name="showadapt"),
    path("adapt/formlap/<str:fname>", views.show_adaptlap, name="showadaptlap"),
    path("adapt/formlap/", views.adapt_distance, name="adaptlapdistance"),
    path("analyze/", views.start_analyze, name="startanalyze"),
    path("analyze/plot/<str:fname>", views.plot_analyze, name="plotanalyze"),
]
