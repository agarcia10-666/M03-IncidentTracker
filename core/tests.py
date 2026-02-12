from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class SecuritySQLInjectionTest(TestCase):
    def setUp(self):
        # 1. Creem un usuari normal (no és superusuari)
        self.client = Client()
        self.user = User.objects.create_user(username='victim_user', password='password123')
        self.client.login(username='victim_user', password='password123')

    def test_privilege_escalation_sqli(self):
        """Test que detecta si un atacant pot esdevenir superusuari via SQLi"""
        # 2. Simulem el payload maliciós de l'Apartat 4
        payload = "hacker@test.com', is_superuser = '1"
        url = reverse('perfil') # Assegurem que el nom coincideix amb urls.py
        
        # Enviem el POST amb el payload
        self.client.post(url, {'email': payload})

        # Refresquem l'objecte usuari des de la base de dades
        self.user.refresh_from_db()

        # 3. Comprovem si l'usuari ha esdevingut superusuari
        # Aquest assert ha de FALLAR si la vulnerabilitat existeix (perquè volem que sigui False)
        # Però el test de l'auditor busca confirmar que NO és superusuari.
        self.assertFalse(
            self.user.is_superuser, 
            "SEGURETAT CRÍTICA: L'usuari ha escalat privilegis a superusuari via SQL Injection!"
        )
