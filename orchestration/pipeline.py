
import luigi

from orchestration.tasks.transformations import TestDbt


class VideogamesPipeline(luigi.Task):
    """
    Pipeline complet de collecte, d'ingestion et de transformation
    des données de jeux vidéo.
    """

    def requires(self):
        return TestDbt()

    def output(self):
        return luigi.LocalTarget(
            "logs/luigi/videogames_pipeline.done"
        )

    def run(self):
        print("=" * 50)
        print("PIPELINE VIDEOGAMES TERMINE AVEC SUCCES")
        print("=" * 50)

        with self.output().open("w") as marker:
            marker.write("Pipeline terminé avec succès.")
