from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

class SecurityRegressionTests(StaticLiveServerTestCase):
    fixtures = ['testdb.json'] # Càrrega de dades (Punt 2.2.2)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.add_argument("--headless") # mode Headless (Punt 2.2.1)
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_role_restriction(self):
#        """AUDITORIA: L'analista no ha d'entrar a /admin/"""
#        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
#        
#        # PUNT 2.2.3: Implementa el login amb 'analista1'
#        self.selenium.find_element(By.NAME, "username").send_keys("analista1")
#        # ... resta del login ...
#        
#        # Intentar forçar URL d'admin
#        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
#        
#        # ASSERT de Seguretat (Punt 2.2.3)
#        self.assertNotEqual(self.selenium.title, "Site administration | Django site admin")
        """AUDITORIA: L'analista no ha d'entrar a /admin/"""
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))

        # 1. Completar el login
        self.selenium.find_element(By.NAME, "username").send_keys("analista1")
        self.selenium.find_element(By.NAME, "password").send_keys("12345678") # La pass que vas posar al crear l'usuari
        
        # 2. Clicar el botó de login (molt important!)
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()

        # 3. Intentar forçar URL d'admin
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))

        # 4. Debug (Opcional: per veure què està passant al terminal)
        print(f"\nDEBUG: El títol actual de la pàgina és: '{self.selenium.title}'")

        # 5. ASSERT de Seguretat
        # Si el títol és "Log in | Django site admin", el test passarà (està prohibit entrar).
        # Si el títol és "Site administration | Django site admin", el test FALLARÀ.
        self.assertNotEqual(self.selenium.title, "Log in | Django site admin", "ERROR: El login ha fallat, revisa la contrasenya al JSON.")
        self.assertNotEqual(self.selenium.title, "Site administration | Django site admin", "VULNERABILITAT: L'analista ha entrat a l'admin!")
