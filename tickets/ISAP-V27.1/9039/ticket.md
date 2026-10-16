# #9039 — Migration Ice 3.7 : C++ - Slice2VT

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Core - SDK |
| Catégorie | com.egidium.isap |
| Version cible | ISAP-V27.1 |
| Ticket parent | #9031 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 19/08/2026 10:13 |
| Mis à jour le | 25/09/2026 15:44 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/9039 |

## Description

~~~textile
<pre>
Projet "c:\DEV\EGIDIUM\com.egidium.tools.slice2vt\private\slice2vt.vcxproj" sur le noud 1 (rebuild cible(s)).
_PrepareForClean:
  Suppression du fichier "..\tmp\RELEASE\slice2vt\slice2vt.tlog\slice2vt.lastbuildstate".
InitializeBuildStatus:
  Mise à jour de l'horodatage "..\tmp\RELEASE\slice2vt\slice2vt.tlog\unsuccessfulbuild".
ClCompile:
  C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Tools\MSVC\14.29.30133\bin\HostX86\x86\CL.exe /c /I. /I../../com.zeroc.ice/public/inc /Zi /nologo /W1 /WX- /diagnostics:column /O2 /Oi /Oy- /GL /D WIN32 /D NDEBUG /D _CONSOLE /D _CRT_SECURE_NO_WARNING
  S /D _UNICODE /D UNICODE /Gm- /EHsc /MD /GS /Gy /fp:precise /Zc:wchar_t /Zc:forScope /Zc:inline /Fo"..\tmp\RELEASE\slice2vt\\" /Fd"..\public\bin\slice2vt.pdb" /external:W1 /Gd /TP /analyze- /FC /errorReport:queue Edition.cpp Generation.cpp moduleStructure.cpp slice2vt
  .cpp
  Edition.cpp
  Generation.cpp
  moduleStructure.cpp
  slice2vt.cpp
c:\DEV\EGIDIUM\com.egidium.tools.slice2vt\private\slice2vt.cpp(12,10): fatal error C1083: Impossible d'ouvrir le fichier include : 'Slice/Preprocessor.h' : No such file or directory [c:\DEV\EGIDIUM\com.egidium.tools.slice2vt\private\slice2vt.vcxproj]
Génération du projet "c:\DEV\EGIDIUM\com.egidium.tools.slice2vt\private\slice2vt.vcxproj" terminée (rebuild cible(s)) -- ÉCHEC.


ÉCHEC de la build.

"c:\DEV\EGIDIUM\com.egidium.tools.slice2vt\private\slice2vt.vcxproj" (rebuild cible) (1) ->
(ClCompile cible) ->
  c:\DEV\EGIDIUM\com.egidium.tools.slice2vt\private\slice2vt.cpp(12,10): fatal error C1083: Impossible d'ouvrir le fichier include : 'Slice/Preprocessor.h' : No such file or directory [c:\DEV\EGIDIUM\com.egidium.tools.slice2vt\private\slice2vt.vcxproj]

    0 Avertissement(s)
    1 Erreur(s)


</pre>
~~~

## Historique

### 21/08/2026 14:04 — Alan Raynaud

- Temps estimé : 4.0 h → 8.0 h

~~~textile
Va certainement nécessiter de recompiler slice.lib/slice.dll à partir des sources... si elles existent encore.
~~~

### 21/08/2026 14:28 — Alan Raynaud

- Statut : Nouveau → Bloqué

~~~textile
Question posée directement à ZeroC : https://github.com/orgs/zeroc-ice/discussions/6659
~~~

### 21/08/2026 16:23 — Alan Raynaud

~~~textile
Réponse non-officielle :

> The upgrade guide is silent about it because nothing was renamed or relocated in a way a migration note would cover — the Slice library stopped being public API in 3.7, and there is no successor to point you at.
> 
> In 3.6 those headers sat in the public include tree:
> 
> cpp/include/Slice/Preprocessor.h
> cpp/include/Slice/Parser.h
> cpp/include/Slice/Util.h
> ...
> In 3.7 cpp/include/Slice/ does not exist at all. The same files live at cpp/src/Slice/Preprocessor.h and so on, alongside Grammar.h, GrammarUtil.h and MD5I.h — which is to say they moved from "headers we ship" to "headers that happen to be in the implementation".
> 
> That the missing slice.lib is deliberate rather than a packaging slip is stated outright in the build file, cpp/src/Slice/Makefile.mk:
> 
> # Always enable the static configuration for the Slice library and never
> # install it
> Slice_always_enable_configs     := static
> Slice_always_enable_platforms   := $(build-platform)
> Slice_install_configs           := none
>
> So the library is built static-only, for the build platform, and explicitly never installed. No binary distribution will contain it, and no combination of packages will produce one.
> 
> Worth knowing before you plan around it: this is unchanged in 3.8. The same file on that branch carries the same three settings and the same comment verbatim, so this is not a 3.7 wrinkle that a later release quietly undoes.
> 
> Practically that leaves building the Slice static library yourself out of the Ice source tree, at the exact version you target, and compiling your generator against cpp/src/Slice/. It works — that is how the bundled slice2cpp and friends are built — but you would be pinning to an internal API with no compatibility promise across releases, so expect the parser interfaces your generator touches to move under you on each upgrade, and keep the Ice source pinned rather than tracking a branch. One detail that catches people building it standalone: the library takes a dependency of its own, Slice_libs := mcpp, so the preprocessor you are including has to be linked too.
> 
> Since "official method" is really a question about what ZeroC intends to support, a maintainer answer is worth waiting for — the above establishes what the tree does, not what they recommend. But given the library has been marked never-install for two major versions running, I would plan on the vendored-source route rather than on a public Slice API returning.
~~~

### 01/09/2026 10:34 — Alan Raynaud

- Avancement : 0 % → 100 %

~~~textile
OK en l'état.
~~~

### 02/09/2026 16:14 — Alan Raynaud

- Statut : Bloqué → Résolu

### 25/09/2026 15:44 — Fernand Alcatrao

- Version cible : Candidate for next major release → ISAP-V27.1
