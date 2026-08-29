LINK: https://github.com/LosEvons/csb-project-1/

The installation instructions are provided in the top-level README.
For this project I am using the OWASP Top 10, 2021 edition.

This project implements a simple note storage system. Flaws from OWASP Top 10 are built into the program on purpose, and fixes are included in the code. In this essay I will describe the flaws in general terms, explain how they appear in this codebase and show how they are fixed in the code.

FLAW 1: Injection

https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/notes/views.py#L23
Injection happens when hostile data interacts with the program in unintended ways due to missing or incomplete validation or filtering, usually through user input accepting dynamic queries or object-relational mapping search. Injections can lead to sensitive information leaking from databases, or even remote code execution in cases where the injected data is directly handled inside an interpreter. In this application an injection happens during note search, where SQL commands are treated equally with user input inside a Python f-string.
This allows an attacker to access the contents of the database, and extract all notes and even usernames and passwords. SQL injections are a well known class of vulnerability, and easy solutions to them exist in the basic tools used. In this project the issue is solved by passing parameters into the SQL query instead of just executing the query with a Python-native string.
https://github.com/LosEvons/csb-project-1/blob/2d8381a32bfd8afdf5d63b6d968779c94c2c72c3/notes/views.py#L27-L28
By passing user input as parameters, instead of constructing it into the string, we guarantee that any input from the user will not be treated as valid SQL commands, making it impossible for an attacker to escape the intended query and access forbidden information. Another way to fix this issue would be to filter and check the SQL query results after retrieval. 

FLAW 2: Broken access control

https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/notes/views.py#L12
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/notes/views.py#L23
An application has broken access control if users are able to perform actions that exceed their intended permissions. This can happen as a result of missing or lacking authentication when retrieving and passing information inside the program. This flaw, like injection, can lead to the leaking of sensitive information, or fraudulent activity, depending on the victim application in question. In this specific application broken access control is demonstrated in the form of a missing ownership check when notes are retrieved.
Since the notes have small predictable numbers as IDs, it is easy for a malicious or misguided user to access notes not belonging to them. All notes also show up in the search function due to a missing check in the SQL query.
The fix to the flaw is to check ownership on retrieval each time to ensure any retrieval of notes in the future can only access a given note if that note is owned by the accessing party.
https://github.com/LosEvons/csb-project-1/blob/2d8381a32bfd8afdf5d63b6d968779c94c2c72c3/notes/views.py#L13
Additionally, we can filter for ownership in the SQL query to add another level of security to the fix.
https://github.com/LosEvons/csb-project-1/blob/2d8381a32bfd8afdf5d63b6d968779c94c2c72c3/notes/views.py#L27-L28
In general, any application should follow the principle of assigning minimum permissions required to any user, and strictly and consistently enforce the limits of those permissions.

FLAW 3: Cryptographic failures

https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/notes/models.py#L24
A cryptographic failure is when sensitive data is stored or transmitted in an insecure state. For example, storing authentication tokens or passwords in plaintext without encryption makes them vulnerable in case of a data breach happening. In this specific application cryptographic failure is demonstrated in the form of a token being stored in plaintext.
In the event of a data breach, due to social engineering or malware that compromises the admin account for example, this token could be easily extracted and used for malicious purposes. This can be fixed by hashing the token and only storing the hashed token on the server side, and verifying token use against the hash. This leaves the original token only in the custody of the user, and the original token cannot be easily decrypted by an attacker, even if the hash falls into their hands as a result of a data breach.
https://github.com/LosEvons/csb-project-1/blob/347de52bbcf0c178309f03de320aa1723b0c7155/notes/models.py#L25
https://github.com/LosEvons/csb-project-1/blob/347de52bbcf0c178309f03de320aa1723b0c7155/notes/models.py#L29-L31
A good principle of secure design is to really think about who owns a piece of data and who needs it. If the program owns it, it must be held securely. If the program doesn't own it but needs it, it should be handled securely and disposed of as soon as that need ends. In this case, the token is owned by the user, and the program disposes of the original token immediately after one-way hashing it. Now the program has a way of checking the token without actually storing it. In essence, you want your program to own as few things as possible, and secure those few things as tightly as possible.

FLAW 4: Identification and authentication failures

https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/config/settings.py#L94-L107
A failure in identification or authentication results from weak safeguards against identity theft and lacking session management. These failures come in many forms, such as permitting weak credentials. A failure of this kind can lead to an unintended information disclosure or fraudulent activity by an attacker on the account of the hijacked credentials. In this project a failure in authentication is demonstrated by allowing weak passwords, such as "1". The fix is quite simple: we enforce minimum requirements for passwords that guarantee relative safety against brute force attacks or just random lucky guesses.

FLAW 5: Security misconfiguration

https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/config/settings.py#L26
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/config/settings.py#L31
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/config/settings.py#L34
The security of an application can be misconfigured in a multitude of ways that weaken it against attacks or disclose information useful to an attacker. This can take the form of unnecessary features being enabled or installed in the system, security settings being configured too loosely, or error handling revealing stack traces with too much information. In this project a security misconfiguration is shown in three different ways. Firstly by having a secret key visible inside the codebase and committed publicly to version control, which means sensitive information is exposed. Secondly by having the DEBUG setting set to TRUE at all times, which reveals extensive stack traces with information about the program on errors. Thirdly the ALLOWED_HOSTS setting is set to a wildcard, which disables header validation and leaves the application vulnerable to host header attacks.
The issue can be fixed with proper security configuration, which in this case means moving the SECRET_KEY variable to an uncommitted .env file to remove it from public view, setting DEBUG to False to hide verbose stack traces, and restricting ALLOWED_HOSTS to only the intended deployment domains. DEBUG and ALLOWED_HOSTS could also be moved to the .env file to move the security configuration outside version control, and then setting DEBUG to False by default.
https://github.com/LosEvons/csb-project-1/blob/457517d94362868f08b4b4e334f29f2d52652cd9/config/settings.py#L28
https://github.com/LosEvons/csb-project-1/blob/457517d94362868f08b4b4e334f29f2d52652cd9/config/settings.py#L32
https://github.com/LosEvons/csb-project-1/blob/457517d94362868f08b4b4e334f29f2d52652cd9/config/settings.py#L35
