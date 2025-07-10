### Inleiding
#### Algemeen
In dit document wordt het functioneel ontwerp voor de informatiestandaard Proactieve Zorgplanning (PZP) beschreven. Voor de bijbehorende technische producten, zoals scenario’s en templates, zijn verwijzingen opgenomen naar de bijbehorende documentatie. 
Deze informatiestandaard is van toepassing op het palliatieve zorgdomein binnen Nederland, waarbinnen men zich bezighoudt met de zorg voor patiënten met een (ongeneeslijke) ziekte of andere aandoening waaraan de patiënt naar verwachting zal komen te overlijden. De ontwikkeling van deze informatiestandaard heeft zich voornamelijk geconcentreerd op het faciliteren van netwerkzorg.

Het functioneel ontwerp (FO) beschrijft voor alle vastlegging- en uitwisselscenario's (in dit document use cases genoemd) uit de informatiestandaard de transacties, transactiegroepen, de systemen, de systeemrollen en de bedrijfsrollen van zorgverleners of patiënten. Daarvoor worden de eisen gegeven voor het vastleggen, sturen of ontvangen van gegevens. In hoofdstuk 2 wordt verder ingegaan op wat een use case inhoudt. Per use case zijn de nadere details beschreven. Voor meer informatie over informatiestandaarden en hoe deze worden ontwikkeld, zie de Nictiz webpagina voor informatiestandaarden. Voor de verklaring van de begrippen die voorkomen in het functioneel ontwerp wordt verwezen naar het begrippenoverzicht op de Nictiz website
#### Doelgroep
De doelgroep voor dit document bestaat uit:
* 	Productmanagers, architecten, ontwerpers, beheerders en testers van ziekenhuizen, XIS-leveranciers, regio-organisaties, (kwaliteits)registraties en Nictiz; 
* 	Zorgverleners en vertegenwoordigers van zorgverleners.
####	Kaders en uitgangspunten
Op deze informatiestandaard zijn de uitgangspunten en gebruikersrechten van toepassing zoals deze gelden voor alle informatiestandaarden die ontwikkeld zijn volgens de methodiek van IKNL

######	Richtlijn
De informatiestandaard is (onder meer) gebaseerd op informatie uit de richtlijn Proactieve Zorgplanning van het  Nederlands Huisartsgenootschap (NHG) uit. Deze richtlijn richt zich op wat volgens de huidige maatstaven en beschikbare evidence de beste zorg is voor patiënten in de palliatieve fase.

######	Reikwijdte Informatiestandaard
De reikwijdte van de informatiestandaard beslaat de functionele beschrijvingen en de dataset voor alle gegevensuitwisselingen binnen één of meerdere zorgprocessen. 

Het gaat daarbij om het proces van:
-	vastleggen van PZP informatie ten behoeve van het documenteren van gesprekken;
-	raadplegen van PZP informatie ten behoeve van het leveren van zorg.

######	Wettelijke kaders
Bij de implementatie van deze informatiestandaard dient voldaan te worden aan de wettelijke kaders van de AVG en de toekomstige Wet elektronische gegevensuitwisseling in de zorg (Wegiz). Ook wordt er gekeken naar de impact van de European Health Data Space (EHDS) die voortbouwt op bestaande Europese wetgeving.
####	Kwalificatie (optioneel)
Op basis van dit FO en de daarbij behorende dataset wordt een kwalificatiescript opgesteld. Het opstellen van kwalificatiescripts valt buiten de scope van dit FO. Voor meer informatie zie de webpagina over Nictiz kwalificaties.


###	Use Case(s)
Een use case is een specifieke beschrijving van een praktijksituatie in de zorg waarbij voor een concrete situatie het vastleggen en uitwisselen van informatie wordt beschreven aan de hand van actoren (mensen, systemen) en transacties (welke informatie wordt wanneer uitgewisseld). Een use case is een verbijzondering van een specifiek onderdeel van het zorgproces. Een informatiestandaard kan bestaan uit één of meerdere use cases. Iedere use case koppelt met een scenario in ART-DECOR. Wanneer verschillende use cases gebruik maken van hetzelfde scenario kan een andere indeling gewenst zijn, bijvoorbeeld op basis van proces. In dit FO wordt elke use case geanalyseerd en uitgewerkt.

Deze informatiestandaard gaat uit van onderstaand zorgproces voor palliatieve zorg. Dit zorgproces is een dynamisch proces, zonder vooraf afgebakende stappen of zorgpaden met veel verschillende actoren zoals huisartsen, specialisten, wijkverpleging, maar ook mantelzorgers en de patiënt spelen zelf een belangrijke rol. De behoeften van de patiënt veranderen en de informatiebehoefte van de zorgverleners daarmee ook.  

 
Figuur 1: Overzicht van het verloop van de ziekte in de palliatieve fase.

