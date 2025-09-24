from django.urls import path
from admin.views import admin_login,admin_dashboard,all_users,admin_logout,block_user,unblock_user,show_block_users,show_category,delete_category,edit_category,show_products,delete_product,add_category,add_product,edit_product,cartview,removefromcart,order_transactions

urlpatterns = [
    path('login/',admin_login,name='admin_login'),
    path('admindashboard/',admin_dashboard,name='admin_dashboard'),
    path('all_users/',all_users,name='all_users'),
    path('admin_logout',admin_logout,name="admin_logout"),
    path('block_user/<int:user_id>',block_user,name='block_user'),
    path('unblock_user/<int:user_id>',unblock_user,name='unblock_user'),
    path('show-all-block-users/',show_block_users,name='show_block_users'),
    path('show-category/',show_category,name='show_category'),
    path('delete-category/<int:pk>/',delete_category,name='delete_category'),
    path('edit-category/<int:pk>',edit_category,name='edit_category'),
    path('show_products',show_products,name='show_products'),
    path('delete-product/<int:pk>/',delete_product,name='delete_product'),
    path('add-category/',add_category,name='add_category'),
    path('add_product',add_product,name='add_product'),
    path('edit-product/<int:pk>/',edit_product,name='edit_product'),
    path('cart-view/',cartview,name='cartview'),
    path('removefromcart/<int:product_id>/',removefromcart, name='removefromcart'),
    path('order-transactions/',order_transactions,name='order_transactions')

]
