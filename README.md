# Steuerlotse

> **Important**
**This project has been discontinued**

🇬🇧 This is the code repository of the [_Steuerlotse_ ](https://steuerlotse-rente.de) by DigitalService.
You can use this code under the terms of the provided license.
The _Steuerlotse_ is available at: https://steuerlotse-rente.de

With the _Steuerlotse_, taxable pensioners can submit their tax returns online.
The _Steuerlotse_ was specially developed for the tax return of pensioners without additional income.

As early as 2019, four federal states (Brandenburg, Bremen, Mecklenburg-Western Pomerania and Saxony) developed
a simplified tax return in paper form for pensioners. Based on the paper form a
[digital prototype](https://github.com/tech4germany/steuerlotse) was developed as part of the Tech4Germany Fellowship 2020. The fellowship is organized by [DigitalService GmbH des Bundes](https://digitalservice.bund.de).

🇩🇪 Dies ist der Quellcode des [_Steuerlotse_](https://steuerlotse-rente.de) vom DigitalService.
Du kannst den Code unter den Bedingungen der angegebenen Lizenz nutzen.
Der _Steuerlotse_ ist verfügbar unter: https://steuerlotse-rente.de

Mit dem _Steuerlotsen_ können steuerpflichtige Rentner:innen und Pensionär:innen ihre
Steuererklärung online einreichen. Der _Steuerlotse_ wurde extra für die Steuererklärung von Rentner:innen und
Pensionär:innen ohne Zusatzeinkünfte entwickelt.

Bereits 2019 haben vier Bundesländer (Brandenburg, Bremen, Mecklenburg-Vorpommern und Sachsen) eine vereinfachte
Steuererklärung in Papierform für Rentner:innen entwickelt. Auf Basis des Papiervordrucks wurde im Rahmen des
Tech4Germany Fellowships 2020, das von der [DigitalService GmbH des Bundes](https://digitalservice.bund.de)
organisiert wird, von vier Fellows in Kooperation mit dem BMF ein
[digitaler Prototyp](https://github.com/tech4germany/steuerlotse) entwickelt.


## General remarks

🇬🇧
The _Steuerlotse_ will be shut down by the end of year 2022. For this reason the source code will only be mantained and not actively further developped.

🇩🇪
Der Steuerlotse wird zum Endes des Jahres 2022 abgeschaltet. Aus diesem Grund wird der Quellcode nur noch gewartet und nicht weiterentwickelt.


## Contributing

🇬🇧
Everyone is welcome to contribute to the development of the _Steuerlotse_. You can contribute by opening pull requests,
providing documentation or answering questions or giving feedback. Please always follow the guidelines and our
[Code of Conduct](CODE_OF_CONDUCT.md).

🇩🇪  
Jede:r ist herzlich eingeladen, die Entwicklung der _Steuerlotse_ mitzugestalten. Du kannst einen Beitrag leisten,
indem du Pull-Requests eröffnest, die Dokumentation erweiterst, Fragen beantwortest oder Feedback gibst.
Bitte befolge immer die Richtlinien und unseren [Verhaltenskodex](CODE_OF_CONDUCT_DE.md).

### Contributing code

🇬🇧
Open a pull request with your changes, and it will be reviewed by someone from the team. When you submit a pull request,
you declare that you have the right to license your contribution to the DigitalService and the community.
By submitting the patch, you agree that your contributions are licensed under the MIT license.

Please make sure that your changes have been tested before submitting a pull request.

🇩🇪  
Nach dem Erstellen eines Pull Requests wird dieser von einer Person aus dem Team überprüft. Wenn du einen Pull-Request
einreichst, erklärst du dich damit einverstanden, deinen Beitrag an den DigitalService und die Community zu
lizenzieren. Durch das Einreichen des Patches erklärst du dich damit einverstanden, dass deine Beiträge unter der
MIT-Lizenz lizenziert sind.

Bitte stelle sicher, dass deine Änderungen getestet wurden, bevor du einen Pull-Request sendest.

## For Developers 👩‍💻 👨‍💻

### Overview

The two main components are the webapp and erica.

The webapp handles user input, renders html and connects to the PostgresSQL database.

Erica provides an internal API to connect via ERiC (ELSTER Rich Client) with the ELSTER APIs.
Erica has been moved to its own repository here: https://github.com/digitalservicebund/erica.

### Run directly

For developing, we suggest running both webapp and erica locally.
See the following readmes for instructions:

- [webapp/README.md](webapp/README.md)
- [erica_app/README.md](https://github.com/digitalservicebund/erica/blob/main/README.md)

### Run with docker-compose

Alternatively, you can start the application with `docker-compose up`.

Run database migrations and create test data:

```
docker-compose exec web pipenv run flask db upgrade
docker-compose exec web pipenv run flask populate-database
```

Visit the application by pointing your browser at http://localhost.

### Run with docker-compose for development

Copy env file

```bash
# Add the needed parameter values to the copied .env file
cp .env.example .env
cp .erica.env.example .erica.env
```

Login on our docker registry

```bash
docker login $DOCKER_REGISTRY
```

Start our needed services for development
(migrations, testdata and translations will be automatically populated)

```bash
docker-compose -f docker-compose.development.yml up
```

Run database migrations, create test data and translations:

```bash
docker-compose -f docker-compose.development.yml up migrations
```

Start frontend storybook client

```bash
cd ./webapp/client
yarn storybook
```

When docker services are running you can configure IDE(e.g. Pycharm)
to use this docker compose services as python interpreter to debug.
(see .run/Flask (autoapp).run.xml)

### Enviroments

We support four different environments with different configurations:

- Testing
- Development
- Staging
- Production

In the testing environment a mocked version of Erica and the hashing algorithm is used.

### Architecture Decision Records

We will document architecture decision records going forward. If you want to add a new ADR you can use [adr-tools](https://github.com/npryce/adr-tools):

```bash
adr new <title of adr>
```

or the [python version](https://pypi.org/project/adr-tools-python/):

```bash
pipenv run adr-new create <title of adr>
```

Both commands create a new file in doc/adr. Make sure to edit this file to explain the decision.
