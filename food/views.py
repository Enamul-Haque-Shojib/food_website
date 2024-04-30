from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

# Create your views here.
from . import models
from . import forms


from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# class ClothViewSet(viewsets.ModelViewSet):
#     queryset = models.Cloth.objects.all()
#     serializer_class = serializers.ClothSerializer
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['name', 'price', 'color__name', 'Size__name', 'category__name']
#     ordering_fields = ['Size__name', 'rating', 'price']




# class ClothWishListFilter(filters.BaseFilterBackend):
#     def filter_queryset(self, request, query_set, view):
#         u = request.user
#         if u:
#             return query_set.filter(author = u)
#         return query_set

# class ClothWishListViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = models.ClothWishList.objects.all()
#     serializer_class = serializers.ClothWishListSerializer
#     filter_backends = [ClothWishListFilter]  


# class ClothCartListFilter(filters.BaseFilterBackend):
#     def filter_queryset(self, request, query_set, view):
#         u = request.user
#         if u:
#             return query_set.filter(author = u)
#         return query_set

# class ClothCartListViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = models.ClothCartList.objects.all()
#     serializer_class = serializers.ClothCartListSerializer
#     filter_backends = [ClothCartListFilter] 
    





class FoodDetailsView(DetailView):
    model = models.Food
    template_name = 'food_details.html'
    pk_url_kwarg = 'foodid'

    

    

    def post(self, request, *args, **kwargs):
        review_form = forms.ReviewForm(data = self.request.POST)
        
        food_object = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit = False)
            new_review.food = food_object
            new_review.author = self.request.user
            new_review.save()
            count_rating=0
            review_model = models.Review.objects.filter(food = food_object.foodid)
            total_reviews = len(review_model)
            for rev in review_model:
                print('>>>>',rev.rating)
                count_rating = count_rating + int(rev.rating)
            avg_rating = count_rating/total_reviews
           
            food_object.rating = format(avg_rating, ".1f")
            food_object.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        food = self.object
        reviews = food.reviews.all()

        review_form = forms.ReviewForm()



        foodData = models.Food.objects.filter(category = self.object.category ).exclude(foodid = self.object.foodid)
        context["foodData"] = foodData

        
        context['reviews'] = reviews
        context['review_form'] = review_form
        context['food_ratings'] = range(int(self.object.rating))
        return context
    

    

class FoodRecommendView(TemplateView):
    model = models.Food
    template_name = 'food_details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['food_data'] = models.FoodWishList.objects.filter(author = self.request.user)

        return context




class FoodWishListView(TemplateView):
    template_name = 'food_wishlist.html'
    model = models.FoodWishList

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['food_wishlist'] = models.FoodWishList.objects.filter(author = self.request.user)

        return context

class FoodCardListView(TemplateView):
    template_name = 'food_cardlist.html'
    model = models.FoodCardList
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        foodcardlist = models.FoodCardList.objects.filter(author = self.request.user)
        count_price = 0
        for obj in models.FoodCardList.objects.filter(author = self.request.user):
            count_price = count_price + obj.price
        print(count_price)
        context = {'total_price' : count_price, 'food_cardlist' : foodcardlist}
        return context
    
class FoodHistoryListView(TemplateView):
    template_name = 'food_history.html'
    model = models.HistoryList
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['food_historylist'] = models.HistoryList.objects.filter(author = self.request.user)

        return context


@login_required
def foodWishList(request, foodid):

    food = models.Food.objects.get(pk = foodid)
    
    check_in_food_wishlist = models.FoodWishList.objects.filter(foodid = food.foodid, name = food.name, author = request.user)
      
    
    
    if request.method == 'GET':

        if check_in_food_wishlist:
            messages.warning(request, 'You have already added this your wish list')
            return redirect('food_details',foodid=food.foodid)
        else:
            food_wishlist = models.FoodWishList()
            
            food_wishlist.foodid = food.foodid
            food_wishlist.name = food.name
            food_wishlist.price = food.price
            food_wishlist.description = food.description
            food_wishlist.category = food.category
            food_wishlist.rating = food.rating
            food_wishlist.author = request.user
            
            food_wishlist.image = food.image
            

            food_wishlist.save()


            
            messages.success(request, 'The item is added in wishlist')
            return redirect('food_details',foodid=food.foodid)
                
    return render(request, 'food_details.html')


