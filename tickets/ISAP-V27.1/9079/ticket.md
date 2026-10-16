# #9079 — Migration Ice 3.7 : IsapGridGUI

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Core - Configuration |
| Catégorie | com.egidium.isap |
| Version cible | ISAP-V27.1 |
| Ticket parent | #8842 |
| Auteur | Fernand Alcatrao |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 23/09/2026 11:33 |
| Mis à jour le | 25/09/2026 10:26 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/9079 |

## Description

(aucune description)

## Relations

- Liée à #2866

## Historique

### 23/09/2026 11:33 — Fernand Alcatrao

- Relation ajoutée (liée à) : #2866

### 23/09/2026 11:59 — Fernand Alcatrao

- Statut : Nouveau → En cours
- Assigné à : Fernand Alcatrao → Alan Raynaud
- Version cible : Candidate for next major release → ISAP-V27.1
- Avancement : 0 % → 90 %

~~~textile
Procédure inspirée de #2866. J'ai fait sur mon PC dans un répertoire temporaire et pas livré dans le private CVS.
La procédure avec Ice 3.7 (déjà ancien ...) ne fonctionne pas avec un JDK 21. Il faut un JDK 17.
J'ai téléchargé un jdk-17.0.12 sous forme de zip et mis dans @"c:/Program Files/Java/jdk-17.0.12-TODEL"@.

<pre><code class="shell">
cd /c/DEV/SRC-EXTRA
git clone -b 3.7 https://github.com/zeroc-ice/ice.git
cd ice/java
# Chercher chaines contenant "IceGrid GUI" et remplacer par "ISAP Grid" et "Copyright...ZeroC, Inc" par "Copyright...Egidium Technologies"
export PATH="/cygdrive/c/Program Files/Java/jdk-17.0.12-TODEL/bin:$PATH"
export JAVA_HOME="c:/Program Files/Java/jdk-17.0.12-TODEL"
./gradlew.bat build
cpfp ./lib/icegridgui.jar /c/DEV/EGIDIUM/com.egidium.grid/public/bin/IsapGridGUI.jar
</code></pre>

Fichiers modifiées :
<pre>
modified:   src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/Coordinator.java
modified:   src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/ApplicationDetailsDialog.java
modified:   src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/LogFilterDialog.java
modified:   src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/LogPrefsDialog.java
modified:   src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/ObjectDialog.java
modified:   src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/ShowIceLogDialog.java
modified:   src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/ShowLogFileDialog.java
modified:   src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/WriteMessageDialog.java
modified:   src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/Logger.java
modified:   src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/Main.java
modified:   src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/SessionKeeper.java
modified:   src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/XMLWriter.java
</pre>

