const translations = {
  errors: {
    warningImage: {
      ariaLabel: "Fehlermeldung",
    },
  },
  button: {
    help: {
      ariaLabel: "Weitere Informationen",
    },
    close: {
      ariaLabel: "Schließen",
    },
  },
  dropDown: {
    defaultOption: "Bitte auswählen",
  },
  form: {
    optional: "optional",
    back: "Zurück",
    backToOverview: "Zurück zur Übersicht",
    next: "Weiter",
    logout: {
      button: "Abmelden",
      title: "Sind Sie sicher, dass Sie sich abmelden möchten?",
      intro:
        "Ihre bisher eingetragenen Angaben werden erst an uns übermittelt, wenn Sie Ihre Steuererklärung verschicken. Ihre Steuererklärung wird daher nicht zwischengespeichert. Wenn Sie sich abmelden, kann es sein, dass Ihre Angaben bei der nächsten Anmeldung nicht mehr vorhanden sind.",
    },
  },
  lotse: {
    fieldDeclarationIncomes: {
      fieldConfirmIncomes:
        "Hiermit erkläre ich / erklären wir, dass ich / wir im Steuerjahr 2021 keine weiteren Einkünfte hatte / hatten, außer der oben aufgeführten Einkünfte.",
    },
    declarationIncomes: {
      listItem1:
        "inländische Renteneinkünfte und / oder Pensionen, die von den Rentenversicherungsträgern oder vom Arbeitgeber elektronisch gemeldet worden sind, und ggf.",
      listItem2:
        "Kapitaleinkünfte, von denen bereits Abgeltungsteuer an das Finanzamt abgeführt oder für die der Sparer-Pauschbetrag in Anspruch genommen wurde (Freistellungsauftrag), und ggf.",
      listItem3:
        "pauschal besteuerte Einkünfte aus geringfügigen Beschäftigungen (Mini-Jobs) bis zu einer Höhe von insgesamt 450 Euro monatlich",
    },
    sessionNote: {
      title: "Hinweis zur Sitzung",
      listItem1:
        "Ihre Daten gehören Ihnen und werden erst übermittelt, wenn Sie Ihre Steuererklärung verschicken.",
      listItem2:
        "Aus diesem Grund werden Ihre Angaben derzeit nicht zwischengespeichert. Sie müssen Ihre Steuererklärung daher <bold>in einer Sitzung abschließen.</bold>",
      listItem3:
        "Sie können sich innerhalb der Sitzung für das Ausfüllen Ihrer Steuererklärung natürlich Zeit lassen. Sollten Sie allerdings <bold>länger als 3 Stunden</bold> nichts mehr auf dieser Webseite machen, werden Sie aus Sicherheitsgründen automatisch abgemeldet.",
      listItem4:
        "Sie können alle Angaben vor Versand noch einmal kontrollieren.",
    },
    declarationEdaten: {
      intro1:
        "Da viele Informationen der Finanzverwaltung bereits vorliegen, müssen Sie diese nicht mehr in Ihre Steuererklärung eintragen. Dazu gehören zum Beispiel die elektronisch an die Finanzverwaltung übermittelten inländischen Renteneinkünfte, Pensionen und Krankenversicherungsbeiträge.",
      intro2:
        "Welche Beträge über Sie übermittelt wurden, können Sie den Bescheiden entnehmen, die Sie von der jeweiligen Stelle per Post erhalten haben. Die Daten kommen aus der gleichen Quelle.",
      labelText:
        "Ich bzw. wir sind damit einverstanden, dass die Festsetzung meiner / unserer Einkommensteuer anhand der elektronisch vorliegenden Daten erfolgt, die der Finanzbehörde vorliegen.",
    },
    confirmation: {
      fieldRegistrationConfirmDataPrivacy: {
        labelText:
          "Ich habe die <dataPrivacyLink href='http://test.de'>Datenschutzerklärung</dataPrivacyLink> inklusive der <taxGdprLink>Allgemeinen Informationen zur Umsetzung der datenschutzrechtlichen Vorgaben der Artikel 12 bis 14 der Datenschutz-Grundverordnung in der Steuerverwaltung</taxGdprLink> zur Kenntnis genommen und akzeptiere diese.",
      },
      fieldRegistrationConfirmTermsOfService: {
        labelText:
          "Ich habe die <termsOfServiceLink>Nutzungsbedingungen</termsOfServiceLink> gelesen und stimme ihnen zu.",
      },
      finish: "Steuererklärung abgeben",
    },
    taxNumber: {
      taxNumberExists: {
        labelText_one: "Haben Sie bereits eine Steuernummer?",
        labelText_other: "Haben Sie bereits eine gemeinsame Steuernummer?",
        help: {
          title: "Wo finde ich diese Nummer?",
          text: "Sie finden Ihre Steuernummer auf jedem Steuerbescheid. Sollten Sie noch keine Steuererklärung abgegeben haben, können Sie eine neue Steuernummer beantragen. Bitte beachten Sie, dass die Steuernummer und die Steuer-Identifikationsnummer zwei verschiedene Nummern sind.",
        },
      },
      bundesland: {
        labelText: "Wählen Sie Ihr Bundesland",
      },
      taxOffices: {
        labelText: "Wählen Sie Ihr Finanzamt",
      },
      taxNumberInput: {
        label: {
          labelText: "Steuernummer",
          exampleInput: "Muss 10 oder 11 Ziffern haben",
        },
      },
      requestNewTaxNumber: {
        labelText_one:
          "Hiermit bestätige ich, dass ich noch keine Steuernummer bei meinem Finanzamt habe und eine neue Steuernummer beantragen möchten.",
        labelText_other:
          "Hiermit bestätigen wir, dass wir noch keine Steuernummer bei unserem Finanzamt haben und eine neue Steuernummer beantragen möchten.",
        headline: "Neue Steuernummer beantragen",
        intro:
          "Mit der Abgabe der Steuererklärung wird eine neue Steuernummer beim zuständigen Finanzamt beantragt. Die neue Steuernummer wird Ihnen dann mit dem Steuerbescheid mitgeteilt.",
      },
    },
    hasDisability: {
      intro_single:
        "Im Falle einer Behinderung oder Pflegebedürftigkeit können erhöhte Kosten für Medikamente und Betreuung anfallen. Damit diese Ausgaben Sie nicht zu sehr belasten, können Sie steuerliche Vergünstigungen in Anspruch nehmen.",
      intro_person_a:
        "Im Falle einer Behinderung oder Pflegebedürftigkeit können erhöhte Kosten für Medikamente und Betreuung anfallen. Damit diese Ausgaben Sie nicht zu sehr belasten, können Sie steuerliche Vergünstigungen für Person A in Anspruch nehmen.",
      intro_person_b:
        "Im Falle einer Behinderung oder Pflegebedürftigkeit können erhöhte Kosten für Medikamente und Betreuung anfallen. Damit diese Ausgaben Sie nicht zu sehr belasten, können Sie steuerliche Vergünstigungen für Person B in Anspruch nehmen.",
      details: {
        title: "Infos zu den steuerlichen Vergünstigungen",
        text: "Bei einer Behinderung besteht in der Regel Anspruch auf den <bold>Pauschbetrag für Menschen mit Behinderung.</bold> Die Höhe des Pauschbetrags ist vom Grad der Behinderung abhängig. Menschen mit Behinderung können unter bestimmten Voraussetzungen außerdem eine <bold>Pauschale für Fahrtkosten</bold> beantragen. Wählen Sie hier aus, ob Sie Angaben zu einer Behinderung machen möchten.",
      },
    },
    merkzeichen: {
      hasPflegegrad: {
        label: "Wurde ein Pflegegrad 4 oder 5 festgestellt?",
      },
      disabilityDegree: {
        label: "Grad der Behinderung",
        example: "ab 20",
      },
      merkzeichen: {
        label: "Merkzeichen",
        details: {
          title: "Infos zu den Merkzeichen",
          text: "Im Schwerbehindertenausweis, den man ab einem Grad der Behinderung von 50 und mehr erhalten kann, werden spezifische Behinderungen und bestimmte gesundheitliche Einschränkungen durch Merkzeichen kenntlich gemacht. Viele Nachteilsausgleiche für schwerbehinderte Menschen sind an bestimmte Merkzeichen gekoppelt. Sollten Sie kein Merkzeichen haben, lassen Sie das Feld frei.",
        },
      },
      hasMerkzeichenH: {
        label: "Merkzeichen H",
      },
      hasMerkzeichenG: {
        label: "Merkzeichen G",
      },
      hasMerkzeichenBl: {
        label: "Merkzeichen Bl",
      },
      hasMerkzeichenTbl: {
        label: "Merkzeichen TBl",
      },
      hasMerkzeichenAg: {
        label: "Merkzeichen aG",
      },
    },
    noPauschbetrag: {
      intro: {
        p1: "Ein Pauschbetrag wird erst ab einem Grad der Behinderung von 20 gewährt. Liegt der Grad der Behinderung darunter, gibt es keinen Anspruch auf einen Pauschbetrag.",
        p2: "<bold>Hinweis:</bold> Auch ohne Pauschbetrag können Sie behinderungsbedingte Aufwendungen absetzen. Und zwar im Bereich Krankheitskosten und weitere außergewöhnliche Belastungen.",
      },
    },
    pauschbetrag: {
      intro:
        "Auf Basis Ihrer Angaben haben Sie Anspruch auf den Pauschbetrag für Menschen mit Behinderung. <bold>Alternativ können die tatsächlichen Kosten</bold>, die in Zusammenhang mit Ihrer Behinderung entstanden sind, einzeln angegeben werden. Wählen Sie aus, ob Sie den Pauschbetrag in Anspruch nehmen möchten.",
      details: {
        title: "Welche Kosten sind damit abgegolten?",
        p1: "Den Pauschbetrag erhalten Sie für die Mehraufwendungen, die erfahrungsgemäß durch ihre Krankheit bzw. Behinderung entstehen. Hierzu zählen Aufwendungen für",
        p2: "Sind Ihre tatsächlichen Kosten, die auf Grund der Behinderung entstanden sind, höher als der Behinderten-Pauschbetrag, ist es sinnvoll die tatsächlichen Kosten anzugeben. Das können Sie im Bereich „Krankheitskosten und weitere außergewöhnliche Belastungen” machen.",
        p3: "<bold>Wichtig</bold>: In diesem Fall werden die tatsächlichen Aufwendungen um die zumutbare Belastung gekürzt.",
        p4: "Außerordentliche Kosten sind auch neben dem Pauschbetrag gesondert zu berücksichtigen, wenn sie zwar mit der Körperbehinderung zusammenhängen, sich jedoch in Folge ihrer Einmaligkeit der Typisierung des §  33b Abs. 3 EStG entziehen.",
        list: {
          listItem1:
            "die Hilfe bei den gewöhnlichen und regelmäßig wiederkehrenden Verrichtungen des täglichen Lebens",
          listItem2: "die eigene Pflege und",
          listItem3: "einen erhöhten Wäschebedarf.",
        },
      },
      requestPauschbetrag: {
        yes: "Pauschbetrag in Höhe von <bold>{{pauschbetrag}} Euro</bold> beantragen",
        no: "Pauschbetrag nicht beantragen",
      },
    },
    fahrtkostenpauschale: {
      introText:
        "Auf Basis Ihrer Angaben haben Sie Anspruch auf die behinderungsbedingte Fahrtkostenpauschale von <bold>{{fahrtkostenpauschaleAmount}} Euro abzüglich der zumutbaren Belastung</bold>. Einzelne Fahrten können Sie nicht mehr geltend machen.",
      requestsFahrtkostenpauschale: {
        yesLabel: "Pauschale beantragen",
        noLabel: "Pauschale nicht beantragen",
      },
      helpTitle: "Hinweis zur zumutbaren Belastung",
      helpText:
        "Nur der Betrag, der höher ist als Ihre zumutbare Belastung, wirkt sich steuermindernd aus. Die zumutbare Belastung hängt unter anderem von der Höhe Ihres Einkommens ab und wird von Ihrem Finanzamt automatisch berechnet.",
    },
    telephoneNumber: {
      fieldTelephoneNumber: {
        label: "Telefonnummer",
      },
    },
    stmindSelection: {
      selectVorsorge: {
        label: {
          title: "Vorsorgeaufwendungen",
          text: "Viele Versicherungen, mit denen Sie für Ihre Zukunft vorsorgen, können Sie von der Steuer absetzen. Hierzu zählen z.B. Unfallversicherungen, Haftpflichtversicherungen und bestimmte Risikolebensversicherungen.",
        },
      },
      selectAussergBela: {
        label: {
          title: "Krankheitskosten und weitere außergewöhnliche Belastungen",
          text: "In diesen Bereich fallen z.B. Aufwendungen, die durch Krankheit, Kur, eine Behinderung, Pflege, Bestattung, Unwetter oder durch Naturkatastrophen entstanden sind.",
        },
      },
      selectHandwerker: {
        label: {
          title: "Haushaltsnahe Dienstleistungen und Handwerkerleistungen",
          text: "Zu den Kosten für haushaltsnahe Dienst- und Handwerkerleistungen zählen z.B. Leistungen für Reinigung, Winterdienst, Gartenarbeit, Handwerker, Schornsteinfeger, Pflegeleistungen oder die Betreuung von Haustieren.",
        },
      },
      selectSpenden: {
        label: {
          title: "Spenden und Mitgliedsbeiträge",
          text: "An dieser Stellen können Sie Spenden und Mitgliedsbeiträge für steuerbegünstigte Zwecke angeben. Hierzu zählen z.B. Zahlungen an steuerbegünstigte Vereine, Stiftungen und inländische Parteien.",
        },
      },
      selectReligion: {
        label: {
          title: "Steuern für Ihre Religionsgemeinschaft",
          text: "Im Veranlagungsjahr 2021 gezahlte Steuern für Ihre Religionsgemeinschaft können Sie als sogenannte Sonderausgaben angeben.",
        },
      },
    },
  },
  unlockCodeActivation: {
    unlockCode: {
      labelText: "Freischaltcode",
      help: {
        title: "Wo finde ich diese Nummer?",
        text: "Wenn Sie sich beim Steuerlotsen erfolgreich registriert haben, bekommen Sie von Ihrer Finanzverwaltung einen Brief mit Ihrem persönlichen Freischaltcode zugeschickt. Den Freischaltcode finden Sie auf der letzten Seite des Briefes.",
      },
    },
    failure: {
      causes: {
        title: "Mögliche Ursachen",
        reasons1:
          "Ihr Freischaltcode ist nicht korrekt. Eine Ursache kann die Verwechslung von Ziffern oder Buchstaben sein, die sich ähneln. So kann die Ziffer 0 schnell mit dem Buchstaben O oder der Buchstabe B schnell mit der Ziffer 8 verwechselt werden. Prüfen Sie Ihre Angabe.",
        reasons2:
          "Haben Sie sich vor 90 Tagen registriert? In diesem Fall können Sie sich mit diesem Freischaltcode nicht mehr beim Steuerlotsen anmelden. <registrationLink>Registrieren</registrationLink> Sie sich bitte erneut. Sie erhalten dann einen Brief mit einem neuen Freischaltcode.",
        reasons3:
          "Ihre Anmeldung ist bereits mehr als 5 Mal fehlgeschlagen. Dann ist Ihr Freischaltcode nicht mehr gültig. Bitte <revocationLink>stornieren</revocationLink> Sie Ihren Freischaltcode und <registrationLink>registrieren</registrationLink> sich erneut. Sie erhalten dann einen Brief mit einem neuen Freischaltcode.",
      },
    },
  },
  unlockCodeRequest: {
    dataPrivacyAndAgb: {
      title: "Datenschutzerklärung und Nutzungsbedingungen",
    },
    fieldRegistrationConfirmDataPrivacy: {
      labelText:
        "Ich habe die <dataPrivacyLink>Datenschutzerklärung</dataPrivacyLink> inklusive der <taxGdprLink>Allgemeinen Informationen zur Umsetzung der datenschutzrechtlichen Vorgaben der Artikel 12 bis 14 der Datenschutz-Grundverordnung in der Steuerverwaltung</taxGdprLink> zur Kenntnis genommen und akzeptiere diese.",
    },
    fieldRegistrationConfirmTermsOfService: {
      labelText:
        "Ich habe die <termsOfServiceLink>Nutzungsbedingungen</termsOfServiceLink> gelesen und stimme ihnen zu.",
    },
    fieldRegistrationConfirmIncomes: {
      labelText:
        "Ich habe unter <eligibilityLink>Nutzung prüfen</eligibilityLink> den Fragebogen ausgewertet und erfülle alle Voraussetzungen für die Nutzung des Steuerlotsen.",
    },
    fieldRegistrationConfirmEData: {
      labelText:
        "Ich bzw. wir sind damit einverstanden, dass die Festsetzung meiner / unserer Einkommensteuer anhand der elektronisch vorliegenden Daten erfolgt, die der Finanzbehörde vorliegen.",
    },
    eData: {
      title: "Einverständnis zur automatischen Übernahme vorliegender Daten",
      helpTitle: "Was bedeutet das?",
      helpText:
        "Daten zu beispielsweise <bold>inländischen Renten, Pensionen oder Kranken- und Pflegeversicherungen</bold> erhält die Steuerverwaltung vom jeweiligen Träger elektronisch. Diese Daten werden vom Finanzamt automatisch übernommen und müssen von Ihnen nicht in diese Steuererklärung eingetragen werden. Welche Beträge über Sie übermittelt wurden, können Sie den Bescheiden entnehmen, die Sie von der jeweiligen Stelle per Post erhalten haben. Die Daten kommen aus der gleichen Quelle. Sollten Sie mit der Übernahme nicht einverstanden sein, können Sie die vereinfachte Steuererklärung leider nicht nutzen.",
    },
    gotFsc:
      "Sie haben Ihren Freischaltcode bereits erhalten? <br><loginLink>Dann können Sie sich anmelden</loginLink>.",
    input: {
      intro:
        "Mit Ihrer Registrierung beantragen Sie einen Freischaltcode bei Ihrer Finanzverwaltung. Sie erhalten diesen mit einem Brief <bold>innerhalb von zwei Wochen</bold> nach erfolgreicher Beantragung. Wenn Sie die Zusammenveranlagung nutzen möchten, reicht es aus, wenn sich eine Person registriert.",
    },
  },
  filing: {
    success: {
      title:
        "Ihre Informationen wurden erfolgreich verschickt. Speichern Sie Ihre Nachweise für Ihre Unterlagen.",
      intro:
        "Ihre Informationen wurden erfolgreich an Ihre Finanzverwaltung übermittelt. Bewahren Sie Ihre Nachweise für Nachfragen gut auf.",
      transfer_ticket: {
        heading: "Transferticket",
        text: "Mit dem Transferticket wird die erfolgreiche Übermittlung Ihrer Daten durch die Finanzverwaltung bestätigt. Notieren Sie sich Ihr Transferticket, damit Sie nachweisen können, dass Ihre Daten erfolgreich übermittelt wurden.",
        your_heading: "Ihr Transferticket:",
      },
      pdf: {
        heading: "Übersicht Ihrer übermittelten Angaben",
        text: "Sie finden in der Übersicht Ihrer übermittelten Angaben alle Daten, die an Ihre Finanzverwaltung gesendet wurden. So können Sie jederzeit nachsehen, was Sie angegeben haben. Die Übersicht hilft Ihnen zum Beispiel dabei, Ihren Steuerbescheid zu kontrollieren.",
        download: "Übersicht speichern",
      },
    },
    failure: {
      alert: {
        title: "Ihre Steuererklärung kann nicht übermittelt werden.",
      },
      nextStep: {
        heading: "Wie geht es weiter?",
        text: "Bitte wenden Sie sich mit einer E-Mail an  <anchormail>kontakt@steuerlotse-rente.de</anchormail>  und schildern Sie uns das Problem. Vermeiden Sie aber unbedingt, uns persönliche Daten, wie Ihren Freischaltcode oder Ihre Steuer-Identifikationsnummer zu senden.",
        mailto: "mailto:kontakt@steuerlotse-rente.de",
      },
      textUs: "Schreiben Sie uns",
      icon_alt: "Weißes Kreuzzeichen auf rotem Kreis",
    },
  },
  submitAcknowledge: {
    title:
      "Steuerformular - Abgabebestätigung - Der Steuerlotse für Rente und Pension",
    successMessage:
      "Herzlichen Glückwunsch! Sie sind mit Ihrer Steuererklärung fertig!",
    "next-steps": {
      heading: "Wie geht es weiter?",
      text: "Ihre Steuererklärung wird von Ihrem Finanzamt bearbeitet. Sie bekommen Ihren Steuerbescheid per Post zugeschickt.",
    },
    recommend: {
      heading: "Empfehlen Sie uns weiter!",
      text: "Wir möchten noch mehr Menschen bei Ihrer Steuererklärung helfen! Sie können uns dabei helfen, indem Sie den Steuerlotsen bekannter machen. Empfehlen Sie uns Ihren Bekannten und Freunden!",
      share_text:
        "Tipp: Mit dem Steuerlotsen für Rente und Pension kannst du deine Steuererklärung einfach und unkompliziert machen. Ich habe es selbst ausprobiert! Hier der Link: https://www.steuerlotse-rente.de/",
      mail_subject:
        "Hallo, schau dir das mal an: Steuerlotse für Rente und Pension",
      promote_url: "https://www.steuerlotse-rente.de/",
    },
    logout: {
      heading: "Wir löschen Ihr Nutzerkonto",
      text: "Bitte beachten Sie, dass Sie Ihren Freischaltcode nicht erneut verwenden können. Wenn Sie unseren Service nächstes Jahr wieder nutzen möchten, können Sie sich einfach erneut registrieren. Haben Sie Ihre Steuererklärung gespeichert? Dann können Sie sich abmelden.",
    },
  },
  dateField: {
    day: "Tag",
    month: "Monat",
    year: "Jahr",
  },
  register: {
    success: {
      "next-steps": {
        header: {
          title: "Ihre Registrierung war erfolgreich!",
          intro:
            "Wir haben Ihren Antrag an Ihre Finanzverwaltung weitergeleitet. Sie können mit Ihrer Steuererklärung beginnen, sobald Sie Ihren Freischaltcode erhalten haben. Es kann bis zu zwei Wochen dauern, bis Sie Ihren Brief erhalten.",
        },
        heading: "So geht es weiter",
        "step-1":
          "Sie bekommen von Ihrem Finanzamt den <bold>Brief mit Ihrem persönlichen Freischaltcode</bold> zugeschickt.",
        "step-2":
          "Sie können sich auf Ihre Steuererklärung vorbereiten bis Sie den Brief erhalten haben. Sammeln Sie dazu alle notwendigen Unterlagen sowie Belege. Eine Übersicht über die notwendigen Unterlagen, die Sie für die Erstellung Ihrer Steuererklärung brauchen, finden Sie in unserer <vorbereitungsHilfeLink>Vorbereitungshilfe</vorbereitungsHilfeLink>.",
        "step-3":
          "Wenn Sie den Brief erhalten haben und vorbereitet sind, gehen Sie erneut auf www.steuerlotse-rente.de",
        "step-4":
          "Wählen Sie den Menüpunkt <steuerErklaerungLink>Ihre Steuererklärung</steuerErklaerungLink> und melden sich mit Ihrem Freischaltcode an. Nach der Anmeldung können Sie das Steuerformular ausfüllen und verschicken.",
      },
      letter: {
        heading: "So sieht der Brief aus, den Sie erhalten werden",
        intro:
          "Auf dem Brief wird der DigitalService4Germany als Antragsteller angegeben. Die Organisation ist der Betreiber des Steuerlotsen. Ihren Freischaltcode finden Sie auf der letzten Seite des Briefes.",
      },
      preparation: {
        heading: "Wie Sie sich auf Ihre Steuererklärung vorbereiten können",
        intro:
          "Unsere Vorbereitungshilfe gibt Ihnen einen Überblick darüber, welche Unterlagen Sie für die Erstellung Ihrer Steuererklärung beim Steuerlotsen brauchen, und erklärt, wie Sie nach Erhalt des Briefes fortfahren.",
        anchor: "Vorbereitungshilfe herunterladen",
      },
    },
    failure: {
      header: {
        title: "Registrierung fehlgeschlagen. Bitte prüfen Sie Ihre Angaben.",
        intro:
          "Haben Sie sich vielleicht bereits registriert? In diesem Fall können Sie sich nicht erneut registrieren und bekommen einen Brief mit Ihrem persönlichen Freischaltcode von Ihrer Finanzverwaltung zugeschickt.",
      },
    },
  },
  revocation: {
    failure: {
      header: {
        title: "Stornierung fehlgeschlagen. Bitte prüfen Sie Ihre Angaben.",
        intro:
          "Sind Sie vielleicht noch nicht bei uns registriert? In diesem Fall können Sie Ihren Freischaltcode nicht stornieren. Haben Sie Ihre Steuererklärung bereits erfolgreich verschickt? Dann haben wir Ihren Freischaltcode automatisiert storniert und Sie müssen nichts weiter tun.",
      },
    },
  },
  fields: {
    idnr: {
      labelText: "Steuer-Identifikationsnummer",
      help: {
        title: "Wo finde ich diese Nummer?",
        text: "Die 11-stellige Nummer haben Sie mit einem Brief vom Bundeszentralamt für Steuern erhalten. Die Nummer steht oben rechts groß auf dem Brief. Alternativ finden Sie diese Nummer auch auf Ihrem letzten Steuerbescheid.",
      },
    },
    dob: {
      labelText: "Geburtsdatum",
    },
    dateField: {
      exampleInput: {
        text: "z.B. 29.2.1951",
      },
    },
    yesNoSwitch: {
      Yes: "Ja",
      No: "Nein",
    },
  },
  infoTaxReturnPensioners: {
    intro: {
      heading:
        "Vereinfachte Steuererklärung für Rentner - wie Sie in wenigen Minuten Ihre Steuererklärung kostenlos online machen können",
      paragraphOne:
        "Dank des neuen vereinfachten Online-Steuerformulars für Menschen im Ruhestand, das wir im Auftrag des Bundesfinanzministeriums entwickelt haben, können Sie jetzt Ihre Steuererklärung schnell, unkompliziert und kostenlos online einreichen. Ganz ohne Vorwissen und lästigen Papierkram.",
      paragraphTwo:
        "Was viele nicht wissen: Auch Rentner sind grundsätzlich steuerpflichtig - wenn ihre Alterseinkünfte eine gewisse Grenze überschreiten. Und weil die <statistaLink>Renten seit Jahren angepasst</statistaLink> werden, rutschen immer mehr Ruheständler in die Steuerpflicht. Aktuell zählt das Statistische Bundesamt insgesamt <destatisLink>6,8 Millionen steuerpflichtige Rentnerinnen und Rentner</destatisLink> in Deutschland. Tendenz steigend. ",
    },
    section_two: {
      heading:
        "Die vereinfachte Steuererklärung wurde speziell für Menschen im Ruhestand entwickelt",
      paragraph:
        "Wenn Sie also zu denen gehören, denen unerwartet ein Brief vom Finanzamt ins Haus flattert, können Sie erstmal beruhigt sein. Denn mit dem Steuerlotsen für Rente und Pension schrumpft die Steuererklärung zu einer kleinen Pflicht, die Sie in wenigen Minuten erledigen können. Der Steuerlotse führt Sie Schritt-für-Schritt mit einfachen Erklärungen durch die vereinfachte Steuererklärung. Außerdem müssen Sie viel weniger Angaben machen als bei üblichen Steuerformularen. Die Daten zu Ihren Einkünften werden direkt via E-Daten an das Finanzamt übermittelt. Ihre Steuererklärung beschränkt sich damit auf persönliche Angaben und die Beiträge, die Sie absetzen möchten. Was Sie alles absetzen können, erfahren Sie in unserem <downloadPreparationLink>Vorbereitungs-PDF</downloadPreparationLink>. Das spart enorm Zeit und Nerven und vereinfacht den gesamten Prozess. ",
    },
    section_three: {
      heading: "Wie finde ich heraus, ob ich als Rentner steuerpflichtig bin? ",
      paragraphOne:
        "Ob Sie den Steuerlotsen nutzen können, hängt natürlich davon ab, ob Sie steuerpflichtig sind. Wenn Sie bereits wissen, dass dies bei Ihnen der Fall ist, weil Sie zum Beispiel ein Schreiben vom Finanzamt erhalten haben, können Sie direkt zum Abschnitt „So funktioniert der Steuerlotse“ springen.",
      paragraphTwo:
        "Wenn Sie jedoch noch unsicher sind, ob Sie überhaupt eine Steuererklärung abgeben müssen, dann können Sie mit dem <incomeCalculatorLink>Alterseinkünfte-Rechner</incomeCalculatorLink> des Bayerischen Landesamts für Steuern kostenlos kalkulieren, wie hoch eine mögliche Einkommensteuer bei Ihnen ausfällt. Außerdem finden Sie weitere Informationen zur Besteuerung der Rente auf der Seite der <pensionersInsuranceLink>Deutschen Rentenversicherung.</pensionersInsuranceLink>",
    },
    section_four: {
      heading:
        "So funktioniert der Steuerlotse für Rente und Pension in 4 Schritten",
      paragraph:
        "Ist die Frage der Steuerpflicht geklärt, dann geht es mit dem Steuerlotsen in 4 Schritten zur fertigen Steuererklärung.",
    },
    section_five: {
      listItemOneHeading: "Schritt 1: Nutzung prüfen",
      listItemOne:
        "Im ersten Schritt müssen Sie auf der <eligibilityLink>Webseite des Steuerlotsen prüfen</eligibilityLink>, ob Sie den Steuerlotsen in seiner aktuellen Entwicklungsform nutzen können. Denn zur Zeit richtet sich der Steuerlotse nur an Personen und Paare, die eine Rente und Pension beziehen und keine Zusatzeinkünfte haben. Trifft dies zu, können Sie im zweiten Schritt mit der Registrierung fortfahren.",
      listItemTwoHeading: "Schritt 2: Registrieren",
      listItemTwo:
        "Wenn Sie den Steuerlotsen nutzen können, registrieren Sie sich im nächsten Schritt. Bei der <registrationLink>Registrierung</registrationLink> wird automatisch ein Freischaltcode bei Ihrer Finanzverwaltung beantragt. Den Freischaltcode wird Ihnen per Brief innerhalb von zwei Wochen nach erfolgreicher Beantragung zugesendet. Übrigens: auch eine Zusammenveranlagung ist möglich. Hierfür muss sich nur eine Person registrieren.",
      listItemThreeHeading: "Schritt 3: Vorbereiten",

      listItemThree:
        "Nach der erfolgreichen Registrierung ist es wichtig, dass Sie sich gut vorbereiten. Stellen Sie daher sicher, alle erforderlichen Informationen, wie zum Beispiel Belege, vorliegen zu haben. Damit Sie nichts vergessen und perfekt vorbereitet sind, haben wir eine nützliche Kontrollliste mit allen wichtigen Informationen zum <downloadPreparationLink>Herunterladen</downloadPreparationLink> für Sie angefertigt.",
      listItemFourHeading: "Schritt 4: Steuererklärung ausfüllen",

      listItemFour:
        "Nach Erhalt des Freischaltcodes können Sie mit der <activationLink>Steuererklärung</activationLink> beginnen. Dafür melden Sie sich auf der Webseite unter „Ihre Steuererklärung“ mit den entsprechenden Daten an. Aber aufgepasst: bevor Sie mit der vereinfachten Steuererklärung loslegen, sollten Sie alle erforderlichen Informationen, wie zum Beispiel Belege, vorliegen haben. Und damit Sie nichts vergessen und perfekt vorbereitet sind, gibt es noch eine nützliche Checkliste zum Herunterladen.",
    },
    section_six: {
      text: "Nachdem Sie sich durch das Online-Formular des Steuerlotsen geklickt haben und alle Angaben gemacht haben, wird Ihre Steuererklärung elektronisch an ihr Finanzamt weitergeleitet. Ihre Steuererklärung ist offiziell eingereicht! Sie können sich nun zurücklehnen und auf den Steuerbescheid warten. Dieser wird Ihnen vom Finanzamt innerhalb der üblichen Frist zugeschickt.",
    },
  },
  AmbassadorMaterial: {
    Heading: "Werden Sie Digital-Botschafter:in für den Steuerlotsen",
    SubHeading:
      "Wir wollen so viele Menschen im Ruhestand wie möglich erreichen. Unterstützen Sie uns dabei! Hier finden Sie Informationsmaterialien zum Download und ein Erklärvideo zum Steuerlotsen.",
    Paragraph: {
      DownloadInformationText: "Informationsmaterialien zum Download",
      InfoBroshureDownloadLink: "Informationsbroschüre (PDF) speichern",
      SteuerlotsenFlyerLink: "Steuerlotsen-Flyer (PDF) speichern",
      HowItWorks: "So funktioniert der Steuerlotse für Rente und Pension",
    },
  },
  taxGuideQuestionBox: {
    canIUseTaxGuide:
      "Kann ich den Steuerlotsen für meine Steuererklärung nutzen?",
    startQuestionnaire: "Fragebogen starten",
    moreInformationTaxGuide:
      "Wo finde ich mehr Informationen zum Steuerlotsen?",
    faq: "Häufig gestellte Fragen",
    contactUs: "Kontaktieren Sie uns",
  },
};

export default translations;
