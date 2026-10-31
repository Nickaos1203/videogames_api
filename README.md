# videogames_api

## Scrapy commandes

- Initialisation de Scrapy :

```bash
scrapy startproject videogames_scrapy
cd videogames_scrapy
```

- Commande de lancement de la collecte de données (se placer dans le 2e dossier videogames_scrapy)

```bash
cd videogames_scrapy
scrapy crawl videogames_spider -O videogames_dataset.json
```

- déplacer le fichier json généré dans le dossier 'scripts_python'

## DBT commandes

- Initialisation du projet DBT :

```bash
dbt init videogames_dbt
```

- Informations de configuration de DBT:

```text
Enter a number : 1
host : localhost
port : 5432
user : [votre nom utilisateur]
pass : [votre mot de passe utilisateur]
dbname : [votre nom de base de données]
schema : silver
threads : 1
```

- Vérification de la connection avec Postgresql :

```bash
dbt debug
````

- Exécution des modèles DBT dans le dossier "model/gold" + test

```bash
dbt run --select path:models/gold
dbt test --select path:models/gold
```
ou 

```bash
dbt build --select path:models/gold
```

- Génération de la documentation des modèles + lancement

```bash
dbt docs generate
dbt docs serve
```



## Streamlit commandes

- lancement de l'application Streamlit (se positionner à la racine du projet) :

```bash
streamlit run streamlit/app.py
```

- " ctrl + c " pour arrêter le serveur

## Luigi (orchestration) commandes

- lancer la pipeline de données (à la racine du projet)

```bash
python -m luigi \
  --module orchestration.pipeline \
  VideogamesPipeline \
  --local-scheduler
```

## FastAPI Commandes

- lancement de l'API à la racine du projet

```bash
uvicorn api.main:app --reload
```

- Accéder à l'API : ```http://127.0.0.1:8000```

- Ctrl + C : Arrêter l'API

## Pytest commandes

- lancer les tests (à la racine du projet)

```bash
python -m pytest tests/ -v
```

