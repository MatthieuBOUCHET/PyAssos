import requests
import time

ADRESSE_VERSION_RACINE = "https://entreprise.data.gouv.fr/api/rna/v1/"

ADRESSE_API_INFO_TEXTE = ADRESSE_VERSION_RACINE + "full_text/"
ADRESSE_API_INFO_RNA = ADRESSE_VERSION_RACINE + "id/"
ADRESSE_API_INFO_SIRET = ADRESSE_VERSION_RACINE + "siret/"


def recherche_par_nom(nom_cherche: str) -> list or None:
    """Recherche via l'API des associations correspondantes au nom
    recherchées.
    Lors de requêtes mutliples, dans le cas de plusieurs pages de
    résultats, une requête est envoyée toutes les une seconde au maximum
    pour respecter les conditions d'utilisations de l'API.
    Renvoie une liste d'associations sous forme d'une liste de
    dictionnaires.

    Args:
        nom_cherche -- (string), nom de l'association cherchée
    """

    requete_api = requests.get(ADRESSE_API_INFO_TEXTE +
                               str(nom_cherche) +
                               "?per_page=100")

    json_data = requete_api.json()

    listeAssociation = []

    try:
        for association in json_data["association"]:
            listeAssociation.append(Association(paramsAPI=association))

    except KeyError:
        raise ValueError("Aucun résultat n'a été trouvé par l'API.")

    if json_data["total_pages"] > 1:
        page = 2
        while page <= json_data["total_pages"] and page <= 60:
            time.sleep(1)
            # Limite de requête sur l'API pour respecter les conditions
            # de l'API

            requete_api = requests.get(ADRESSE_API_INFO_TEXTE +
                                       str(nom_cherche) +
                                       "?page={}&per_page=100".format(page))

            json_data = requete_api.json()

            for association in json_data["association"]:
                listeAssociation.append(
                    Association(paramsAPI=association))

    return listeAssociation


class Association:
    def __init__(self, id_rna=None, num_siret=None, paramsAPI=None):
        """
        Constructeur de la classe Association.
        Définit les paramètres à None par défaut.

        Si un identifiant RNA ou un numéro SIRET est fournie, alors une
        requête est envoyée sur l'API pour obtenir des informations sur
        l'association en question.
        Si un dictionnaire Python se basant sur un modèle issu de l'API
        alors une instance sera créée avec les données fournies.
        Tout les attributs sont par défaut à None.

        Il ne faut fournir qu'un seul argument lors de la création de
        l'instance (soit un identifiant RNA, soit un numéro de SIRET ou
        un dictionnaire Python provenant de l'API RNA).
        Si plusieurs arguments sont fournis, il n'y en aura qu'un de
        traité. L'ordre de traitement est hiérarchiquement :
        - L'identifiant RNA (id_rna)
        - Le numéro de SIRET (num_siret)
        - Le dictionnaire provenant de l'API RNA (paramsAPI)

        Args:
            id_rna: (str), identifiant RNA
            num_siret: (str) ou (int), numéro de SIRET
            paramsAPI: (dict), dictionnaire provenant de l'API RNA
        """
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
        self.adresse = None  # Adresse de l'association
        self.code_insee = None  # Code INSEE commune
        self.code_postal = None  # Code postale de la commune
        self.commune = None  # Commune de l'association
        self.pays = None  # Pays de l'association
        self.telephone = None  # Téléphone de l'association
        self.email = None  # Courriel de l'asssociation
        self.site_web = None  # Site web de l'association
        self.activite = None  # D: Dissoute;S:Supprimée;A:En activité
        self.derniere_maj = None  # Date de MAJ de article
        self.observations = None  # Observations sur l'association

        if id_rna is not None:
            """Requête sur numéro RNA"""

            requete_api = requests.get(ADRESSE_API_INFO_RNA +
                                       str(id_rna))

            json_data = requete_api.json()

            try:
                association = json_data["association"]
                self.set_attributs_api(association)
            except KeyError:
                # Si aucune association trouvée
                raise ValueError("Le numéro RNA fournit ne correspond à"
                                 "aucune association connue")

        elif paramsAPI is not None:
            """Construction d'une instance à partir d'un dictionnaire
            obtenue via l'API"""

            if type(paramsAPI) is not dict:
                raise ValueError("Les paramètres de l'association n'est"
                                 "pas un dictionnaire")

            self.set_attributs_api(paramsAPI)

        elif num_siret is not None:
            """Requête sur numéro RNA"""

            requete_api = requests.get(ADRESSE_API_INFO_SIRET +
                                       str(num_siret))

            json_data = requete_api.json()

            try:
                association = json_data["association"]
                self.set_attributs_api(association)
            except KeyError:
                # Si aucune association trouvée
                raise ValueError("Le numéro SIRET fournit ne correspond"
                                 "à aucune association connue")

        else:
            raise ValueError("Merci de préciser au moins un argument "
                             "(Identifiant RNA, numéro SIRET ou un"
                             "dictionnaire Python issue de l'API")

    def set_attributs_api(self, donnees: dict) -> None:
        """
        Définit les attributs de l'objet par rapport aux données
        fournies.
        Si aucune donnée n'est fournie pour un attribut, alors
        l'attribut vaut None

        Args:
            donnees: (dict), données provenant de l'API ou sous le même
        format

        Returns:
            None

        """
        try:
            self.id = donnees["id_association"]
            self.id_ex = donnees["id_ex_association"]
            self.siret = donnees["siret"]
            self.num_utilite_publique = donnees["numero_reconnaissance_"
                                                "utilite_publique"]
            self.code_gestion = donnees["code_gestion"]
            self.date_creation = donnees["date_creation"]
            self.date_derniere_declaration = donnees["date_derniere_"
                                                     "declaration"]
            self.date_publi_creation = donnees["date_publication_"
                                               "creation"]

            self.date_publi_dissolution = donnees["date_declaration_"
                                                  "dissolution"]
            self.nature = donnees["nature"]
            self.groupement = donnees["groupement"]
            self.titre = donnees["titre"]
            self.titre_court = donnees["titre_court"]
            self.objet_social = donnees["objet"]
            self.code_objet_social_1 = donnees["objet_social1"]
            self.code_objet_social_2 = donnees["objet_social2"]
            self.code_postal = donnees["adresse_code_postal"]
            self.code_insee = donnees["adresse_code_insee"]
            self.commune = donnees["adresse_libelle_commune"]
            self.pays = donnees["adresse_gestion_pays"]
            self.adresse = "{}, {} {} {} {}".format(
                donnees["adresse_gestion_geo"],
                donnees["adresse_gestion_libelle_voie"],
                self.code_postal,
                self.commune,
                self.pays
            )
            self.telephone = donnees["telephone"]
            self.email = donnees["email"]
            self.site_web = donnees["site_web"]
            self.observations = donnees["observation"]
            self.activite = donnees["position_activite"]
            self.derniere_maj = donnees["derniere_maj"]

        except KeyError:
            raise ValueError("Les données ne semblent pas provenir de"
                             "l'API")

        return None

