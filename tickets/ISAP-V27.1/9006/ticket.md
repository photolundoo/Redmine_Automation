# #9006 — Installation et configuration de SecurityCenter 5.14

| Champ | Valeur |
|---|---|
| Tracker | Configuration |
| Statut | Résolu |
| Priorité | Haut |
| Version cible | ISAP-V27.1 |
| Ticket parent | #9003 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 10/08/2026 14:30 |
| Mis à jour le | 18/08/2026 11:29 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Lien Redmine | https://srvfr-redmine/issues/9006 |

## Description

(aucune description)

## Pièces jointes

- [clipboard-202608171721-igmn2.png](pieces_jointes/clipboard-202608171721-igmn2.png) — 20 Ko, ajoutée par Alan Raynaud le 17/08/2026 17:21

## Historique

### 10/08/2026 14:31 — Alan Raynaud

- Sujet : « Installation et configuration de SecurityCenter 5.13 » → « Installation et configuration de SecurityCenter 5.14 »
- Version cible : ISAP-V25.1 → ISAP-V27.1
- Avancement : 100 % → 0 %

### 17/08/2026 15:35 — Alan Raynaud

~~~textile
Genetec NOK après migration.

D'après les logs, il semble y avoir un problème dans la base de donnée :
<pre>
2026-08-17T15:29:10.378+02:00, dskfr-orleans, StartupDiagnostics (Debug): >> PersistenceManager::CreateDefaultEntities
2026-08-17T15:29:10.396+02:00, dskfr-orleans, StartupDiagnostics (Performance): Step: 'WFDefaultEntities::CreateDefaultEntities' @ 03:29:10.396 =>  & 17,053s from start (20m0,693s from root)
2026-08-17T15:29:10.486+02:00, dskfr-orleans, StartupDiagnostics (Performance): Step: 'AssemblyLoad: System.Xml.resources, Version=4.0.0.0, Culture=fr, PublicKeyToken=b77a5c561934e089' @ 03:29:10.486 =>  & 17,143s from start (20m0,783s from root)
2026-08-17T15:29:10.929+02:00, dskfr-orleans, SqlCommandWarnings#DirectoryDomain_0 (Warning): SqlException occurred, sql error: 242
Exception:
Microsoft.Data.SqlClient.SqlException (0x80131904): La conversion d'un type de données varchar en type de données datetime a créé une valeur hors limites.
   à Microsoft.Data.SqlClient.SqlConnection.OnError(SqlException exception, Boolean breakConnection, Action`1 wrapCloseInAction)
   à Microsoft.Data.SqlClient.TdsParser.ThrowExceptionAndWarning(TdsParserStateObject stateObj, SqlCommand command, Boolean callerHasConnectionLock, Boolean asyncClose)
   à Microsoft.Data.SqlClient.TdsParser.TryRun(RunBehavior runBehavior, SqlCommand cmdHandler, SqlDataReader dataStream, BulkCopySimpleResultSet bulkCopyHandler, TdsParserStateObject stateObj, Boolean& dataReady)
   à Microsoft.Data.SqlClient.SqlDataReader.TryHasMoreRows(Boolean& moreRows)
   à Microsoft.Data.SqlClient.SqlDataReader.TryReadInternal(Boolean setTimeout, Boolean& more)
   à Microsoft.Data.SqlClient.SqlDataReader.Read()
   à Microsoft.Data.SqlClient.SqlCommand.CompleteExecuteScalar(SqlDataReader ds, Boolean returnLastResult)
   à Microsoft.Data.SqlClient.SqlCommand.ExecuteScalar()
   à Genetec.Data.SqlCommandExtensions.ExecuteWithRetry(ExecuteType action, SqlCommand command, Boolean exposeCommandOnError, Boolean enableRetry, CommandBehavior commandBehavior, SqlTracingState traceSession, Boolean createTraceSessionIfNull)
ClientConnectionId:e31fa799-3d44-4c0f-a638-d82cb9f5615a
Error Number:242,State:3,Class:16
</pre>
~~~

### 17/08/2026 17:19 — Alan Raynaud

~~~textile
Similaire à https://techdocs.genetec.com/r/en-US/KBA-79205-5.12.2.0-Directory-upgrade-fails-when-expansion-server-is-upgraded-first
mais l'erreur n'est pas tout à fait la même
~~~

### 17/08/2026 17:21 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202608171721-igmn2.png

~~~textile
!clipboard-202608171721-igmn2.png!
~~~

### 17/08/2026 18:01 — Alan Raynaud

~~~textile
Problème contourné avec

<pre><code class="sql">
ALTER LOGIN sa WITH DEFAULT_LANGUAGE = us_english;
</code></pre>
~~~

### 18/08/2026 11:29 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %
