# PyLogParser

## FR - Parseur et analyseur de log en Python 

Ce script Python est conçu pour analyser des fichiers de logs de serveur et extraire des informations spécifiques sur les requêtes basées sur des plages horaires définies. Il est particulièrement utile pour filtrer et obtenir des informations sur les adresses IP impliquées dans les requêtes, ainsi que pour obtenir des détails supplémentaires tels que le reverse DNS et les informations de géolocalisation.

### Fonctionnalités
- **Filtrage par horodatage** : Le script lit un fichier de log et extrait les lignes dont les horodatages se situent entre deux moments spécifiés.
- **Traitement des adresses IPv4 et IPv6** : Il gère à la fois les adresses IPv4 et IPv6, en retirant le préfixe ::ffff: des adresses IPv4 mappées en IPv6 si nécessaire.
- **Recherche de Reverse DNS** : Pour chaque adresse IP, le script effectue une recherche de reverse DNS.
- **Géolocalisation IP** : Il utilise une base de données GeoIP pour déterminer la localisation géographique de chaque adresse IP.
- **Éviter les doublons** : Le script ne traite pas plusieurs fois la même adresse IP si celle-ci apparaît plusieurs fois dans la plage horaire spécifiée.

### Prérequis
- **Python 3**
- **Bibliothèque geoip2** : Cette bibliothèque peut être installée via pip avec pip install geoip2.
- **Base de données GeoIP** : Vous aurez besoin d'une base de données GeoIP, telle que GeoLite2 de MaxMind, pour la fonctionnalité de géolocalisation.

### Usage
Pour exécuter le script, utilisez la commande suivante dans le terminal :
`python3 parser.py "DD/MMM/YYYY:HH:MM:SS" "DD/MMM/YYYY:HH:MM:SS" logfile.txt`

Ne pas oublier d'importer le fichier `GeoLite2-City.mmdb` au même endroit que le script, disponible à cette adresse : https://github.com/P3TERX/GeoLite.mmdb

Remplacez **DD/MMM/YYYY:HH:MM:SS** par les horodatages de début et de fin, et **logfile.txt** par le chemin du fichier de log à analyser.

### Exemple d'utilisation
`python3 parser.py "13/Nov/2023:10:13:30" "13/Nov/2023:10:15:00" ns1.log`

Cette commande analysera le fichier ns1.log et affichera des informations sur les requêtes effectuées entre 10:13:30 et 10:15:00 le 13 novembre 2023.

Exemple de résultat : 
```
IP: fe80::1712:47a9:127:9f7, Timestamp: 13/Nov/2023:10:13:40, Reverse DNS: tor-exit-56.for-privacy.net, GeoIP: Brandenburg, Germany
IP: 192.168.0.2, Timestamp: 13/Nov/2023:10:13:41, Reverse DNS: Reverse DNS not found, GeoIP: Frankfurt am Main, Germany
IP: 10.10.0.67, Timestamp: 13/Nov/2023:10:13:55, Reverse DNS: tor-exit-52.for-privacy.net, GeoIP: None, Russia
```

### Structure du Code
Le script est structuré comme suit :

#### Définition des fonctions :
**parse_line** : Extrait l'adresse IP et l'horodatage de chaque ligne du fichier de log.
**nslookup** : Réalise une recherche de reverse DNS pour une adresse IP.
**geoip_lookup** : Obtient la localisation géographique d'une adresse IP à partir de la base de données GeoIP.
**filter_log** : Filtre le fichier de log basé sur les horodatages spécifiés et appelle les autres fonctions pour traiter chaque ligne pertinente.

#### Bloc principal :
Le script prend les horodatages de début et de fin, ainsi que le chemin du fichier de log en tant qu'arguments de ligne de commande.

### Licence
Ce script est fourni sous licence MIT. Vous êtes libre de l'utiliser, le modifier et le distribuer, sous réserve des termes de cette licence.
