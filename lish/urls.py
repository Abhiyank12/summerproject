
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from lishapp import views
app_name="dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='main'),
    path('index/',views.index, name='index'),
    path('contact/',views.contact, name='contact'),
    # path('main/',views.main, name='main'),
    path('about/',views.about, name='about'),
    path('adminlog/',views.adminlog, name='adminlog'),
    path('adminbase/',views.adminbase,name='adminbase'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('dashboard/vproduct/',views.vproduct,name="dashboard-vproduct"),
    path('dashboard/addproduct/',views.addproduct,name='dashboard-addproduct'),
    path("dashboard/addcat/",views.addcat,name="dashboard-addcat"),
    path("dashboard/vcat/",views.vcat,name="vcat"),
    path('ecat/<int:pid>/',views.ecat,name="dashboard-ecat"),
    path('dcat/<int:pid>/',views.dcat,name="dashboard-dcat"),
    path('epro/<int:pid>/',views.epro,name="dashboard-epro"),
    path('dpro/<int:pid>/',views.dpro,name="dashboard-dpro"),
    path('userregis/',views.userregis,name='userregis'),
    path('ulogin/',views.ulogin,name='ulogin'),
    path('logout/',views.logoutuser,name='logout'),
    path('dashboard/adminlogout/',views.adminlogout,name="dashboard-adminlogout"),
    path('userprofile',views.userprofile,name="userprofile"),
   
    path('user-product/<int:pid>/', views.user_product, name="user_product"),
    path('product-detail/<int:pid>/', views.product_detail, name="product_detail"),
    path('add-to-cart/<int:pid>/', views.addToCart, name="addToCart"),
    path('cart/',views. cart, name="cart"),
    path('incredecre/<int:pid>/',views. incredecre, name="incredecre"),
    path('deletecart/<int:pid>/',views. deletecart, name="deletecart"),
    path("dashboard/vuser/",views.vuser,name="dashboard-vuser"),
    path('duser/<int:pid>/',views.duser,name="dashboard-duser"),
    path('booking/',views. booking, name="booking"),
    path('order/', views.myOrder, name="myorder"),
    path('change-order-status/<int:pid>/', views.change_order_status, name="change_order_status"),
   
   path('manage-order/', views.manage_order, name="manage-order"), 
   path('delete-order/<int:pid>/', views.delete_order, name="delete_order"),
   path('payment/',views.payment, name="payment"), 
  path('api/verify_payment',views.verify_payment,name='verify_payment'),
   
   
    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
