import requests

# Clé API JCDecaux
api_key = "e0a1bf2c844edb9084efc764c089dd748676cc14"

# URL de l'API JCDecaux
url = "https://api.jcdecaux.com/vls/v3/"

# URL pour récupérer les informations sur les contrats
url_ville = url + "contracts" + "?apiKey=" + api_key


# Récupérer toutes les villes sous contrat
def get_villes():
    response = requests.get(url_ville)
    villes = [ville["name"] for ville in response.json()]
    return villes

villes = get_villes()


# Récupérer le nombre de vélos par ville
def get_velos_par_ville(ville):
    url_velos = url + "stations?contract={}&apiKey={}".format(ville, api_key)
    response = requests.get(url_velos)
    velos = sum(station["mainStands"]["availabilities"]["bikes"] for station in response.json())
    return velos


# Afficher le classement des villes avec le plus grand nombre de vélos
def afficher_classement_villes():
    # Dictionnaire associant chaque ville à son nombre de vélos
    velos_par_ville = {ville: get_velos_par_ville(ville) for ville in villes}
    classement_villes = sorted(velos_par_ville.items(), key=lambda x: x[1], reverse=True)
    print("Classement des villes avec le plus grand nombre de vélos :")
    for i, (ville, velos) in enumerate(classement_villes):
        print(f"{i+1}. {ville} : {velos} vélos")


# Récupérer les informations des vélos en fonction de chaque ville
for ville in villes:
        nb_velos = 0
        ville_url = url + f"stations?contract={ville}&apiKey={api_key}"
        
        # Initialisation/Réinitialisation des variables pour le comptage
        total_stands = 0
        total_bikes = 0
        total_mechanical_bikes = 0
        total_electrical_bikes = 0
        contractName = ""
        
        # Récupérer les données de chaque station
        for station in requests.get(ville_url).json():
            nb_velos += station["mainStands"]["availabilities"]["bikes"]
            total_stands += station["mainStands"]["capacity"]
            contractName += station["contractName"]
            total_mechanical_bikes += station["mainStands"]["availabilities"]["mechanicalBikes"]
            total_electrical_bikes += station["mainStands"]["availabilities"]["electricalBikes"]

            

        # Calcul des pourcentages de vélos mécaniques et électriques
        if nb_velos > 0:
            total_bikes += total_mechanical_bikes + total_electrical_bikes
            percentage_mechanical = (total_mechanical_bikes / total_bikes) * 100
            percentage_electrical = (total_electrical_bikes / total_bikes) * 100
        
        # Empeche la division par 0 lorsqu'il n'y a pas d'information ou qu'il n'y a pas de vélos
        else :
            total_bikes = 0
            percentage_mechanical = 0
            percentage_electrical = 0


        # Affichage des résultats
        print(ville)
        print(f"Nombre total de stands : {total_stands}")
        print(f"Nombre total de vélos disponibles : {total_bikes}")
        print(f"Nombre total de vélos mécaniques disponibles : {total_mechanical_bikes}")
        print(f"Nombre total de vélos électriques disponibles : {total_electrical_bikes}")
        print(f"Pourcentage de vélos mécaniques : {percentage_mechanical:.2f}%")
        print(f"Pourcentage de vélos électriques : {percentage_electrical:.2f}%")
        print(" ")
   
    
# Appeler la fonction d'affichage du classement des villes
afficher_classement_villes()
    
#https://api.jcdecaux.com/vls/v3/stations?contract={ville}&apiKey=e0a1bf2c844edb9084efc764c089dd748676cc14