Binnen het zorgproces en het zorgnetwerk van de patiënt zijn verschillende zorgverleners met verschillende rollen en specialismen (regiebehandelaar, casemanager, huisarts, medisch specialisten, verpleegkundig specialisten, etc.) actief. In dit functioneel ontwerp wordt binnen de use cases vastleggen en raadplegen geen onderscheid gemaakt tussen deze rollen en specialismen omdat de dataset als minimale set geldt , en als geheel wordt behandeld.  Zolang er impliciete toestemming (behandelrelatie of verwijzing) of expliciete toestemming (door patiënt gegeven) is maakt het daarna niet uit welke rol de raadplegende zorgverlener heeft. Deze toestemmingen voor raadplegen en vastleggen kunnen wel per regio of zorgcontext verschillen. Zo kunnen er per organisatie variërende afspraken zijn over wie gegevens mag vastleggen en raadplegen in bepaalde situaties. 

Voor het raadplegen van informatie kan er ook een rol worden aangewezen voor secundaire gebruikers. Ook hiervoor geldt dat zolang er toestemming is, en er wordt voldaan aan wet- en regelgeving dit gebruik door de informatiestandaard kan worden ondersteund. 

De volledige dataset van deze informatiestandaard is hier te vinden. 

Dit hoofdstuk vervolgt met de volgende use cases: 
-	Vastleggen PZP (PZP-EDIT);
-	Raadplegen PZP (PZP-VIEW).
###	Vastleggen van PZP informatie
####	Doel en relevantie
Het doel van deze use case is het vastleggen van PZP informatie op basis van een gesprek over de wensen en grenzen van een patiënt. Zorgverleners registreren deze gegevens voor hun eigen dossiervoering, maar ook om deze te kunnen delen met collega zorgverleners binnen en buiten hun organisatie. Om dit effectief te doen moet PZP informatie eenduidig volgens de informatiestandaard worden geregistreerd.

####	Domein
Deze use case is van toepassing op het palliatieve zorgdomein binnen Nederland, maar is ook breder toepasbaar binnen de algemene bevolking. Het bespreken en vastleggen van wensen en behandelgrenzen voor de toekomst is niet beperkt tot bepaalde ziektebeelden of bevolkingsgroepen.

####	Procesbeschrijving
Het vastleggen van PZP informatie wordt beschreven in de richtlijn PZP.
Deze paragraaf beschrijft voor welke patiëntengroepen in welke fase van het zorgproces deze use case van toepassing is (de preconditie(s)), welke processtap(pen) in scope zijn van deze use case en hoe het proces vervolgt na deze use case (de postconditie(s)).

Preconditie(s)
Om te kunnen vastleggen moet er een gesprek met de patiënt plaatsvinden / zijn geweest waar de benodigde informatie in is besproken, en moet er een systeem beschikbaar zijn waarin gegevens (gestructureerd) kunnen worden ingevuld. 

Processtap(pen) in scope van deze use case
Tijdens of na een contactmoment registreert de zorgverlener de relevante gegevens in het eigen dossier, of in een editor die wordt opgestart met een Single Sign On vanuit het eigen dossier. De inhoudelijke registratie kan op een aantal manieren plaatsvinden:
•	Gestructureerd: registratie volgens het uniform format, in het digitaal invulbaar PDF of in een vergelijkbaar formulier (ACP Formulier)
•	Gestandaardiseerd: registratie in datavelden conform het uniform format of de dataset, met antwoordopties die gecodeerd zijn zoals gedefinieerd in de Informatiestandaard Proactieve Zorgplanning (Dataset PZP) 

Postconditie(s)
Afhankelijk van de gekozen methode van verslaglegging kan vastgelegde informatie door middel van de juiste codestelsels en metadata beter vindbaar, toegankelijk, interoperabel en herbruikbaar (meer FAIR) zijn voor interne en externe samenwerkende zorgverleners met toestemming, en secundaire gebruikers. 

######	Bedrijfsrollen
Binnen het vastleggen van PZP informatie wordt slechts één bedrijfsrol onderscheiden, namelijk de vastleggende zorgverlener zoals te zien is in onderstaande Tabel 1. Vervolgens toont Figuur 2 de verschillende activiteiten uit de procesbeschrijving die door de bedrijfsrol worden uitgevoerd.

