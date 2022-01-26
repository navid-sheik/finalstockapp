



from django.http import JsonResponse


def get_stock_data (request, stock_id) :
    current_user  =  request.user
    if request.method  == 'GET':
        return JsonResponse({
            'current_user': current_user.to_dict()

        })