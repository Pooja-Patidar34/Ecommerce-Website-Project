from django.urls import path
from admin.views import admin_login,admin_dashboard,all_users,admin_logout,block_user,unblock_user,show_block_users,show_category,delete_category,edit_category,show_products,delete_product,add_category,add_product,edit_product,cartview,removefromcart,order,create_user,role_list,create_role,assign_role,assigned_roles,permission_list_create,assign_role_permissions,edit_user

urlpatterns = [
    path('login/',admin_login,name='admin_login'),
    path("create-user/", create_user, name="create_user"),
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
    path('all-order',order,name='order'),
    path('roles/', role_list, name='role_list'),
    path('roles/create/', create_role, name='create_role'),
    path('assign-role',assign_role,name='assign_role'),
    path('assigned_roles',assigned_roles,name='assigned_roles'),
    path("permissions/", permission_list_create, name="permission_list_create"),
    path("assign-role-permissions/", assign_role_permissions, name="assign_role_permissions"),
    path('edit-user/<int:user_id>/', edit_user, name='edit_user'),

]

