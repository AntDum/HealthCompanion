## Projet

1. **Objectif principal** :
   - Développer une application Web de suivi de santé qui permet aux utilisateurs (patients) de surveiller divers aspects de leur santé quotidienne et de partager ces informations avec les professionnels de la santé (médecins).

2. **Fonctionnalités principales** :
   - Enregistrement des données de santé quotidiennes telles que la température, la pression artérielle, le pouls, le poids, etc.
   - Gestion des médicaments : permettre aux utilisateurs de suivre les médicaments qu'ils prennent, avec des rappels pour les prises.
   - Suivi de la vaccination : permettre aux utilisateurs de garder une trace de leurs vaccinations, avec des rappels pour les prochaines doses et la date d'expiration des vaccins.
   - Intégration d'un système de rappel de suivi de santé basé sur le dossier médical de l'utilisateur.
   - Interface utilisateur conviviale pour une expérience utilisateur fluide.

3. **Technologies à utiliser** :
   - Python comme langage de programmation pour le backend.
   - Flask pour le développement du backend et la création de l'API REST.
   - CouchDB comme base de données pour stocker les données de santé des utilisateurs.
   - Utilisation de FHIR pour la gestion des données des patients.
   - Intégration de fonctionnalités de rappel à l'aide de bibliothèques Python telles que Flask-Mail pour les rappels par e-mail ou des services de notifications push pour les rappels sur appareil mobile.
   - Création d'un frontend convivial à l'aide de technologies telles que HTML, CSS et JavaScript, éventuellement avec l'utilisation d'un framework comme React ou Angular.

4. **Interface Médecin** :
   - Un portail pour les médecins où ils peuvent accéder aux données de santé de leurs patients.
   - Vue détaillée des données de santé des patients, y compris les médicaments pris, les données de vaccination, etc.
   - Possibilité d'ajouter des notes ou des recommandations pour les patients.

5. **Interface Patient** :
   - Un tableau de bord personnalisé pour chaque patient où ils peuvent voir un aperçu de leurs données de santé.
   - Rappels pour la prise de médicaments et les rendez-vous médicaux.
   - Accès aux informations sur les vaccinations et aux rappels pour les doses à venir.

6. **Sécurité** :
   - Assurer la confidentialité des données de santé en mettant en œuvre des mesures de sécurité appropriées, telles que l'authentification et l'autorisation des utilisateurs.

7. **Test et Déploiement** :
   - Effectuer des tests rigoureux pour garantir le bon fonctionnement de l'application.
   - Déployer l'application sur un serveur sécurisé.

## Interface

### Interface Médecin :

1. **Page de Connexion** :
   - **Titre de la Page** : Centré verticalement et horizontalement en haut de la page.
   - **Formulaire de Connexion** : Centré verticalement et horizontalement au milieu de la page, avec des champs pour le nom d'utilisateur et le mot de passe, et un bouton de connexion en dessous.
   - **Liens de Navigation** : En bas de la page, centrés horizontalement, avec des liens vers la page d'inscription et la récupération du mot de passe.

2. **Tableau de Bord Médecin** :
   - **Barre de Navigation** : Sur le côté gauche de la page, fixée, avec des liens vers les différentes sections du tableau de bord (Gestion des Patients, Consultation des Données de Santé, Ajout de Notes, etc.).
   - **Vue d'Ensemble** : À droite de la barre de navigation, avec des widgets dynamiques affichant les KPI (nombre de patients actifs, rendez-vous à venir, etc.).
   - **Graphiques et Visualisations** : Répartis sur la page principale, centrés et alignés horizontalement, fournissant des visualisations interactives des données de santé des patients.

3. **Gestion des Patients** :
   - **Barre de Recherche** : En haut de la page, centrée horizontalement, permettant de rechercher des patients par nom ou ID.
   - **Liste des Patients** : Sous la barre de recherche, avec chaque entrée de patient affichée dans une liste déroulante, permettant un accès rapide aux dossiers médicaux individuels.

4. **Consultation des Données de Santé** :
   - **Sélection du Patient** : Sur le côté gauche de la page, avec une liste déroulante permettant de sélectionner le patient dont les données de santé doivent être consultées.
   - **Visualisation des Données** : À droite de la sélection du patient, avec des graphiques interactifs affichant les données de santé telles que la température, la pression artérielle, etc.

5. **Ajout de Notes et Recommandations** :
   - **Sélection du Patient** : Comme dans la section précédente, avec une liste déroulante pour choisir le patient concerné.
   - **Formulaire de Saisie** : Centré verticalement et horizontalement, permettant d'ajouter des notes, des recommandations ou des observations au dossier médical du patient.

6. **Rappels de Rendez-vous et Communications** :
   - **Liste des Rappels** : Centrée verticalement et horizontalement sur la page, affichant les prochains rendez-vous médicaux et les rappels de santé importants.
   - **Système de Communication** : En bas de la page, centré horizontalement, avec des options pour envoyer des messages ou des rappels aux patients.

### Interface Patient :

1. **Page de Connexion ou d'Inscription** :
   - **Titre de la Page** : Centré verticalement et horizontalement en haut de la page.
   - **Formulaire de Connexion ou d'Inscription** : Centré verticalement et horizontalement au milieu de la page, avec des champs appropriés et des boutons correspondants.

2. **Tableau de Bord Patient** :
   - **Barre de Navigation** : Sur le côté gauche de la page, fixée, avec des liens vers les différentes sections du tableau de bord (Enregistrement des Données de Santé, Gestion des Médicaments, Rappels et Notifications, etc.).
   - **Vue d'Ensemble** : À droite de la barre de navigation, avec des widgets dynamiques affichant un résumé des données de santé du patient.
   - **Graphiques et Visualisations** : Répartis sur la page principale, centrés et alignés horizontalement, fournissant des visualisations interactives des données de santé enregistrées.

3. **Enregistrement des Données de Santé** :
   - **Section de Saisie des Données** : Centrée verticalement et horizontalement, avec des champs pour enregistrer les données de santé telles que la température, la pression artérielle, etc.
   - **Bouton de Soumission** : Centré sous la section de saisie des données, permettant au patient de soumettre les informations enregistrées.

4. **Gestion des Médicaments et Vaccinations** :
   - **Liste des Médicaments et Vaccinations** : Centrée verticalement et horizontalement, avec des entrées pour chaque médicament ou vaccin, et des boutons pour ajouter, modifier ou supprimer des entrées.

5. **Rappels et Notifications** :
   - **Liste des Rappels et Notifications** : Centrée verticalement et horizontalement, affichant les prochains rendez-vous médicaux, les rappels de prise de médicaments, les vaccinations à venir, etc.
   - **Préférences de Notification** : En bas de la page, centrées horizontalement, avec des options pour choisir les méthodes de notification préférées (e-mail, SMS, notifications push, etc.).

6. **Communication avec le Médecin** :
   - **Boîte de Réception** : Centrée verticalement et horizontalement, affichant les messages et les réponses des médecins, avec des options pour envoyer de nouveaux messages ou poser des questions supplémentaires.
