import { t } from "i18next";

const anchorList = [
  {
    text: t("ContentPagesAnchors.Krankheitskosten.text"),
    url: "/krankheitskosten",
  },
  {
    text: t("ContentPagesAnchors.Vorsorgeaufwendungen.text"),
    url: "/#",
  },
  {
    text: t("ContentPagesAnchors.Pflegekosten.text"),
    url: "/#",
  },
  {
    text: t("ContentPagesAnchors.Behinderung.text"),
    url: "/#",
  },
  {
    text: t("ContentPagesAnchors.Bestattungskosten.text"),
    url: t("ContentPagesAnchors.Bestattungskosten.url"),
  },
  {
    text: t("ContentPagesAnchors.Belastungen.text"),
    url: "/#",
  },
  {
    text: t("ContentPagesAnchors.Dienstleistungen.text"),
    url: "/#",
  },
  {
    text: t("ContentPagesAnchors.Handwerkerleistungen.text"),
    url: "/#",
  },
  {
    text: t("ContentPagesAnchors.Spenden.text"),
    url: "/#",
  },
  {
    text: t("ContentPagesAnchors.Kirchensteuer.text"),
    url: "/#",
  },
];

const anchorBack = {
  text: t("anchorBackUebersicht.text"),
  url: "/#",
};

const anchorAnmelden = {
  text: t("anchorButton.anmelden.text"),
  url: "/unlock_code_request/step/data_input?link_overview=False",
};

export { anchorList, anchorBack, anchorAnmelden };