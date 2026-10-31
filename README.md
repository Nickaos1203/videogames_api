# Video Games Analytics API

## 1. Présentation du projet

**Video Games Analytics API** est une API REST développée avec FastAPI permettant d'exposer les données dédiées aux jeux vidéo.

Elle s'appuie sur une base de données PostgreSQL (utilisée en tant que Data Warehouse) organisée selon une architecture en médaillon (couches Bronze, Silver et Gold).

L'API exploite les tables du schéma **Gold**, produites par les transformations dbt, afin de mettre à disposition des données structurées et exploitables.

### Objectifs

- Mettre en place un data warehouse et l'architecture en médaillon (bronze, silver, gold).
- Réaliser un pipeline orchestrant la collecte, l'ingestion et la transformation des données de jeux vidéo.
- Exposer les données via une API REST.
- Produire des indicateurs et visualiser les données.

## 2. Architecture et organisation du projet

Le projet **Video Games Analytics** repose sur une architecture modulaire organisée autour de plusieurs composants complémentaires :

- **sql** : création du data warehouse dans postgreSQL via des requêtes SQL.
- **videogames_scrapy** : collecte des données depuis Metacritic avec Scrapy.
- **scripts_python** : ingestion des données brutes dans PostgreSQL avec Python.
- **videogames_dbt** : nettoyage, transformation et modélisation des données avec DBT.
- **orchestration** : orchestration des différentes étapes du pipeline avec Luigi.
- **api** : exposition des données analytiques via une API REST avec FastAPI.
- **dashboard** : visualisation des indicateurs et analyse des données avec Streamlit.

### 2.1 Arborescence générale