Bedrijfsrol	Activiteit(en)
Vastleggende zorgverlener 	Registreert PZP gegevens volgens standaard t.b.v. raadplegen op later moment voor intern collegiaal, extern collegiaal of eigen gebruik. 
	
Tabel 1: De bedrijfsrollen en activiteiten behorende bij het uitvoeren van het Vastleggen PZP
 
Figuur 2: UML activiteitendiagram voor het Vastleggen van PZP informatie
 


######	Systemen & Systeemrollen
De vastleggende zorgverlener maakt gebruik van een informatiesysteem, namelijk een vastleggend/wijzigend (editor) systeem (HIS, EPD, ECD, etc.). Dit systeem kent alleen de rol van vastleggen systeem, zie ook Figuur 3. 

Het Vastleggende systeem vervult één systeemrol, namelijk:
•	PZP_IS – PZP_VASTLEGGEN – EDITOR Systeem (PZP_IS - PZP_EDIT - EDIT)

 
Figuur 3: Component Diagram voor PZP-RAADPLEGEN 

######	Transacties & Transactiegroepen
Het uitwisselen van gegevens tussen de verschillende systeemrollen gebeurt op basis van transacties, een verzameling van transacties (bijvoorbeeld een vraag- en antwoordbericht) vormt een zogeheten transactiegroep.
Figuur 4 toont de samenhang tussen de bedrijfsrollen, bedrijfsprocessen, systeemrollen, transacties en transactiegroepen die onderdeel uitmaken van het PZP_RAADPLEGEN.

 
Figuur 4: Use case Diagram – PZP-RAADPLEGEN

Zoals zichtbaar is in Figuur 4, hebben sommige bedrijfsactiviteiten een bepaalde transactie tot gevolg. Deze transactie wordt uitgevoerd door een systeemrol, en maakt onderdeel uit van een transactiegroep. De gegevenselementen die als onderdeel van de transacties tussen systeemrollen worden uitgewisseld, zijn gespecificeerd in ART-DECOR. Tabel 2 maakt het mogelijk direct de gewenste scenario’s, transactiegroepen, templates en/of transacties te raadplegen in ART-DECOR en FormStudio.

Scenario	Transactiegroep	Template	Transacties
PZP dataset	PZP dataset	PZP dataset o.b.v. zibs2017
PZP dataset o.b.v. zibs2020	PZP dataset vastleggen

ACP formulier 	ACP formulier	ACP formulier o.b.v. zibs2017
ACP formulier o.b.v. zibs2020	ACP formulier invullen

			
Tabel 2: Referenties naar ART-DECOR en naar Template voor PZP dataset .
####	Raadplegen van PZP informatie
######	Doel en relevantie
Het doel van deze use case is het raadplegen van beschikbare PZP informatie. Zorgverleners hebben behoefte aan inzicht in de meest actuele wensen en behandelgrenzen van de patiënt om zo de best passende zorg te kunnen leveren, en het gesprek over huidige en toekomstige zorg gericht aan te kunnen gaan.

Zonder de mogelijkheid tot raadplegen moeten zorgverleners blind handelen, of worden patiënten continu belast met de verantwoordelijkheid om zelf al hun zorgverleners op de hoogte te houden van hun wensen.

Secundair gebruik kan ook binnen de scope van deze use case worden gezien als onderzoekers en kwaliteitsregistraties gebruik willen maken van gegevens die volgens de standaard zijn vastgelegd en daarna zijn geanonimiseerd. 

######	Domein
Deze use case is van toepassing op het palliatieve zorgdomein binnen Nederland, maar is ook breder toepasbaar binnen de zorg bij ziektebeelden zoals parkinson en dementie, en binnen de algemene bevolking. De relevantie van het bespreken en vastleggen van wensen en behandelgrenzen voor de toekomst is niet beperkt tot bepaalde ziektebeelden of bevolkingsgroepen.

######	Procesbeschrijving
Het raadplegen van PZP informatie wordt beschreven in de richtlijn PZP.
Deze paragraaf beschrijft voor welke patiëntengroepen in welke fase van het zorgproces deze use case van toepassing is (de preconditie(s)), welke processtap(pen) in scope zijn van deze use case en hoe het proces vervolgt na deze use case (de postconditie(s)).

Preconditie(s)
Om te kunnen raadplegen moet er informatie beschikbaar zijn, en moet er bekend zijn waar deze informatie zich bevindt. Ook moeten er duidelijke afspraken zijn gemaakt over het beheer en verwerken van toestemmingen om ervoor te zorgen dat alleen personen met de juiste autorisaties bij de gegevens kunnen komen.

