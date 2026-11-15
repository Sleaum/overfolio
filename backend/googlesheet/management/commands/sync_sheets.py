import os

from django.core.management.base import BaseCommand, CommandError

from googlesheet.services import SheetError
from googlesheet.sync import DEFAULT_TABS, sync_sheets


class Command(BaseCommand):
    help = "Recopie les onglets du Google Sheet (portfolio, inout, stock, budget, _history) en base de données."

    def add_arguments(self, parser):
        parser.add_argument(
            "--doc",
            default=os.getenv("GOOGLE_SHEET_DOC_NAME", "overfolio"),
            help="Nom du document Google (ignoré si GOOGLE_SHEET_ID est défini). Défaut : overfolio",
        )
        parser.add_argument(
            "--tabs",
            help="Onglets séparés par des virgules. Défaut : SHEET_SYNC_TABS ou " + ",".join(DEFAULT_TABS),
        )
        parser.add_argument(
            "--header-row",
            action="append",
            default=[],
            metavar="ONGLET=N",
            help="Force la ligne d'en-tête d'un onglet (ex. --header-row portfolio=2). Répétable.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Lit la feuille et affiche ce qui serait enregistré, sans écrire en base.",
        )
        parser.add_argument(
            "--allow-empty",
            action="store_true",
            help="Autorise un onglet vide à remplacer des données existantes.",
        )

    def handle(self, *args, **options):
        tabs = [t.strip() for t in options["tabs"].split(",") if t.strip()] if options["tabs"] else None

        header_rows = {}
        for item in options["header_row"]:
            name, sep, number = item.rpartition("=")
            if not sep or not name or not number.isdigit() or int(number) < 1:
                raise CommandError(f"--header-row attend ONGLET=N avec N >= 1 (reçu : {item!r})")
            header_rows[name] = int(number)

        try:
            results = sync_sheets(
                options["doc"],
                tabs=tabs,
                header_rows=header_rows,
                dry_run=options["dry_run"],
                allow_empty=options["allow_empty"],
            )
        except SheetError as exc:
            raise CommandError(str(exc))

        for r in results:
            if r.ok:
                line = f"{r.tab} : {r.rows} lignes, {len(r.columns)} colonnes (en-tête ligne {r.header_row})"
                if r.message:
                    line += f" - {r.message}"
                self.stdout.write(self.style.SUCCESS(line))
            else:
                self.stdout.write(self.style.ERROR(f"{r.tab} : ÉCHEC - {r.message}"))
            if r.columns:
                shown = ", ".join(r.columns[:12]) + (" …" if len(r.columns) > 12 else "")
                self.stdout.write(f"    colonnes : {shown}")

        failed = [r.tab for r in results if not r.ok]
        if failed:
            raise CommandError("Synchronisation incomplète, onglets en échec : " + ", ".join(failed))
