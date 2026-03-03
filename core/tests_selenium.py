from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import os

class SecurityRegressionTests(StaticLiveServerTestCase):
    fixtures = ['testdb.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.add_argument("--headless")  # Modo sin interfaz (obligatorio en CI)
        
        # En GitHub Actions, Firefox suele estar en esta ruta de Ubuntu
        # Si localmente usas Windows/Mac, el 'if' evita errores
        if os.path.exists("/usr/bin/firefox"):
            opts.binary_location = "/usr/bin/firefox"
        
        try:
            cls.selenium = WebDriver(options=opts)
            cls.selenium.implicitly_wait(10)
        except Exception as e:
            print(f"Error al iniciar Firefox WebDriver: {e}")
            raise

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'selenium'):
            cls.selenium.quit()
        super().tearDownClass()

    def test_role_restriction(self):
        """AUDITORIA: L'analista no ha d'entrar a /admin/"""
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))

        # 1. Completar el login
        self.selenium.find_element(By.NAME, "username").send_keys("analista1")
        self.selenium.find_element(By.NAME, "password").send_keys("12345678")
        
        # 2. Clicar el botó de login
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()

        # 3. Intentar forçar URL d'admin
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))

        # 4. Debug (Útil si vuelve a fallar en GitHub)
        print(f"\nDEBUG: El títol actual de la pàgina és: '{self.selenium.title}'")

        # 5. ASSERT de Seguretat
        # Si el títol NO es el de administración, significa que el acceso fue denegado o redirigido.
        self.assertNotEqual(
            self.selenium.title, 
            "Site administration | Django site admin", 
            "ERROR: L'analista ha pogut accedir al panell d'administració!"
        )
