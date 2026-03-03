from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

class SecurityRegressionTests(StaticLiveServerTestCase):
    fixtures = ['testdb.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox") # Añadido para mayor compatibilidad
        opts.add_argument("--disable-dev-shm-usage") # Evita problemas de memoria
        
        try:
            # Quitamos la línea de binary_location para que Selenium use el autodetect
            cls.selenium = WebDriver(options=opts)
            cls.selenium.implicitly_wait(10)
        except Exception as e:
            print(f"\n[ERROR] No se pudo iniciar Firefox: {e}")
            raise

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'selenium'):
            cls.selenium.quit()
        super().tearDownClass()

    def test_role_restriction(self):
        """AUDITORIA: L'analista no ha d'entrar a /admin/"""
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))

        # 1. Login
        self.selenium.find_element(By.NAME, "username").send_keys("analista1")
        self.selenium.find_element(By.NAME, "password").send_keys("12345678")
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()

        # 2. Intento de acceso a admin
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))

        # 3. Verificación
        # Si el acceso se deniega correctamente, el título NO debería ser el de administración
        self.assertNotEqual(
            self.selenium.title, 
            "Site administration | Django site admin", 
            "ERROR: ¡El analista ha podido entrar en el panel de admin!"
        )
