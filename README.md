# PyAssos
_PyAssos_ est une bibliothèque fournissant une interface de connexion avec [l'API _open-source_ du 
Répertoire National des Associations (RNA) fournie par Etalab](https://entreprise.data.gouv.fr/api_doc/rna).

## Fonctionnalités
- La recherche par **nom d'association**
- La recherche par **identifiant RNA**
- La recherche par **son numéro SIRET**

### La recherche par _nom d'association_
La recherche par _nom d'association_ fonctionne grâce à la fonction `recherche_par_nom()`.

La fonction `recherche_par_nom()` prend un argument `nom_cherche` (_string_).
Elle renvoie une liste d'instance de la classe `Association()`.

Si aucun résultat n'a été trouvé, une `ValueError` est levée.

### La recherche par _identifiant RNA_
La recherche par _identifiant RNA_ fonctionne grâce à la déclaration d'une instance `Association()` avec un passage de
l'argument `id_rna`.

Si aucun résultat n'a été trouvé, une `ValueError` est levée.

### La recherche par _numéro de SIRET_
La recherche par _numéro de SIRET_ fonctionne grâce à la déclaration d'une instance `Association()` avec un passage de
l'argument `num_siret`.

Si aucun résultat n'a été trouvé, une `ValueError` est levée.