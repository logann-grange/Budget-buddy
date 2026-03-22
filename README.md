# Projet Budget — Application Bancaire
 
Application de gestion bancaire développée en Python avec CustomTkinter et MySQL.
 
---
 
## Prérequis
 
- Python 3.12+
- MySQL (XAMPP ou autre)
- Bibliothèques Python :
 
```bash
pip install customtkinter mysql-connector-python bcrypt matplotlib
```
 
---
 
## Structure de la base de données
 
Base de données : `banque`
 
### Table `login`
| Colonne | Type         | Description              |
|---------|--------------|--------------------------|
| id      | INT (PK)     | Identifiant unique       |
| Nom     | VARCHAR(255) | Nom de l'utilisateur     |
| Prenom  | VARCHAR(255) | Prénom de l'utilisateur  |
| Email   | VARCHAR(255) | Adresse email (unique)   |
| MDP     | VARCHAR(255) | Mot de passe hashé bcrypt|
 
### Table `compte_bancaire`
| Colonne        | Type          | Description                    |
|----------------|---------------|--------------------------------|
| id             | INT (PK)      | Identifiant unique             |
| login_id       | INT (FK)      | Référence vers `login.id`      |
| numero_compte  | VARCHAR(255)  | Numéro FR + 16 chiffres        |
| solde          | DECIMAL(10,2) | Solde du compte                |
 
### Table `transaction`
| Colonne       | Type          | Description                        |
|---------------|---------------|------------------------------------|
| id            | INT (PK)      | Identifiant unique                 |
| type          | VARCHAR(255)  | `depot`, `retrait` ou `transfert`  |
| description   | TEXT          | Description de la transaction      |
| montant       | DECIMAL(10,2) | Montant de la transaction          |
| date          | DATETIME      | Date et heure                      |
| expediteur_id | INT           | ID du compte expéditeur            |
| receveur_id   | INT           | ID du compte receveur              |
 
> Pour ajouter les colonnes manquantes si besoin :
> ```sql
> ALTER TABLE `transaction`
> ADD COLUMN expediteur_id INT NOT NULL DEFAULT 0,
> ADD COLUMN receveur_id INT NOT NULL DEFAULT 0;
> ```
 
---
 
## Fichiers du projet
 
### Connexion BDD
| Fichier              | Rôle                                      |
|----------------------|-------------------------------------------|
| `bdd_connector.py`   | Crée et retourne la connexion MySQL       |
 
### Logique métier
| Fichier                | Rôle                                                        |
|------------------------|-------------------------------------------------------------|
| `gestion_connexion.py` | Classe `Auth` — inscription, connexion, hachage bcrypt      |
| `Users.py`             | Classe `Users` — liste des comptes, historique, nouveau compte |
| `Compte_bancaires.py`  | Classe `Compte_bancaire` — dépôt, retrait, transfert, solde |
| `transaction.py`       | Classe `Transaction` — représentation d'une transaction     |
| `historique.py`        | Classe `Historique` — filtrage des transactions             |
 
### Interface client
| Fichier                    | Rôle                                                       |
|----------------------------|------------------------------------------------------------|
| `log.py`                   | Page de connexion et d'inscription                         |
| `menu.py`                  | Menu principal client — solde, actions, graphique          |
| `historique_affichage.py`  | Page historique avec filtres (type, montant, date)         |
 
### Interface administrateur (`@labank.com`)
| Fichier                | Rôle                                                        |
|------------------------|-------------------------------------------------------------|
| `menu_bank.py`         | Liste de tous les clients chargée depuis la BDD             |
| `client_account.py`    | Vue admin d'un compte client — mêmes actions que le client  |
| `historique_client.py` | Redirige vers `historique_affichage.py`                     |
 
---
 
## Fonctionnalités
 
### Authentification
- Inscription avec validation complète du mot de passe (10+ caractères, majuscule, chiffre, caractère spécial)
- Connexion avec vérification bcrypt
- Redirection automatique : `@labank.com` → interface admin, autre → interface client
 
### Interface client
- Sélection du compte bancaire via dropdown
- **Dépôt** — ajoute un montant au solde
- **Retrait** — retire un montant (vérifie le solde suffisant)
- **Transfert** — envoie un montant vers un autre compte via son numéro `FR...`
- **Nouveau compte** — crée un compte bancaire supplémentaire
- **Graphique** — courbe d'évolution du solde + barres par type d'opération
- **Historique** — liste des dépenses et revenus avec filtres
 
### Interface administrateur
- Vue de tous les clients avec leur solde
- Accès au compte de n'importe quel client
- Mêmes actions que le client (dépôt, retrait, transfert)
- Accès à l'historique de chaque client
 
### Historique et filtres
- Filtrage par **type** (`depot`, `retrait`, `transfert`)
- Filtrage par **montant** (ex: `100.0`)
- Filtrage par **date** (ex: `2025-01` pour janvier 2025)
- Bouton **Reset** pour réinitialiser les filtres
 
---
 
## Règles mot de passe
 
| Règle                          | Détail                          |
|--------------------------------|---------------------------------|
| Longueur minimale              | 10 caractères                   |
| Lettres + chiffres             | Obligatoire                     |
| Majuscule + minuscule          | Obligatoire                     |
| Caractère spécial              | `! @ # $ % ^ & * ( ) - + _`    |
 
---
 
## Connexion admin
 
Tout email contenant `@labank.com` donne accès à l'interface administrateur.
 
Exemple : `admin@labank.com`
 
---
 
## Notes techniques
 
- Les mots de passe sont hashés avec **bcrypt** avant stockage
- Les numéros de compte sont générés aléatoirement au format `FR` + 16 chiffres
- Le nom `transaction` étant un mot réservé MySQL, toutes les requêtes l'utilisent entre backticks : `` `transaction` ``
- Chaque instance de `Compte_bancaire` ouvre sa propre connexion MySQL pour éviter les conflits de cursor
- Le graphique utilise **matplotlib** intégré dans CustomTkinter via `FigureCanvasTkAgg`

- ---
 
## Auteurs
 
| Nom                  |
|----------------------|
| Logan Grange         |
| Clément Koch         |
| Mohamed Mahamoud     |
