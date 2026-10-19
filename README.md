# AXEN — Site vitrine

**Avec AXEN, faites bonne impression !**

Site vitrine statique, responsive, accessible et sans dépendance de build, prévu pour **GitHub Pages**.

## Pages et sections

- Accueil avec présentation, illustration originale d'un photocopieur et slogan officiel.
- Solutions : multifonctions, imprimantes professionnelles, numérisation et gestion du parc.
- Services : conseil, configuration, mise en place, suivi/maintenance selon prestation.
- Approche commerciale, profils professionnels, bonnes pratiques et FAQ.
- Formulaire de préparation de demande d'information (via messagerie de l'utilisateur après configuration).
- Mentions légales et confidentialité (données de l'éditeur **à compléter**).

## Charte et logo

Les logos vectoriels proviennent du dépôt maître [AXEN Branding](https://github.com/kesurof/AXEN). Les copies nécessaires à l'affichage sont dans `assets/brand/`, sans appels vers un dépôt privé ou un CDN externe. Les assets source ne doivent pas être redessinés.

## Lancer localement

```bash
python3 -m http.server 8080
# ouvrir http://localhost:8080
```

La navigation locale ne nécessite aucune installation. Pour générer les PNG sociaux et les favicons (comme dans le déploiement) :

```bash
python3 -m pip install 'CairoSVG>=2.7,<3' 'tinycss2>=1.2,<2'
python3 scripts/check_site.py
python3 scripts/build_site.py
python3 -m http.server --directory dist 8080
```


## Déploiement GitHub Pages

Fichier : `.github/workflows/deploy-pages.yml`. À chaque push sur `main`, les fichiers sont publiés à l'aide de `actions/configure-pages`, `upload-pages-artifact` et `deploy-pages`.

1. Dans **Settings → Pages → Build and deployment**, sélectionner **Source : GitHub Actions**. L'action nécessite l'activation du site dans les paramètres Pages.
2. Vérifier **Settings → Actions → General** (les workflows doivent être autorisés).
3. Examiner l'onglet **Actions**, workflow **Publier le site AXEN sur GitHub Pages**.
4. URL cible (si Pages est activé) : `https://kesurof.github.io/axen-web/`.

**Attention :** sur GitHub Free, Pages exige un **dépôt public**. Les dépôts privés ont besoin d'un plan GitHub compatible. Le workflow seul ne peut pas changer la visibilité du dépôt ni activer Pages sans autorisations administratives adaptées.

## Informations à compléter avant exploitation commerciale

- Dans `site-config.js`, renseigner `contactEmail` avec **l'adresse professionnelle AXEN vérifiée** ; sinon le formulaire **ne peut pas envoyer la demande**, et prépare seulement un texte copiable.
- Remplacer les informations légales à compléter dans `mentions-legales.html` et `confidentialite.html` (SIREN, dénomination, adresse, responsable de publication, responsable de traitement).
- Valider la réalité et les modalités des services présentés (notamment maintenance et installation) avant communication commerciale officielle.
- Renseigner éventuellement un nom de domaine propre à AXEN et mettre à jour `canonical`, métadonnées Open Graph, robots et sitemap.

Aucun chiffre, nom de client, adresse, numéro de téléphone, zone d'intervention ou certification n'a été inventé.

## Confidentialité et fonctionnement

Aucun traceur, SDK publicitaire, base de données ni traitement serveur. Le formulaire côté client prépare un `mailto:` si une adresse est configurée. Le bouton n'envoie jamais une demande automatiquement : c'est l'utilisateur qui valide dans son logiciel de messagerie. En l'absence de destinataire, le texte est copié si le navigateur l'autorise.

## Maintenance

Le site a été conçu en HTML/CSS/JS natifs. Les chemins d'assets sont relatifs pour fonctionner sur le sous-chemin `/axen-web/`. Vérifier la version mobile et les liens avant toute mise à jour majeure.


## Pages détaillées des solutions

Chaque carte **En savoir plus** de la page d'accueil ouvre désormais sa véritable fiche (textes sur les usages, fonctionnalités, critères de choix et questions courantes). Ce contenu est statique, lisible sans JavaScript et inclus dans le sitemap :

- `solutions/photocopieurs-multifonctions.html`
- `solutions/imprimantes-professionnelles.html`
- `solutions/numerisation-documents.html`
- `solutions/gestion-parc-impression.html`

Le script `scripts/check_site.py` contrôle aussi les liens entre pages et les fragments d'ancrage. Le script `scripts/build_site.py` copie le dossier `solutions/` dans `dist/` pour GitHub Pages.


## Site de démonstration (octobre 2026)

AXEN est utilisé ici pour un **cas d'étude fictif**. Tous les avis sont inventés : la rubrique porte la mention « Avis fictifs » et chaque carte est marquée « EXEMPLE FICTIF ». Un badge discret « SITE DE DÉMONSTRATION » reste affiché sur toutes les pages, et la mention figure en pied de page.

Deux illustrations premium au format WebP remplacent les anciennes photos sombres : `assets/photos/copier-hero-office.webp` (mise en situation) et `assets/photos/copier-feature-studio.webp` (vue studio). Les visuels ont été générés pour la maquette. Ils ne sont **pas des photographies officielles**, ne prouvent aucun partenariat fournisseur et ne présentent pas des modèles contractuels. Voir `credits-photos.html`.

Les pages restent hébergées localement dans GitHub Pages, sans téléchargement d'images externes lors du build. Une future utilisation commerciale impose de retirer les avis fictifs et de valider les mentions légales et les visuels.
