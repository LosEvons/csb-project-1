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



FLAW 3: Cryptographic failures
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/notes/models.py#L24



FLAW 4: Identification and authentication failures
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/config/settings.py#L94



FLAW 5: Security misconfiguration
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/config/settings.py#L26
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/config/settings.py#L31
https://github.com/LosEvons/csb-project-1/blob/3f9c1a6a928233b37e7e3c46642fef9ffce36f30/config/settings.py#L34
