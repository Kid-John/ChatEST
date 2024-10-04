import sqlite3

conn = sqlite3.connect('domandeQuiz.db')

cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS domande (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               domanda TEXT NOT NULL,
               risposta_1 TEXT NOT NULL,
               risposta_2 TEXT NOT NULL,
               risposta_3 TEXT NOT NULL,
               risposta_corretta TEXT NOT NULL,
               categoria TEXT NOT NULL
               );
               ''')
cursor.execute('''
               CREATE TABLE IF NOT EXISTS utente(
               id_utente INTEGER,
               id_domanda INTEGER,
               risposta_utente TEXT,
               is_correct BOOLEAN,
               FOREIGN KEY(id_domanda) REFERENCES domande(id)
               );
               ''')

domande = [
    ('Qual è l’obiettivo principale del penetration testing?',
    'Migliorare la velocità di rete',
    'Creare un firewall personalizzato',
    'Monitorare l’uso della rete',
    'Identificare vulnerabilità di sicurezza',
    'Penetration Testing'),

    ('Qual è la fase iniziale di un penetration test?',
    'Attacco a forza bruta',
    'Installazione di malware',
    'Manutenzione di sistemi di rete',
    'Raccolta di informazioni (reconnaissance)',
    'Penetration Testing'),

    ('Quale dei seguenti strumenti è comunemente utilizzato nei penetration test per la scansione delle reti?',
    'Wireshark',
    'Metasploit',
    'John the Ripper',
    'Nmap',
    'Penetration Testing'),

    ('Quale attacco mira a indovinare le password durante un penetration test?',
    'Phishing',
    'SQL Injection',
    'DNS Spoofing',
    'Attacco a forza bruta',
    'Penetration Testing'),

    ('Quale fase di un penetration test prevede l’analisi dei danni dopo un attacco simulato?',
    'Attacco iniziale',
    'Installazione di backdoor',
    'Test delle applicazioni web',
    'Post-exploitation',
    'Penetration Testing'),

    ('Qual è una delle principali differenze tra un penetration test(PT) e un vulnerability scan(VS)?',
    'Il VS è più invasivo',
    'Il PT è automatizzato',
    'Il PT trova solo vulnerabilità note',
    'Il PT tenta di sfruttare le vulnerabilità',
    'Penetration Testing'),

    ('Quale attacco sfrutta vulnerabilità nel codice di un’applicazione web durante un penetration test?',
    'Man in the Middle',
    'DDoS',
    'Phishing',
    'SQL Injection',
    'Penetration Testing'),

    ('Qual è l’obiettivo della fase di reporting in un penetration test?',
    'Attivare firewall',
    'Testare malware',
    'Raccogliere credenziali',
    'Documentare vulnerabilità e soluzioni',
    'Penetration Testing'),

    ('Quale attacco tenta di intercettare il traffico tra due parti durante un penetration test?',
    'SQL Injection',
    'Phishing',
    'Brute Force',
    'Man in the Middle',
    'Penetration Testing'),

    ('Qual è lo strumento di penetration testing utilizzato per lanciare exploit noti?',
    'Nmap',
    'Wireshark',
    'Nikto',
    'Metasploit',
    'Penetration Testing'),
    
    ('Qual è lo scopo principale di un vulnerability scan?',
    'Proteggere i firewall',
    'Monitorare le prestazioni di rete',
    'Installare aggiornamenti',
    'Identificare vulnerabilità note nei sistemi',
    'Vulnerability Scanning'),
    
    ('Quale differenza esiste tra un vulnerability scan(VS) e un penetration test?',
    'Il VS è manuale',
    'Il VS verifica solo la rete',
    'Il penetration test è meno invasivo',
    'Il VS cerca vulnerabilità senza sfruttarle',
    'Vulnerability Scanning'),
    
    ('Quale dei seguenti strumenti è utilizzato per il vulnerability scanning?',
    'Wireshark',
    'Burp Suite',
    'John the Ripper',
    'Nessus',
    'Vulnerability Scanning'),
    
    ('Quale vulnerabilità è comunemente rilevata durante un vulnerability scan?',
    'Phishing',
    'Man in the Middle',
    'Attacchi brute force',
    'Patch mancanti nei sistemi',
    'Vulnerability Scanning'),
    
    ('Quando dovrebbe essere eseguito un vulnerability scan?',
    'Solo dopo un incidente di sicurezza',
    'Una volta all’anno',
    'Quando richiesto dai dirigenti',
    'Regolarmente e dopo cambiamenti nei sistemi',
    'Vulnerability Scanning'),
    
    ('Qual è la differenza principale tra un vulnerability scan attivo e passivo?',
    'La velocità di esecuzione',
    'Il numero di vulnerabilità trovate',
    'Il tipo di firewall utilizzato',
    'Coinvolge sistemi scansionati',
    'Vulnerability Scanning'),
    
    ('Qual è una limitazione del vulnerability scanning?',
    'È troppo costoso',
    'Identifica solo malware',
    'Causa downtime significativi',
    'Non rileva vulnerabilità sconosciute',
    'Vulnerability Scanning'),
    
    ('Quale strumento di scanning viene comunemente utilizzato per rilevare vulnerabilità nelle applicazioni web?',
    'Metasploit',
    'Wireshark',
    'Nikto',
    'Burp Suite',
    'Vulnerability Scanning'),
    
    ('Che cosa può causare un falso positivo in un vulnerability scan?',
    'Problemi hardware',
    'Configurazione errata del firewall',
    'Attacchi brute force durante la scansione',
    'Rilevazione errata di configurazioni di rete',
    'Vulnerability Scanning'),
    
    ('Qual è il primo passo da fare dopo aver ricevuto un report da un vulnerability scan?',
    'Ignorare le vulnerabilità non critiche',
    'Contattare il fornitore di software',
    'Ripetere la scansione',
    'Implementare le correzioni',
    'Vulnerability Scanning'),
    
    ('Qual è lo scopo principale di una security code review?',
    'Migliorare la velocità del codice',
    'Testare la sicurezza del network',
    'Monitorare il traffico di rete',
    'Identificare vulnerabilità nel codice',
    'Security Code Review'),
    
    ('Quale vulnerabilità è comunemente identificata durante una security code review?',
    'DDoS',
    'Phishing',
    'Man in the Middle',
    'SQL Injection',
    'Security Code Review'),
    
    ('Quale tecnica è comunemente utilizzata durante una security code review?',
    'Forza bruta',
    'Analisi dinamica del traffico',
    'DNS Poisoning',
    'Analisi statica del codice',
    'Security Code Review'),
    
    ('Che cosa significa "sanitizzazione dell’input" in una security code review?',
    'Inserire commenti nel codice',
    'Crittografare i dati in transito',
    'Aumentare i permessi di esecuzione',
    'Validare e pulire i dati forniti dall’utente',
    'Security Code Review'),
    
    ('Qual è il principio di "least privilege" applicato al codice?',
    'Aumentare le performance del software',
    'Consentire l’accesso root a tutti gli utenti',
    'Consentire l’accesso completo agli sviluppatori',
    'Limitare i permessi al minimo necessario',
    'Security Code Review'),
    
    ('Qual è una delle differenze principali tra una code review(CR) automatica e una manuale?',
    'La CR automatica trova più vulnerabilità',
    'La CR manuale è sempre più veloce',
    'La CR automatica si basa su vulnerabilità note',
    'La CR manuale richiede l’intervento di umani',
    'Security Code Review'),
    
    ('Quale strumento è utilizzato per una security code review automatizzata?',
    'Wireshark',
    'Nmap',
    'Nessus',
    'SonarQube',
    'Security Code Review'),
    
    ('Quale vulnerabilità riguarda l’inserimento di codice dannoso in una query SQL?',
    'Cross-site scripting (XSS)',
    'Man in the Middle',
    'Phishing',
    'SQL Injection',
    'Security Code Review'),
    
    ('Che cosa si cerca di prevenire implementando la validazione dell’input nel codice?',
    'DDoS',
    'Attacchi brute force',
    'Intercettazione di pacchetti',
    'Attacchi di injection',
    'Security Code Review'),
    
    ('Qual è uno dei vantaggi principali di un code review manuale?',
    'È più veloce',
    'Si basa su modelli predefiniti',
    'Non richiede competenze tecniche',
    'Può identificare vulnerabilità complesse',
    'Security Code Review'),
    
    ('Qual è l’obiettivo principale dell’ethical hacking?',
    'Rubare informazioni personali',
    'Bloccare l’accesso a determinati siti web',
    'Accedere illegalmente a un sistema',
    'Migliorare la sicurezza testando vulnerabilità',
    'Ethical Hacking'),
    
    ('Quale strumento è comunemente utilizzato dagli ethical hacker per identificare vulnerabilità di rete?',
    'Burp Suite',
    'Metasploit',
    'Wireshark',
    'Nmap',
    'Ethical Hacking'),
    
    ('Quale tipo di attacco viene simulato dagli ethical hacker per verificare la sicurezza delle credenziali?',
    'Phishing',
    'DDoS',
    'DNS Spoofing',
    'Brute Force',
    'Ethical Hacking'),
    
    ('Qual è il termine che descrive un hacker che lavora con il consenso dell’azienda?',
    'Hacker Black Hat',
    'Hacker Grey Hat',
    'Cybercriminale',
    'Hacker White Hat',
    'Ethical Hacking'),
    
    ('Qual è il tipo di attacco che tenta di manipolare gli utenti per ottenere informazioni sensibili?',
    'Brute Force',
    'SQL Injection',
    'Cross-site scripting (XSS)',
    'Phishing',
    'Ethical Hacking'),
    
    ('Qual è la fase finale di un ethical hacking engagement?',
    'Distribuire malware',
    'Esfiltrare dati',
    'Identificare gli utenti della rete',
    'Redigere un rapporto di vulnerabilità',
    'Ethical Hacking'),
    
    ('Quale tipo di attacco viene comunemente simulato per testare la robustezza dei sistemi aziendali?',
    'DNS Spoofing',
    'Man in the Middle',
    'Cross-site scripting (XSS)',
    'Distributed Denial of Service (DDoS)',
    'Ethical Hacking'),
    
    ('Quale attacco utilizza tecniche di social engineering per ottenere accessi non autorizzati?',
    'SQL Injection',
    'Phishing',
    'Man in the Middle',
    'Brute Force',
    'Ethical Hacking'),
    
    ('Quale dei seguenti è un vantaggio dell’ethical hacking per un’organizzazione?',
    'Rallenta le operazioni aziendali',
    'Aumenta il numero di attacchi',
    'Rende i dati più vulnerabili',
    'Aiuta a prevenire incidenti di sicurezza',
    'Ethical Hacking'),
    
    ('Quale scenario descrive un attacco DoS (Denial of Service)?',
    'Iniettare codice dannoso in una query SQL',
    'Rubare le credenziali dell’utente',
    'Intercettare le comunicazioni tra due parti',
    'Sovraccaricare un server',
    'Ethical Hacking'),


]

cursor.executemany("INSERT INTO domande (domanda, risposta_1, risposta_2, risposta_3, risposta_corretta, categoria) VALUES (?, ?, ?, ? ,?, ?)", domande)
conn.commit()
conn.close()