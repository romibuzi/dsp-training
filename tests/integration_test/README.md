# Le "test d’intégration gratuit"

## En quoi consiste ce test ?

L’objet de ce test est de faire tourner l’ensemble du projet sur un sous-ensemble léger des données brutes pour pouvoir débugger facilement. Il ne s’agit pas d’un test à proprement parler dans le sens où la qualité de l’output du projet n’est pas contrôlée, mais plutôt d’un outil très pratique pour déceler les bugs rapidement et faire tourner le pipeline en mode debug en local facilement.

## Comment ça fonctionne ?

La mécanique principale repose sur la création de variables d’environnement définies dans le fichier [pytest.ini](../../pytest.ini) lors du lancement de tests avec pytest. Cela permet de créer une variable IS_RUNNING_TEST égale à "True", qui est reprise dans le module [src/constants/files.py](../../src/constants/files.py) pour influer sur la valeur prise par la variable DATA_PATH:

- Dans le cas où le code est lancé avec *python main.py*, la variable is_running_test du module [src/constants/files.py](../../src/constants/files.py) prend la valeur par défaut False et DATA_PATH pointe vers [/data](../../data).
- Dans le cas où le code est lancé avec pytest, notamment en exécutant la commande *python -m pytest tests*, is_running_test est égal à True et DATA_PATH pointe vers [/tests/free_integration_test/data](data).

Les données de /tests/free_integration_test/data/raw sont créées à partir de celles de /data/raw grâce à la fonction prepare_raw_test_data (À MODIFIER). Cela permet d’avoir toute la latitude nécessaire à la construction d’un échantillon des données brutes pertinent, et de versionner l’algorithme de construction de cet échantillon. Les données de [/tests/free_integration_test/data/raw](data/raw) sont versionnées pour pouvoir lancer le test indépendamment du téléchargement complet des données brutes (cf [.gitignore du projet](../../.gitignore)).