Processtap(pen) in scope van deze use case
Voor een contactmoment, of op een ander moment dat een zorgverlener de behoefte heeft om de meest recente en relevante PZP gegevens (PZP dataset en/of het ACP formulier) in te zien. 

Postconditie(s)
De zorgverlener heeft de recente PZP meegenomen in het gesprek met de patiënt en/of naar de laatste PZP informatie gehandeld. Het raadplegen van informatie moet worden gelogd om inzichtelijk te maken wie er wanneer toegang tot de informatie heeft verkregen.  

######	Bedrijfsrollen
Binnen het raadplegen van PZP informatie worden een tweetal bedrijfsrollen onderscheiden, namelijk de beschikbaarstellende zorgverlener en de raadplegende zorgverlener zoals te zien is in onderstaande Tabel 2. Vervolgens toont Figuur 2 de verschillende activiteiten uit de procesbeschrijving die door de bedrijfsrollen worden uitgevoerd.

Bedrijfsrol	Activiteit(en)
Beschikbaar stellende zorgverlener 	Beschikt over (PZP) informatie die geraadpleegd dient te worden 
Raadplegende zorgverlener	Heeft informatiebehoefte waarvoor PZP (informatie) geraadpleegd dient te worden.

Tabel 2: De bedrijfsrollen en activiteiten behorende bij het uitvoeren van het Raadplegen PZP
 
Figuur 5: UML activiteitendiagram voor het Raadplegen van PZP informatie
 


######	Systemen & Systeemrollen
Zowel de Raadplegende zorgverlener als de Beschikbaar stellende zorgverlener maken ieder gebruik van een informatiesysteem, namelijk een raadplegend (viewend) systeem en/of een beschikbaar stellend (bron)systeem (HIS, EPD, ECD, etc.). Deze systemen kennen ieder verschillende systeemrollen, die het proces en uitwisselen van gegevens tussen deze systemen mogelijk maken, zie ook Figuur 6. 

Het Raadplegende systeem vervult één systeemrol, namelijk:
•	PZP_IS – PZP_RAADPLEGEN – VIEWER Systeem (PZP_IS - PZP_VIEW - VIEW)
Het Beschikbaar Stellende Systeem vervult één systeemrollen, namelijk:
•	PZP_IS – PZP_RAADPLEGEN – BRON Systeem (PZP_IS - PZP_VIEW - BRON)

 
Figuur 6: Component Diagram voor PZP_RAADPLEGEN 

######	Transacties & Transactiegroepen
Het uitwisselen van gegevens tussen de verschillende systeemrollen gebeurt op basis van transacties, een verzameling van transacties (bijvoorbeeld een vraag- en antwoordbericht) vormt een zogeheten transactiegroep.
Figuur 7 toont de samenhang tussen de bedrijfsrollen, bedrijfsprocessen, systeemrollen, transacties en transactiegroepen die onderdeel uitmaken van het PZP_RAADPLEGEN.
 
Figuur 7: Use case Diagram – PZP_RAADPLEGEN

Zoals zichtbaar is in Figuur 7, hebben sommige bedrijfsactiviteiten een bepaalde transactie tot gevolg. Deze transactie wordt uitgevoerd door een systeemrol, en maakt onderdeel uit van een transactiegroep. De gegevenselementen die als onderdeel van de transacties tussen systeemrollen worden uitgewisseld, zijn gespecificeerd in ART-DECOR. Tabel 2 maakt het mogelijk direct de gewenste scenario’s, transactiegroepen, templates en/of transacties te raadplegen in ART-DECOR en FormStudio.

Scenario	Transactiegroep	Template	Transacties
PZP dataset	PZP dataset	PZP dataset o.b.v. zibs2017
PZP dataset o.b.v. zibs2020 	PZP dataset raadplegen

ACP formulier	ACP formulier	ACP formulier o.b.v. zibs2017
ACP formulier o.b.v. zibs2020	ACP formulier raadplegen


Tabel 2: Referenties naar ART-DECOR en naar Template voor PZP-Raadplegen.
 
###	Aanwijzingen / eisen voor functionaliteit van systemen
Voor alle scenario’s geldt dat duidelijk dient te zijn welke PZP informatie door wie wanneer als laatste is vastgelegd / gewijzigd.  

###	Verantwoordelijkheid voor informatie
De verantwoordelijkheid voor het vastleggen en beheren van de informatie ligt bij de registrerende zorgverlener. In de situatie dat de informatie buiten het eigen bronsysteem (bijvoorbeeld in een losse editor) wordt ingevoerd blijft deze verantwoordelijkheid bestaan. 

