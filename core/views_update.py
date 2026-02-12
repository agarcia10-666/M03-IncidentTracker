from django.db import connection
from django.shortcuts import render, redirect

def actualitzar_correu(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_id = request.user.id
        
        # LÍNIA VULNERABLE: Manca de sanitització per concatenació directa
        sql = f"UPDATE auth_user SET email = '{email}' WHERE id = {user_id};"
        
        with connection.cursor() as cursor:
            cursor.execute(sql)
            
        return redirect('dashboard')
    return render(request, 'actualitzar_correu.html')