```text
videogames_api/
│
├── api/                              # Répertoire de l'API REST FastAPI
│   ├── main.py                         # Initialisation de l'application et des routeurs
│   ├── database.py                     # Connexion PostgreSQL et accès aux tables Gold
│   ├── routers/                        # Dossiers des Endpoints organisés par domaine
│   │   ├── videogames.py                   # Endpoints relatifs aux jeux vidéo
│   │   ├── platforms.py                    # Endpoints relatifs aux plateformes
│   │   ├── genres.py                       # Endpoints relatifs aux genres
│   │   ├── editors.py                      # Endpoints relatifs aux éditeurs
│   │   └── quality.py                      # Endpoints relatifs à la qualité des données
│   └── schemas/                        # Schémas Pydantic des réponses API
│       ├── videogame.py                    # Structure des réponses des jeux vidéo
│       ├── platform.py                     # Structure des réponses des plateformes
│       ├── genre.py                        # Structure des réponses des genres
│       ├── editor.py                       # Structure des réponses des éditeurs
│       └── quality.py                      # Structure des réponses de qualité
│
├── dashboard/                        # Répertoire de l'application de visualisation des données Streamlit
│   ├── app.py                          # Point d'entrée du dashboard
│   ├── db.py                           # Connexion à PostgreSQL et récupération des données
│   └── pages/                        # Dossier comprenant les pages du dashboard
│       ├── editor_analysis.py          # Analyse des éditeurs
│       ├── overview_quality.py         # Vue d'ensemble et indicateurs de qualité
│       └── platform_genre.py           # Analyse des plateformes et des genres
│
├── orchestration/                    # Orchestration du pipeline avec Luigi
│   ├── pipeline.py                     # Définition du pipeline principal
│   └── tasks/                          # Dossiers comprenant les têches d'orchestration
│       ├── scraping.py                     # Exécution du processus de scraping
│       ├── ingestion.py                    # Chargement des données dans PostgreSQL
│       └── transformations.py              # Exécution des transformations et tests dbt
│
├── scripts_python/                   # Répertoire des Scripts Python
│   ├── 00_script_test_connection.py    # Vérification de la connexion à PostgreSQL
│   ├── 01_load_dataset.py              # Ingestion du dataset JSON dans la couche Bronze
│   └── videogames_dataset.json         # Dataset collecté par Scrapy
│
├── sql/                              # Répertoire des Scripts SQL
│   ├── 01_database_init.sql            # Initialisation de la base de données
│   └── 02_test.sql                     # Requêtes SQL de vérification et de test
│
├── tests/                            # Répertoire des Tests automatisés de l'API
│   └── test_api.py                     # Tests fonctionnels des endpoints FastAPI
│
├── videogames_dbt/                   # Répertoire du projet de transformation dbt
│   ├── analyses/                       # Analyses SQL ponctuelles
│   ├── dbt_packages/                   # Dépendances dbt installées
│   ├── logs/                           # Journaux d'exécution dbt
│   ├── macros/                         # Dossiers comprenant les macros dbt
│   │   └── generate_schema_name.sql        # Personnalisation de la génération des schémas
│   ├── models/                         # Dossiers comprenant les modèles dbt
│   │   ├── gold/                           # Modèles analytiques destinés aux utilisateurs
│   │   │   ├── mart_data_quality.sql
│   │   │   ├── mart_editor_performance.sql
│   │   │   ├── mart_genre_performance.sql
│   │   │   ├── mart_platform_performance.sql
│   │   │   ├── mart_videogame_performance.sql
│   │   │   └── schema.yml                      # Documentation et tests des modèles Gold
│   │   ├── silver/                         # Modèles nettoyés et structurés
│   │   │   ├── staging/                        # Modèles de préparation des données brutes
│   │   │   ├── editor.sql            
│   │   │   ├── genre.sql             
│   │   │   ├── platform.sql          
│   │   │   ├── schema.yml                      # Documentation et tests des modèles Silver
│   │   │   ├── videogame_platform.sql
│   │   │   └── videogame.sql        
│   │   └── sources.yml                     # Déclaration des sources de données
│   ├── seeds/                          # Données statiques importables dans dbt
│   ├── snapshots/                      # Gestion de l'historisation des données
│   ├── target/                         # Fichiers générés par dbt
│   ├── tests/                          # Dossier des tests SQL personnalisés
│   │   ├── assert_mart_data_quality_valid.sql
│   │   ├── assert_videogame_platform_unique.sql
│   │   └── assert_videogame_scores_valid.sql
│   ├── dbt_project.yml                 # Configuration du projet dbt
│   ├── packages.yml                    # Déclaration des packages dbt
│   ├── package-lock.yml                # Verrouillage des dépendances
│   └── README.md                       # Documentation du projet dbt
│
├── videogames_scrapy/                # Répertoire du projet de collecte Scrapy
│   ├── videogames_scrapy/
│   │   ├── spiders/
│   │   │   └── videogames_spider.py            # Spider de collecte des jeux vidéo
│   │   ├── items.py                        # Définition des données collectées
│   │   ├── middlewares.py                  # Middlewares Scrapy
│   │   ├── pipelines.py                    # Traitement des éléments collectés
│   │   └── settings.py                     # Configuration du projet Scrapy
│   └── scrapy.cfg                      # Configuration du projet Scrapy
│
├── logs/                             # Fichiers de suivi de l'orchestration
├── .env                              # Variables d'environnement locales
├── .gitignore                        # Fichiers exclus du versionnement Git
├── requirements.txt                  # Dépendances Python du projet
└── README.md                         # Documentation générale du projet
```

### 2.2 Description des composants et procédure d'installation


#### 1. Initialisation du data warehouse – PostgreSQL et SQL

Le répertoire `sql/` regroupe les scripts SQL nécessaires à la préparation de l'environnement de stockage PostgreSQL.

Cette étape permet de mettre en place la base de données, d'organiser les espaces de stockage et de définir les droits d'accès nécessaires aux différents utilisateurs.

- `01_database_init.sql` : initialise l'environnement PostgreSQL, notamment la création de la base de données, des schémas et la configuration des autorisations d'accès.

L'architecture PostgreSQL repose sur trois schémas principaux :

| Schéma | Rôle |
|---|---|
| `bronze` | Stockage des données brutes issues de la collecte |
| `silver` | Stockage des données nettoyées et structurées |
| `gold` | Stockage des modèles analytiques destinés à l'exploitation |

Cette organisation permet de séparer les différentes étapes de transformation des données et de structurer les accès selon les besoins du projet.

#### 2. Collecte des données – Scrapy

Le répertoire `videogames_scrapy/` assure la collecte des informations relatives aux jeux vidéo depuis Metacritic.

- `spiders/videogames_spider.py` : définit les règles de navigation et d'extraction des informations.
- `settings.py` : centralise les paramètres du projet Scrapy.

Le résultat de la collecte est exporté au format JSON dans `scripts_python/videogames_dataset.json`.

