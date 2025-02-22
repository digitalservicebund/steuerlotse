import React from "react";
import { t } from "i18next";
import InfoBox from "../components/InfoBox";
import FormHeader from "../components/FormHeader";
// eslint-disable-next-line import/named
import {
  anchorBack,
  anchorList,
  anchorRegister,
} from "../lib/contentPagesAnchors";
import StepHeaderButtons from "../components/StepHeaderButtons";
import {
  AnchorListItem,
  ContentWrapper,
  Headline2,
  List,
  Paragraph,
} from "../components/ContentPagesGeneralStyling";

export default function ChurchTaxInfoPage() {
  const anchorListItemsMap = anchorList
    .filter((item) => item.text !== "Kirchensteuer")
    .map((anchor) => (
      <AnchorListItem key={anchor.text}>
        <a href={anchor.url}>{anchor.text}</a>
      </AnchorListItem>
    ));

  return (
    <>
      <ContentWrapper>
        <StepHeaderButtons text={anchorBack.text} url={anchorBack.url} />
        <FormHeader
          title={t("Kirchensteuer.Section1.heading")}
          intro={t("Kirchensteuer.Section1.text")}
        />
        <Headline2>{t("Kirchensteuer.Section2.heading")}</Headline2>
        <Paragraph>{t("Kirchensteuer.Section2.text")}</Paragraph>
        <Headline2>{t("Kirchensteuer.Section3.heading")}</Headline2>
        <Paragraph>{t("Kirchensteuer.Section3.text")}</Paragraph>
        <Headline2>{t("Kirchensteuer.Section5.heading")}</Headline2>
        <List aria-label="anchor-list">{anchorListItemsMap}</List>
      </ContentWrapper>
      <InfoBox
        boxHeadline={anchorRegister.headline}
        boxText={t("InfoBox.text")}
        anchor={anchorRegister}
      />
    </>
  );
}
