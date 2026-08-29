LINK: https://github.com/LosEvons/csb-project-1/

The installation instructions are provided in the top-level README.
For this project I am using the OWASP Top 10, 2021 edition.

This project implements a simple note storage system. Flaws from OWASP Top 10 are built into the program on purpose, and fixes are included in the code. In this essay I will describe the flaws and show how to fix them.

FLAW 1: Injection

Injection happens when hostile data interacts with the program in unintended ways due to missing or incomplete validation or filtering, usually through user input accepting dynamic queries or object-relational mapping search. Injections can lead to sensitive information leaking from databases, or even remote code execution in cases where the injected data is directly handled inside an interpreter. In this application an injection happens during note search, where SQL commands are treated equally with user input inside a Python f-string.
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/notes/views.py#L23
This allows an attacker to access the contents of the database, and extract all notes and even usernames and passwords. SQL injections are so well known, that easy solutions to them exist. In this project the issue is solved by passing parameters into the SQL query instead of just executing the query with a Python-native string.
https://github.com/LosEvons/csb-project-1/blob/2d8381a32bfd8afdf5d63b6d968779c94c2c72c3/notes/views.py#L27-L28
By passing user input as parameters, instead of constructing it into the string, we guarantee that any input from the user will not be treated as valid SQL commands, making it impossible for an attacker to escape the intended query and access forbidden information.

FLAW 2: Broken access control

An application has broken access control if users are able to perform actions that exceed their intended permissions. This, like injection, can lead to the leaking of sensitive information, or fraudulent activity, depending on the application in question. In this specific application broken access control is demonstrated in the form of a missing ownership check.
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/notes/views.py#L12
Since the notes have small predictable numbers as IDs, it is easy for a malicious or misguided user to access notes not belonging to them. All notes also show up in the search function due to a missing check in the SQL query.
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/notes/views.py#L23
The fix to the flaw is to check ownership on retrieval each time to ensure any retrieval of notes in the future can only access a given note if that note is owned by the accessing party.
https://github.com/LosEvons/csb-project-1/blob/2d8381a32bfd8afdf5d63b6d968779c94c2c72c3/notes/views.py#L13
Additionally, we can filter for ownership in the SQL query to add another level of security to the fix.
https://github.com/LosEvons/csb-project-1/blob/2d8381a32bfd8afdf5d63b6d968779c94c2c72c3/notes/views.py#L27-L28

FLAW 3: Cryptographic failures

A cryptographic failure is when sensitive data is stored or transmitted in an insecure state. For example, storing authentication tokens or passwords in plaintext without encryption makes them vulnerable in case of a data breach happening. In this specific application cryptographic failure is demonstrated in the form of a token being stored in plaintext.
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/notes/models.py#L24
In the event of a data breach, due to social engineering or malware that compromises the admin account for example, this token could be easily extracted and used for malicious purposes. This can be fixed by hashing the token and only storing the hashed token on the server side, and verifying token use against the hash. This leaves the original token only in the custody of the user, and the original token cannot be easily decrypted by an attacker, even if the hash falls into their hands as a result of a data breach.
https://github.com/LosEvons/csb-project-1/blob/347de52bbcf0c178309f03de320aa1723b0c7155/notes/models.py#L25
https://github.com/LosEvons/csb-project-1/blob/347de52bbcf0c178309f03de320aa1723b0c7155/notes/models.py#L29-L31

FLAW 4: Identification and authentication failures

A failure in identification or authentication results from weak safeguards against identity theft and lacking session management. These failures come in many forms, such as permitting weak credentials. A failure of this kind can lead to an unintended information disclosure or fraudulent activity by an attacker on the account of the hijacked credentials. In this project a failure in authentication is demonstrated by allowing weak passwords, such as "1". The fix is quite simple: we enforce minimum requirements for passwords that guarantee relative safety against brute force attacks or just random lucky guesses.
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/config/settings.py#L94-L107

FLAW 5: Security misconfiguration

The security of an application can be misconfigured in a multitude of ways that weaken it against attacks or disclose information useful to an attacker. This can take the form of unnecessary features being enabled or installed in the system, security settings being configured too loosely, or error handling revealing stack traces with too much information. In this project a security misconfiguration is shown in three different ways. Firstly by having a secret key visible inside the codebase and committed publicly to version control, which means sensitive information is exposed. Secondly by having the DEBUG setting set to TRUE at all times, which reveals extensive stack traces with information about the program on errors. Thirdly the ALLOWED_HOSTS setting is set to a wildcard, which disables header validation.
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/config/settings.py#L26
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/config/settings.py#L31
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/config/settings.py#L34