Diffs:
<pre>
/c/DEV/SRC-EXTRA/ice/java) git diff | grep -e '^[\+\-]'
--- a/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/Coordinator.java
+++ b/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/Coordinator.java
-        getMainFrame().setTitle("IceGrid GUI");
+        getMainFrame().setTitle("Isap Grid");
-                getMainFrame().setTitle(info.getInstanceName() + " (" + _replicaName + ") - IceGrid GUI");
+                getMainFrame().setTitle(info.getInstanceName() + " (" + _replicaName + ") - ISAP Grid");
-                                                                          "This version of IceGrid GUI requires an IceGrid Registry "
+                                                                          "This version of ISAP Grid requires an IceGrid Registry "
-                                          "IceGrid GUI was built without Metrics Graph Support",
-                                          "IceGrid GUI Info",
+                                          "ISAP Grid was built without Metrics Graph Support",
+                                          "ISAP Grid Info",
-                                          "IceGrid GUI Info",
+                                          "ISAP Grid Info",
-        String text = "IceGrid GUI version "
-            + com.zeroc.Ice.Util.stringVersion() + "\n"
-            + "Copyright \u00A9 ZeroC, Inc. All rights reserved.\n";
+        String text = "ISAP Grid version "
+            + "27.1" + "\n"
+            + "Copyright \u00A9 Egidium Technologies. All rights reserved.\n";
-            "About - IceGrid GUI",
+            "About - ISAP Grid",
-            super(owner, "Connection Security Warning - IceGrid GUI");
+            super(owner, "Connection Security Warning - ISAP Grid");
--- a/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/ApplicationDetailsDialog.java
+++ b/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/ApplicationDetailsDialog.java
-        super(root.getCoordinator().getMainFrame(), "Application Details - IceGrid GUI", true);
+        super(root.getCoordinator().getMainFrame(), "Application Details - ISAP Grid", true);
--- a/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/LogFilterDialog.java
+++ b/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/LogFilterDialog.java
-        super(dialog, "Ice log filter - IceGrid GUI", true);
+        super(dialog, "Ice log filter - ISAP Grid", true);
--- a/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/LogPrefsDialog.java
+++ b/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/LogPrefsDialog.java
-        super(dialog, "Preferences - IceGrid GUI", true);
+        super(dialog, "Preferences - ISAP Grid", true);
-        super(dialog, "Preferences - IceGrid GUI", true);
+        super(dialog, "Preferences - ISAP Grid", true);
--- a/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/ObjectDialog.java
+++ b/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/ObjectDialog.java
-              (readOnly ? "" : "New ") + "Dynamic Well-Known Object - IceGrid GUI", true);
+              (readOnly ? "" : "New ") + "Dynamic Well-Known Object - ISAP Grid", true);
--- a/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/ShowIceLogDialog.java
+++ b/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/ShowIceLogDialog.java
-        super(parent.getRoot().getCoordinator().getMainFrame(), title + " - IceGrid GUI", false);
+        super(parent.getRoot().getCoordinator().getMainFrame(), title + " - ISAP Grid", false);
-                setTitle(_title + " (Filtered) - IceGrid GUI");
+                setTitle(_title + " (Filtered) - ISAP Grid");
-                setTitle(_title + " (No filter) - IceGrid GUI");
+                setTitle(_title + " (No filter) - ISAP Grid");
--- a/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/ShowLogFileDialog.java
+++ b/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/ShowLogFileDialog.java
-                                "IceGrid GUI caught: " + e.toString(),
+                                "ISAP Grid caught: " + e.toString(),
-                                "IceGrid GUI caught: " + e.toString(),
+                                "ISAP Grid caught: " + e.toString(),
-        super(root.getCoordinator().getMainFrame(), factory.getTitle() + " - IceGrid GUI", false);
+        super(root.getCoordinator().getMainFrame(), factory.getTitle() + " - ISAP Grid", false);
--- a/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/WriteMessageDialog.java
+++ b/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/LiveDeployment/WriteMessageDialog.java
-        super(root.getCoordinator().getMainFrame(), "Write Message - IceGrid GUI", true);
+        super(root.getCoordinator().getMainFrame(), "Write Message - ISAP Grid", true);
--- a/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/Logger.java
+++ b/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/Logger.java
-        super("IceGrid GUI", "");
+        super("ISAP Grid", "");
-                JOptionPane.showMessageDialog(_mainFrame, message, "Warning - IceGrid GUI Logger",
+                JOptionPane.showMessageDialog(_mainFrame, message, "Warning - ISAP Grid Logger",
-                JOptionPane.showMessageDialog(_mainFrame, message, "Error - IceGrid GUI Logger",
+                JOptionPane.showMessageDialog(_mainFrame, message, "Error - ISAP Grid Logger",
--- a/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/Main.java
+++ b/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/Main.java
-                System.setProperty("com.apple.mrj.application.apple.menu.about.name", "IceGrid GUI");
+                System.setProperty("com.apple.mrj.application.apple.menu.about.name", "ISAP Grid");
-        super("IceGrid GUI");
+        super("ISAP Grid");
--- a/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/SessionKeeper.java
+++ b/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/SessionKeeper.java
-                                    "This version of IceGrid GUI requires a newer IceGrid Registry",
+                                    "This version of ISAP Grid requires a newer IceGrid Registry",
-            initialize("New Connection - IceGrid GUI", parent);
+            initialize("New Connection - ISAP Grid", parent);
-            initialize("Edit Connection - IceGrid GUI", parent);
+            initialize("Edit Connection - ISAP Grid", parent);
-            super(_coordinator.getMainFrame(), "Connection Details - IceGrid GUI", true);
+            super(_coordinator.getMainFrame(), "Connection Details - ISAP Grid", true);
-            super(_coordinator.getMainFrame(), "Saved Connections - IceGrid GUI", true);
+            super(_coordinator.getMainFrame(), "Saved Connections - ISAP Grid", true);
-                                        "Remove Configuration - IceGrid GUI",
+                                        "Remove Configuration - ISAP Grid",
-                                        RequestPasswordResult r = requestPassword("KeyStore Password - IceGrid GUI",
+                                        RequestPasswordResult r = requestPassword("KeyStore Password - ISAP Grid",
-                                                    "Confirm Certificate Update - IceGrid GUI",
+                                                    "Confirm Certificate Update - ISAP Grid",
-                                    "Remove Certificate - IceGrid GUI",
+                                    "Remove Certificate - ISAP Grid",
-                            r = requestPassword("Certificate Password For <" + alias + "> - IceGrid GUI",
+                            r = requestPassword("Certificate Password For <" + alias + "> - ISAP Grid",
-                            "Confirm Certificate Update - IceGrid GUI",
+                            "Confirm Certificate Update - ISAP Grid",
-                            "Confirm Certificate Update - IceGrid GUI",
+                            "Confirm Certificate Update - ISAP Grid",
-            super(_coordinator.getMainFrame(), "Certificate Details - IceGrid GUI", true);
+            super(_coordinator.getMainFrame(), "Certificate Details - ISAP Grid", true);
-            super(_coordinator.getMainFrame(), "Certificate Manager - IceGrid GUI", true);
+            super(_coordinator.getMainFrame(), "Certificate Manager - ISAP Grid", true);
-            super(parent, "Login - IceGrid GUI");
+            super(parent, "Login - ISAP Grid");
-                    super(parent, "Login - IceGrid GUI");
+                    super(parent, "Login - ISAP Grid");
-                    super(parent, "Login - IceGrid GUI");
+                    super(parent, "Login - ISAP Grid");
-                super(parent, "Login - IceGrid GUI");
+                super(parent, "Login - ISAP Grid");
--- a/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/XMLWriter.java
+++ b/java/src/IceGridGUI/src/main/java/com/zeroc/IceGridGUI/XMLWriter.java
-        _writer.write("<!-- This file was written by IceGrid GUI -->" + _newline);
+        _writer.write("<!-- This file was written by ISAP Gridv -->" + _newline);
/c/DEV/SRC-EXTRA/ice/java)
</pre>

Alan pour l'installer, il n'y a plus besoin des paramètres supplémentaires (--add-exports=java.desktop/com.sun.java.swing.plaf.windows=ALL-UNNAMED).
~~~

### 23/09/2026 15:21 — Fernand Alcatrao

~~~textile
Manquait ça !
<pre>
/c/DEV/SRC-EXTRA/ice/java) git diff | grep VerifyDepthMax
-        _verifyDepthMax = properties.getPropertyAsIntWithDefault(prefix + "VerifyDepthMax", 3);
+        _verifyDepthMax = properties.getPropertyAsIntWithDefault(prefix + "VerifyDepthMax", 4);
/c/DEV/SRC-EXTRA/ice/java)
</pre>
~~~

### 25/09/2026 10:26 — Alan Raynaud

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %

~~~textile
Installer serveur màj
~~~
