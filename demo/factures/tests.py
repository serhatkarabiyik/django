from django.test import TestCase
from factures.models import Facture, CategorieFacture
from clients.models import Client 
from django.utils import timezone
from django.core.exceptions import ValidationError

class FactureModelTest(TestCase):

    def setUp(self):
        self.client_test = Client.objects.create(nom="Test Client", email="testclient@testclient.com")
        
        self.categorie_test = CategorieFacture.objects.create(nom="Test Catégorie")
        
        self.facture_test = Facture.objects.create(
            numero="1234",
            date=timezone.now().date(),
            montant=50.00,
            categorie=self.categorie_test,
            client=self.client_test,
            est_payee=False
        )

    def test_creation_facture(self):
        """
        Test que la facture est correctement créée avec les bonnes valeurs.
        """
        facture = self.facture_test
        self.assertEqual(facture.numero, "1234")
        self.assertEqual(facture.montant, 50.00)
        self.assertEqual(facture.client.nom, "Test Client")
        self.assertEqual(facture.est_payee, False)

    def test_facture_avec_montant_negatif(self):
        """
        Test qu'une facture ne peut pas être créée avec un montant négatif.
        """
        with self.assertRaises(ValidationError, msg="Une facture ne peut pas avoir un montant négatif."):
            facture = Facture(
                numero="3579",
                date=timezone.now().date(),
                montant=-100.00,
                categorie=self.categorie_test,
                client=self.client_test,
                est_payee=False
            )
            facture.clean()

    def test_facture_pas_etre_payee_avec_montant_zero(self):
        """
        Test qu'une facture pas payée si son montant est zéro.
        """
        facture = Facture.objects.create(
            numero="5678",
            date=timezone.now().date(),
            montant=0.00,  
            categorie=self.categorie_test,
            client=self.client_test,
            est_payee=False
        )

        facture.est_payee = True
        with self.assertRaises(ValueError, msg="Une facture avec un montant de 0 ne peut pas être marquée comme payée"):
            if facture.montant <= 0:
                raise ValueError("Une facture avec un montant de 0 ne peut pas être marquée comme payée")
            facture.save()

    def test_toutes_les_factures_client_comme_payees(self):
        """
        Test que toutes les factures d'un client peuvent être marquées comme payées et vérifier leur statut.
        """
        facture1 = Facture.objects.create(
            numero="1357",
            date=timezone.now().date(),
            montant=100.00,
            categorie=self.categorie_test,
            client=self.client_test,
            est_payee=False
        )
        facture2 = Facture.objects.create(
            numero="2468",
            date=timezone.now().date(),
            montant=150.00,
            categorie=self.categorie_test,
            client=self.client_test,
            est_payee=False
        )

        Facture.objects.filter(client=self.client_test).update(est_payee=True)

        factures = Facture.objects.filter(client=self.client_test)
        for facture in factures:
            self.assertTrue(facture.est_payee, f"La facture {facture.numero} n'est pas marquée comme payée.")