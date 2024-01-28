
from django.urls import path, include
from . import views



urlpatterns = [

    path('fooddetails/<int:foodid>', views.FoodDetailsView.as_view(), name='food_details' ),
    path('foodwishlist/', views.FoodWishListView.as_view(), name='food_wishlist' ),
    path('foodcardlist/', views.FoodCardListView.as_view(), name='food_cardlist' ),
    path('historylist/', views.FoodHistoryListView.as_view(), name='food_historylist' ),
    path('addwishlist/<int:foodid>', views.foodWishList, name='add_wishlist' ),
    path('addcardlist/<int:foodid>', views.foodCardList, name='add_cardlist' ),
    path('addcardlistplus/<int:foodid>', views.foodCardListPlus, name='add_cardlist_plus' ),
    path('addcardlistminus/<int:foodid>', views.foodCardListMinus, name='add_cardlist_minus' ),
    path('deletecardlist/<int:pk>', views.CardListDeleteView.as_view(), name='delete_cardlist' ),
    path('deletewishlist/<int:pk>', views.WishListDeleteView.as_view(), name='delete_wishlist' ),
    path('deletehistorylist/<int:pk>', views.HistoryListDeleteView.as_view(), name='delete_historylist' ),
    path('deletewishlistall/', views.deleteWishlistAll, name='delete_wishlist_all' ),
    path('deletehistorylistall/', views.deleteHistorylistAll, name='delete_historylist_all' ),
    path('ordercartlist/', views.orderNow, name='ordernow_cardlist' ),
    
  
]