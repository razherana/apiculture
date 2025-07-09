


# class StatistiqueDashboard(models.Model):
#     """
#     This model serves as a placeholder for dashboard statistics.
#     It can be used to store precalculated statistics or
#     for implementing methods that calculate stats on demand.
#     """
#     date_generated = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'statistique_dashboard'

#     @staticmethod
#     def get_total_ruches():
#         return Ruche.objects.count()

#     @staticmethod
#     def get_total_essaims():
#         return Essaim.objects.count()

#     @staticmethod
#     def get_total_miel_stock():
#         from projet.models.productions import MielStock
#         return MielStock.objects.aggregate(total=Sum('added_quantity'))['total'] or 0

#     @staticmethod
#     def get_total_ventes():
#         return Vente.objects.count()