#### 3. Ingestion des données – Python

Le répertoire `scripts_python/` regroupe les scripts utilisés pour interagir avec PostgreSQL.

- `00_script_test_connection.py` : vérifie la connexion à la base de données.
- `01_load_dataset.py` : charge le fichier JSON dans la table `bronze.raw_videogames`.

La couche Bronze conserve les données collectées sous leur forme brute, notamment dans une colonne JSONB.

#### 4. Transformation des données – dbt

Le dossier `videogames_dbt/` contient les modèles SQL responsables de la transformation des données.

Le projet adopte une architecture en couches :

**Couche Silver**

- `staging/` : préparation et nettoyage des données issues de Bronze.
- `videogame.sql` : modélisation des jeux vidéo.
- `platform.sql` : référentiel des plateformes.
- `genre.sql` : référentiel des genres.
- `editor.sql` : référentiel des éditeurs.
- `videogame_platform.sql` : modélisation de la relation entre les jeux et leurs plateformes.

**Couche Gold**


| Modèle | Description |
|---|---|
| `mart_videogame_performance` | Indicateurs de performance des jeux vidéo |
| `mart_platform_performance` | Agrégations et scores moyens par plateforme |
| `mart_genre_performance` | Agrégations et scores moyens par genre |
| `mart_editor_performance` | Agrégations et scores moyens par éditeur |
| `mart_data_quality` | Synthèse des contrôles de qualité des données |

Les fichiers `schema.yml` documentent les modèles et définissent les tests génériques dbt. Les tests SQL personnalisés du dossier `tests/` vérifient notamment l'unicité des relations jeux-plateformes, la validité des scores et la cohérence des indicateurs de qualité.

#### 5. Orchestration – Luigi

Le dossier `orchestration/` organise l'exécution des différentes étapes du pipeline de données. Luigi gère les dépendances entre les tâches afin de garantir leur ordre d'exécution.

- `pipeline.py` : définit la tâche principale `VideogamesPipeline`.
- `tasks/scraping.py` : lance la collecte Scrapy.
- `tasks/ingestion.py` : déclenche le chargement des données dans Bronze.
- `tasks/transformations.py` : exécute les commandes dbt `run` et `test`.



#### 6. Exposition des données – FastAPI

Le dossier `api/` expose les données du Data Warehouse à travers une API REST.

Les routeurs sont séparés par domaine fonctionnel :

- `routers/videogames.py` : consultation des jeux vidéo.
- `routers/platforms.py` : consultation des statistiques par plateforme.
- `routers/genres.py` : consultation des statistiques par genre.
- `routers/editors.py` : consultation des statistiques par éditeur.
- `routers/quality.py` : consultation des indicateurs de qualité.

Le fichier `database.py` centralise l'accès aux données PostgreSQL.

Le dossier `schemas/` contient les modèles Pydantic utilisés pour structurer et valider les réponses de l'API.

#### 7. Visualisation – Streamlit

Le dossier `dashboard/` contient l'application de visualisation analytique en Streamlit.

- `app.py` : point d'entrée de l'application Streamlit.
- `db.py` : centralise la connexion à PostgreSQL et l'accès aux données.
- `pages/editor_analysis.py` : propose une analyse des éditeurs.
- `pages/overview_quality.py` : présente une vue d'ensemble de la qualité des données.
- `pages/platform_genre.py` : présente les analyses des plateformes et des genres.

#### 8. Tests et scripts SQL

Le dossier `tests/` contient les tests automatisés de l'API réalisés avec Pytest et FastAPI TestClient.

Le dossier `sql/` contient les scripts d'initialisation et de vérification de PostgreSQL, présentés dans la première étape de l'architecture.

Le dossier `logs/` conserve les fichiers de suivi générés par l'orchestration Luigi.

### 2.3 Flux de données global

Le fonctionnement du projet peut être résumé par le flux suivant :

```text
              METACRITIC
                   |
                   v
          SCRAPY - COLLECTE
                   |
                   v
        videogames_dataset.json
                   |
                   v
         PYTHON - INGESTION
                   |
                   v
          POSTGRESQL BRONZE
                   |
                   v
             DBT - SILVER
          Nettoyage et structuration
                   |
                   v
              DBT - GOLD
           Modèles analytiques
                   |
            +------+------+
            |             |
            v             v
         FASTAPI       STREAMLIT
          API REST      Dashboard
            |             |
            +------+------+
                   |
                   v
          EXPLOITATION DES
          DONNÉES ANALYTIQUES

       LUIGI : ORCHESTRATION
       DES ÉTAPES DU PIPELINE
```

