from django.urls import reverse
from django.test import TestCase
from factures.models import Facture, Client, CategorieFacture
from django.utils import timezone

class FactureViewTest(TestCase):

    def setUp(self):
        self.client_test = Client.objects.create(nom="Client Test")
        self.categorie_test = CategorieFacture.objects.create(nom="Catégorie Test")
        self.facture_test = Facture.objects.create(
            numero="1234",
            date=timezone.now().date(),
            montant=100.00,
            categorie=self.categorie_test,
            client=self.client_test,
            est_payee=False
        )
        self.facture_test2 = Facture.objects.create(
            numero="5678",
            date=timezone.now().date(),
            montant=150.00,
            categorie=self.categorie_test,
            client=self.client_test,
            est_payee=True
        )

    def test_listage_factures(self):
        """
        Test que la vue de listage des factures renvoie une réponse 200.
        """
        response = self.client.get(reverse('facture_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'factures/facture_list.html')

    def test_listage_factures_contenu(self):
        """
        Test que la liste des factures contient plusieurs factures.
        """
        response = self.client.get(reverse('facture_list'))
        self.assertContains(response, self.facture_test.numero)  
        self.assertContains(response, self.facture_test2.numero)

    def test_listage_factures_vide(self):
        """
        Test qu'un message 'aucune facture' s'affiche quand il n'y a pas de factures.
        """
        Facture.objects.all().delete() 
        response = self.client.get(reverse('facture_list'))
        self.assertContains(response, "Aucune facture trouvée.")

    def test_affichage_facture(self):
        """
        Test que la vue d'affichage d'une facture renvoie une réponse 200.
        """
        url = reverse('facture_detail', args=[self.facture_test.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'factures/facture_detail.html')

    def test_affichage_contenu_facture(self):
        """
        Test que les détails de la facture sont correctement affichés.
        """
        url = reverse('facture_detail', args=[self.facture_test.pk])
        response = self.client.get(url)
        self.assertContains(response, self.facture_test.numero)
        self.assertContains(response, self.facture_test.montant)
        self.assertContains(response, self.facture_test.categorie.nom)

    def test_facture_inexistante(self):
        """
        Test que l'affichage d'une facture inexistante renvoie une erreur 404.
        """
        url = reverse('facture_detail', args=[9999]) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

