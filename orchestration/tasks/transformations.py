
import subprocess
import shutil
from pathlib import Path

import luigi

from orchestration.tasks.ingestion import LoadBronze

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DBT_PROJECT_DIR = PROJECT_ROOT / "videogames_dbt"
DBT_PROFILES_DIR = Path.home() / ".dbt"

DBT_EXECUTABLE = shutil.which("dbt")


def run_dbt_command(command):
    if not DBT_EXECUTABLE:
        raise RuntimeError(
            "Commande dbt introuvable. "
            "Vérifie que l'environnement virtuel .venv est activé."
        )

    subprocess.run(
        [
            DBT_EXECUTABLE,
            command,
            "--project-dir",
            str(DBT_PROJECT_DIR),
            "--profiles-dir",
            str(DBT_PROFILES_DIR),
        ],
        cwd=PROJECT_ROOT,
        check=True,
    )


class RunDbt(luigi.Task):

    def requires(self):
        return LoadBronze()

    def output(self):
        return luigi.LocalTarget(
            str(PROJECT_ROOT / "logs" / "luigi" / "dbt_run.done")
        )

    def run(self):
        print("Démarrage des transformations dbt...")

        run_dbt_command("run")

        Path(self.output().path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.output().open("w") as marker:
            marker.write("dbt run terminé avec succès.")

        print("Transformations dbt terminées.")


class TestDbt(luigi.Task):

    def requires(self):
        return RunDbt()

    def output(self):
        return luigi.LocalTarget(
            str(PROJECT_ROOT / "logs" / "luigi" / "dbt_test.done")
        )

    def run(self):
        print("Démarrage des tests dbt...")

        run_dbt_command("test")

        Path(self.output().path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.output().open("w") as marker:
            marker.write("dbt test terminé avec succès.")

        print("Tous les tests dbt sont passés.")