@login_required
def foodCardList(request, foodid):

    food = models.Food.objects.get(pk = foodid)
    
    if request.method == 'GET':
        
        food_cartlist = models.FoodCardList.objects.filter(foodid = food.foodid, name = food.name, author = request.user)
        if food_cartlist:
            s = models.FoodCardList.objects.get(foodid = food.foodid, name = food.name, author=request.user)
            s.quantity = s.quantity + 1
            s.price = s.price + food.price
            s.save()
            return redirect('food_details',foodid=food.foodid)
                    
            
        else:
            x = models.FoodCardList()

            x.foodid = food.foodid
            x.name = food.name
            x.price = food.price
            x.quantity = 1
            x.description = food.description
            x.category = food.category
            x.author = request.user
            x.image = food.image
            x.rating = food.rating
            x.save()

            messages.success(request, 'The item is added in CardList')
            return redirect('food_details',foodid=food.foodid)
        


    return render(request, 'food_details.html')

@login_required
def foodCardListPlus(request, foodid):
    
    food = models.Food.objects.get(pk = foodid)
    
    if request.method == 'GET':
        food_cardlist = models.FoodCardList.objects.filter(foodid = food.foodid, name = food.name, author = request.user)
        if food_cardlist:
            s = models.FoodCardList.objects.get(foodid = food.foodid, name = food.name, author=request.user)
            s.quantity = s.quantity + 1
            s.price = s.price + food.price
            s.save()
            return redirect('food_cardlist')
                    
            
        else:
               
            return redirect('food_cardlist')
           


    return render(request, 'food_cardlist.html')


@login_required
def foodCardListMinus(request, foodid):
    
    food = models.Food.objects.get(pk = foodid)
    
    
    if request.method == 'GET':
        
        food_cartlist = models.FoodCardList.objects.filter(foodid = food.foodid, name = food.name, author = request.user)
        if food_cartlist:

            s = models.FoodCardList.objects.get(foodid = food.foodid, name = food.name, author=request.user)
            if s.quantity > 0:
            
                s.quantity = s.quantity - 1
                s.price = s.price - food.price
                   
                s.save()
                return redirect('food_cardlist')
            else:
                   
                return redirect('food_cardlist')
            
        else:
            return redirect('food_cardlist')


    return render(request, 'food_cartlist.html')

class WishListDeleteView(DeleteView):
     model = models.FoodWishList
    #  pk_url_kwarg = 'id'
     template_name = 'delete_wishlist.html'
     success_url = reverse_lazy('food_wishlist')

class CardListDeleteView(DeleteView):
     model = models.FoodCardList
    #  pk_url_kwarg = 'id'
     template_name = 'delete_cardlist.html'
     success_url = reverse_lazy('food_cardlist')

class HistoryListDeleteView(DeleteView):
     model = models.HistoryList
    #  pk_url_kwarg = 'id'
     template_name = 'delete_historylist.html'
     success_url = reverse_lazy('food_historylist')






def orderNow(request):
    
    food_cardlist = models.FoodCardList.objects.filter(author = request.user)

    for obj in food_cardlist:
        food_historylist = models.HistoryList()
        food_historylist.foodid = obj.foodid
        food_historylist.name = obj.name
        food_historylist.price = obj.price
        food_historylist.description = obj.description
        food_historylist.quantity = obj.quantity
        food_historylist.author = request.user
        food_historylist.rating = obj.rating        
        food_historylist.category = obj.category        
        food_historylist.image = obj.image        
        food_historylist.save()
    food_cardlist.delete()
    
    context= {}    
    # return render(request, 'food_cardlist.html', context)
    return render(request, 'food_payment.html', context)








def deleteWishlistAll(request):
    
    models.FoodWishList.objects.filter(author = request.user).delete()
    context= {}    
    return render(request, 'food_wishlist.html', context)

def deleteHistorylistAll(request):
    
    models.HistoryList.objects.filter(author = request.user).delete()
    context= {}    
    return render(request, 'food_history.html', context)
















    