## 3. Installation et lancement du projet

Cette section décrit les étapes nécessaires à l'exécution du pipeline de données ainsi qu'au lancement des applications de visualisation et d'exposition des données.

L'ordre recommandé est le suivant :

### 3.1 Pré-requis et installation du projet

Avant de commencer, les outils suivants doivent être installés sur la machine :

| Outil | Utilisation |
|---|---|
| Git | Clonage et gestion du code source |
| Python 3.13 | Exécution des scripts Python et des applications |
| pip | Installation des dépendances Python |
| PostgreSQL | Stockage des données du Data Warehouse |
| pgAdmin (facultatif) | Administration et exploration de la base PostgreSQL |

Un terminal est également nécessaire pour exécuter les commandes d'installation et de lancement. La procédure est adapté à Linux ou MacOS.

- **Clonage du dépôt GitHub**

Récupérer le code source du projet depuis son dépôt GitHub.

```bash
git clone <URL_DU_DEPOT_GITHUB>
```

Accéder ensuite au répertoire du projet (racine du projet) :

```bash
cd videogames_api
```

- **Création de l'environnement virtuel Python**

Il est recommandé d'utiliser un environnement virtuel afin d'isoler les dépendances du projet des autres installations Python présentes sur la machine.

Créer l'environnement virtuel :

```bash
python3 -m venv .venv
```

Activer l'environnement virtuel sous macOS et Linux :

```bash
source .venv/bin/activate
```

Une fois activé, le nom de l'environnement `(.venv)` apparaît dans le terminal.

Sous Windows, utiliser :

```bash
.venv\Scripts\activate
```

Mettre à jour pip :

```bash
python -m pip install --upgrade pip
```

- **Installation des dépendances**

Le fichier `requirements.txt`, situé à la racine du projet, centralise les dépendances Python nécessaires aux différents composants de l'application.

Installer l'ensemble des dépendances :

```bash
pip install -r requirements.txt
```

Vérifier l'installation des dépendances :

```bash
pip list
```

- **Configuration des variables d'environnement**

À la racine du projet, créer un fichier `.env` contenant les paramètres de connexion à PostgreSQL.

```bash
touch .env
```

Ajouter les variables suivantes en adaptant les valeurs selon la configuration locale de PostgreSQL.
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=videogames_database
DB_USER=your_name
DB_PASSWORD=your_password
```

NB : Le fichier `.env` contient des informations sensibles. Il ne doit pas être publié sur GitHub.

### 3.2 Préparation de PostgreSQL

Sur Pgadmin, ouvrer un "Query Tool". Copier, coller et exécuter les requêtes SQL du fichier `01_database_init.sql` (dans le dossier `sql`). 

Avant l'exécution des requêtes SQL d'autorisation, veuillez adapter`[USER]` avec votre nom d'utilisateur PostgreSQL.

```sql
GRANT USAGE, CREATE ON SCHEMA bronze TO [USER];
GRANT USAGE, CREATE ON SCHEMA silver TO [USER];
GRANT USAGE, CREATE ON SCHEMA gold TO [USER];
```

La base de données "videogames_database" - les schémas "bronze", "silver" et "gold" - ainsi que les autorisations seront créés.


### 3.3 Configuration de dbt

Dbt doit être configuré pour accéder à la base PostgreSQL. Créer le fichier `profiles.yml` dans le répertoire de configuration dbt :

```bash
~/.dbt/profiles.yml
```

Configurer la connexion en fonction du profil déclaré dans `videogames_dbt/dbt_project.yml`.

Exemple de configuration :

```yaml
videogames_dbt:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: your_name
      password: your_password
      port: 5432
      dbname: videogames_database
      schema: public
      threads: 4
```

Le nom `videogames_dbt` doit correspondre à la valeur de `profile` dans `dbt_project.yml`.

Vérifier la connexion :

```bash
dbt debug \
  --project-dir videogames_dbt \
  --profiles-dir ~/.dbt
