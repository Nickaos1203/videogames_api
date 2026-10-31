
import subprocess
from pathlib import Path

import luigi

# Chemin racine du projet
PROJECT_ROOT = Path(__file__).resolve().parents[2]

## répertoire d'exécution de scrapy
SCRAPY_DIR = PROJECT_ROOT / "videogames_scrapy"

OUTPUT_FILE = (
    PROJECT_ROOT
    / "scripts_python"
    / "videogames_dataset.json"
)


class ScrapeVideogames(luigi.Task):

    def output(self):
        return luigi.LocalTarget(str(OUTPUT_FILE))

    def run(self):
        command = [
            "scrapy",
            "crawl",
            "videogames_spider",
            "-O",
            "../scripts_python/videogames_dataset.json",
        ]

        subprocess.run(
            command,
            cwd=SCRAPY_DIR,
            check=True,
        )

        print(f"Scraping terminé : {OUTPUT_FILE}")