###	Afschermen van gegevens
Alleen relevante gegevens mogen met toestemming worden gedeeld. Hierbij moet rekening worden gehouden met de aanwezigheid van gevoelige persoonsgegevens.

###	Infrastructuur
De beoogde infrastructuur maakt gebruik van zoveel mogelijk bestaande koppelingen en (technische) standaarden. Daarbij moet rekening worden gehouden met de schaalbaarheid van de infrastructuur zodat ook kleine(re) zorgorganisaties en individuele zorgverleners kunnen aansluiten, en huidige en toekomstige wetgeving zoals de EHDS en het FHIR besluit waar nu en in de toekomst aan moet worden voldaan.

Er zal een overgangsperiode zijn waarin zorgverleners en systeembouwers over gaan van een vrije tekst of pdf gebaseerde uitwisseling naar een digitale (FHIR) uitwisseling. Voor deze overgang moet er in de infrastructuur rekening worden gehouden met beide mogelijke methoden voor het invullen en raadplegen van informatie. Het uniform format ACP kan worden ingevuld en opgeslagen als pdf, en deze pdf moet daarna ook inzichtelijk zijn voor zorgverleners die zelf wel al gestructureerd volgens de dataset PZP registreren.  

Leveranciers moeten rekening houden met deze tussenfase waarin het uniform format in een FHIR questionnaire moet worden ingevuld.

  

###	Betrokken partijen en beheer
####	Betrokken partijen
Organisatie	Rol		Verantwoordelijkheden
NHG	Regiehouder	Eindverantwoordelijk voor het ontwikkelen en beheren van een informatiestandaard. De houder bepaalt de scope en het doel van de informatiestandaard, en bepaalt de principes en de uitgangspunten die worden gehanteerd bij ontwikkelen en beheer.
NHG, Verenso, NVAVG V&VN, NPCF, FMS	Autorisatie	Groep van organisaties die de informatiestandaard goedkeurt.
IKNL, NHG en Verenso	Experts	Brengt specifieke expertise in ten behoeve na het ontwikkelen en/of beheren van een informatiestandaard.
IKNL	Functioneel beheerder	Verantwoordelijk voor het proces van ontwikkelen en beheren van een informatiestandaard, binnen de kaders van de gemaakte afspraken en afgesproken governance. 
IKNL en Nictiz 	Technisch beheerder	Verantwoordelijk voor het technisch beheer van een informatiestandaard. Zorgt voor de inrichting en beheer van een technische omgeving die noodzakelijk is om de artefacten die onderdeel zijn van de informatiestandaard te onderhouden.
IKNL en PZNL	Distributeur	Verantwoordelijk voor het distribueren van een informatiestandaard.
Tabel 6: Betrokken partijen
####	Contactinformatie
Voor vragen en/of opmerkingen kun u terecht bij Guido Out, Klinisch Informaticus bij IKNL (g.out@iknl.nl). 
Voor het indienen van wijzigingsvoorstellen kunt u bij IKNL / PZNL terecht. De procedure voor het verwerken van wijzigingsvoorstellen staat Nog nergens beschreven.

####	Beheer 
Deze informatiestandaard behoort tot de informatiestandaarden die wordt beheerd door IKNL. Meer informatie over hoe het beheer geregeld is vindt u hier (LINK NAAR PAGINA). 

###	Referenties
Auteur(s)	Titel	Versie	Datum	Bron	Organisatie
Manon Boddaert, Joep Douma, Floor Dijxhoorn en Maureen Bijkerk	Kwaliteitskader Palliatieve Zorg Nederland	Definitief	14-09-2017	https://palliaweb.nl/richtlijnen-palliatieve-zorg/richtlijn/kwaliteitskader-palliatieve-zorg-nederland
IKNL, Palliactief, PZNL, Patiëntenfederatie Nederland, Verenso, VGVZ, V&VN, FMS, NVPO, NHG, ZN
Richtlijn werkgroep	Richtlijn Proactieve Zorgplanning	Definitief	20-06-2023	https://palliaweb.nl/richtlijnen-palliatieve-zorg/richtlijn/proactieve-zorgplanning 
NHG
Tabel 7: Referenties 

###	Paginahistorie
Versie		Datum		Omschrijving
Versie 0.1.1		30-04-2024		Eerste volledige versie van document
Versie 0.1.2		08-07-2024		Update n.a.v. beta release
Versie 0.1.3		xx-04-2025		Nieuwe links opgenomen naar templates voor uitwerking in zibs2017 en zibs2020.
		
Tabel 8: Paginahistorie

