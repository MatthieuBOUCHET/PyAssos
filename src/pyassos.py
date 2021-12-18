import requests

ADRESSE_VERSION_RACINE = "https://entreprise.data.gouv.fr/api/rna/v1/"

ADRESSE_API_INFO_TEXTE = ADRESSE_VERSION_RACINE + "full_text/"
ADRESSE_API_INFO_RNA = ADRESSE_VERSION_RACINE + "id/"
ADRESSE_API_INFO_SIRET = ADRESSE_VERSION_RACINE + "siret/"


def recherche_par_nom(nom_cherche):
    """Recherche via l'API des associations correspondantes au nom
    recherchées.

    Renvoie une liste d'associations sous forme d'une liste de
    dictionnaires.

    Args:
        nom_cherche -- (string), nom de l'association cherchée
    """
    try:
        requete_api = requests.get(ADRESSE_API_INFO_TEXTE +
                                   str(nom_cherche) +
                                   "?per_page=100")

    except:
        return None

    json_data = requete_api.json()
    listeAssociation = []

    for association in json_data["association"]:
        listeAssociation.append(association)

    if json_data["total_pages"] > 1:
        page=2
        while page <= json_data["total_pages"] and page <= 60:
            requete_api = requests.get(ADRESSE_API_INFO_TEXTE +
                                       str(nom_cherche) +
                                       "?page={}&per_page=100".format(page))

            json_data = requete_api.json()

            for association in json_data["association"]:
                listeAssociation.append(association)

    return listeAssociation


class Association:
    def __init__(self, id_rna=None, num_siret=None, params=None):
        self.id = None  # Numéro Waldec national unique de l’assoc.(STR)
        self.id_ex = None  # Ancien numéro de l'assoc (STR ou None)
        self.siret = None  # N° SIRET
        self.num_utilite_publique = None  # N° d'utilité publique
        self.code_gestion = None  # Code du site gestionnaire de l'asso
        self.date_creation = None  # Date de déclaration de création
        self.date_derniere_declaration = None  # Date de dernière
        # déclaration
        self.date_publi_creation = None  # Date de publication au JO
        self.date_publi_dissolution = None  # Date de déclaration de
        # dissolution
        self.nature = None  # Simplement déclarée 1901 ou autre
        self.groupement = None  # Simple (S);Union (U);Fédération (F)
        self.titre = None  # Nom de l'association
        self.titre_court = None  # Titre court de l'association
        self.objet_social = None  # Objet social de l'association
        self.code_objet_social_1 = None  # Code obligatoire dans la
        # nomenclature nationale
        self.code_objet_social_2 = None  # 2ème code ( facultatif ) dans
        # la nomenclature nationale
        self.adresse_voie = None  # Adresse de l'association
        self.adresse_code_insee = None  # Code INSEE commune
        self.adresse_code_postal = None  # Code postale de la commune
        self.commune = None  # Commune de l'association
        self.pays = None  # Pays de l'association
        self.telephone = None  # Téléphone de l'association
        self.site_web = None  # Site web de l'association
        self.activite = None  # D: Dissoute;S:Supprimée;A:En activité
        self.derniere_maj = None  # Date de MAJ de article




