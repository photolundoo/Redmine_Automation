# #9016 — [SmartShieldWebAPI] Erreur HTTP 500 si le mot de passe du compte API contient un caractère "deux-points"

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | ISAP Core - SDK |
| Catégorie | com.egidium.api |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 12/08/2026 13:20 |
| Mis à jour le | 13/08/2026 14:46 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V5.6.1 |
| Release notes | Oui |
| Lien Redmine | https://srvfr-redmine/issues/9016 |

## Description

(aucune description)

## Historique

### 13/08/2026 14:44 — Alan Raynaud

~~~textile
Pour tester :
# Créer un compte avec un mot de passe contenant un "deux-points"
# Se connecter à l'API avec ce compte et vérifier qu'il n'y a pas d'erreur 500


Exemple avec le compte toto, dont le mdp est "tata:tutu"

Commande :
<pre>
curl -i -k -u toto:toto:toto -X POST https://localhost:5000/api/connect/login
</pre>

Résultat :
<pre>
HTTP/1.1 403 FORBIDDEN
Content-Type: application/json
Content-Length: 38
Date: Thu, 13 Aug 2026 12:37:54 GMT

{
  "error": "Insufficient rights "
}
</pre>

Ici, le résultat est l'erreur 403 (droits insuffisants) ce qui est le résultat attendu car l'utilisateur n'a pas les droits API. 

Avant correctif, le résultat était :

<pre>
HTTP/1.1 500 INTERNAL SERVER ERROR
Content-Type: text/html; charset=utf-8
Content-Length: 0
Date: Thu, 13 Aug 2026 12:43:57 GMT
</pre>
~~~

### 13/08/2026 14:45 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %

~~~textile
Rien à documenter
~~~

### 13/08/2026 14:46 — Alan Raynaud

- Temps estimé : (vide) → 1.0 h