```

Une connexion valide permet de poursuivre l'exécution du pipeline.

### 3.2 Exécution du pipeline de données avec Luigi

Le pipeline est orchestré avec **Luigi**, qui gère les dépendances et l'ordre d'exécution des différentes tâches.

Il automatise les étapes suivantes :

| Ordre | Tâche | Description |
|---|---|---|
| 1 | Scraping | Collecte des données depuis Metacritic avec Scrapy |
| 2 | Ingestion | Chargement du fichier JSON dans PostgreSQL, schéma Bronze |
| 3 | Transformation | Exécution des modèles dbt avec `dbt run` |
| 4 | Tests | Vérification des transformations avec `dbt test` |

#### Lancement du pipeline complet

Depuis la racine du projet, exécutez la commande suivante dans le terminal :

```bash
python -m luigi \
  --module orchestration.pipeline \
  VideogamesPipeline \
  --local-scheduler
```

Luigi identifie les dépendances entre les tâches et exécute automatiquement les traitements nécessaires.

#### Exécution individuelle des tâches

Il est également possible d'exécuter chaque tâche indépendamment.

**Collecte des données :**

```bash
python -m luigi \
  --module orchestration.tasks.scraping \
  ScrapeVideogames \
  --local-scheduler
```

**Ingestion dans PostgreSQL :**

```bash
python -m luigi \
  --module orchestration.tasks.ingestion \
  LoadBronze \
  --local-scheduler
```

**Transformations et tests dbt :**

```bash
python -m luigi \
  --module orchestration.tasks.transformations \
  TestDbt \
  --local-scheduler
```

#### Suivi de l'exécution

Les fichiers de suivi de Luigi sont enregistrés dans le dossier `logs/luigi/`.

Ils permettent notamment de conserver des marqueurs indiquant la réalisation des différentes tâches.

**Attention :** Luigi utilise ces marqueurs pour déterminer si une tâche est déjà terminée. Si vous souhaitez forcer une nouvelle exécution complète après une modification des données ou du code, supprime les marqueurs concernés :

```bash
rm -f logs/luigi/scrape_videogames.done
rm -f logs/luigi/load_bronze.done
rm -f logs/luigi/dbt_run.done
rm -f logs/luigi/dbt_test.done
rm -f logs/luigi/videogames_pipeline.done
```

Les noms des fichiers doivent correspondre aux chemins réellement définis dans les méthodes `output()` des tâches Luigi.

### 3.3 Lancement du dashboard Streamlit

Le dashboard permet de visualiser et d'explorer les données analytiques produites par le pipeline.

Il s'appuie sur les tables du schéma Gold de PostgreSQL.

Depuis la racine du projet, lancer l'application :

```bash
streamlit run dashboard/app.py
```

Le dashboard est accessible par défaut à l'adresse :

```text
http://localhost:8501
```

#### Fonctionnalités du dashboard

Le dashboard permet d'exploiter les données agrégées et les indicateurs produits par les transformations dbt. L'application propose plusieurs pages d'analyse :

| Page | Fonctionnalités |
|---|---|
| `app.py` | Point d'entrée du dashboard |
| `editor_analysis.py` | Analyse des performances des éditeurs |
| `overview_quality.py` | Visualisation des indicateurs généraux et de qualité des données |
| `platform_genre.py` | Analyse des plateformes et des genres |



### 3.4 Lancement de l'API FastAPI

L'API REST permet d'exposer les données du Data Warehouse à d'autres applications ou services.

Elle est développée avec FastAPI et utilise PostgreSQL comme source de données.

Depuis la racine du projet, lancer le serveur :

```bash
uvicorn api.main:app --reload
```

L'API est accessible à l'adresse :

```text
http://127.0.0.1:8000
```

#### Documentation interactive

FastAPI génère automatiquement une documentation interactive permettant de consulter et de tester les endpoints.

| Interface | Adresse |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

#### Principaux endpoints

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/` | Présentation de l'API |
| GET | `/health` | Vérification de l'état de l'API et de PostgreSQL |
| GET | `/api/v1/games/` | Consultation des jeux vidéo |
| GET | `/api/v1/platforms/` | Statistiques par plateforme |
| GET | `/api/v1/genres/` | Statistiques par genre |
| GET | `/api/v1/editors/` | Statistiques par éditeur |
| GET | `/api/v1/quality/` | Indicateurs de qualité des données |