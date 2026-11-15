from django.db import models


class SheetTable(models.Model):
    """Un onglet du Google Sheet recopié en base (une ligne par onglet)."""

    name = models.CharField(max_length=100, unique=True)  # nom de l'onglet
    # Ordre des colonnes : PostgreSQL (jsonb) ne conserve pas l'ordre des clés d'un objet.
    columns = models.JSONField(default=list)
    header_row = models.PositiveIntegerField(default=1)  # ligne d'en-tête dans la feuille
    row_count = models.PositiveIntegerField(default=0)
    synced_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class SheetRow(models.Model):
    """Une ligne de données d'un onglet : {nom de colonne: valeur}."""

    table = models.ForeignKey(SheetTable, on_delete=models.CASCADE, related_name="rows")
    position = models.PositiveIntegerField()  # ordre de la ligne dans l'onglet (à partir de 0)
    data = models.JSONField()

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(fields=["table", "position"], name="uniq_sheetrow_table_position"),
        ]

    def __str__(self):
        return f"{self.table_id}#{self.position}"
