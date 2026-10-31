
import subprocess
import sys
from pathlib import Path

import luigi

from orchestration.tasks.scraping import ScrapeVideogames

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INGESTION_SCRIPT = PROJECT_ROOT / "scripts_python" / "01_load_dataset.py"


class LoadBronze(luigi.Task):

    def requires(self):
        return ScrapeVideogames()

    def output(self):
        return luigi.LocalTarget(
            str(PROJECT_ROOT / "logs" / "luigi" / "load_bronze.done")
        )

    def run(self):
        print("Démarrage du chargement PostgreSQL...")

        subprocess.run(
            [sys.executable, str(INGESTION_SCRIPT)],
            cwd=PROJECT_ROOT,
            check=True,
        )

        # Création du marqueur après le succès de l'ingestion
        Path(self.output().path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.output().open("w") as marker:
            marker.write("Ingestion PostgreSQL terminée avec succès.")

        print("Chargement Bronze terminé.")
