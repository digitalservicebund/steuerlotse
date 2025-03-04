import React from "react";
import { useTranslation } from "react-i18next";
import InfoBox from "../components/InfoBox";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormHeader from "../components/FormHeader";
// eslint-disable-next-line import/named
import {
  anchorBack,
  anchorList,
  anchorRegister,
} from "../lib/contentPagesAnchors";
import {
  ContentWrapper,
  List,
  AnchorListItem,
  ListItem,
  Headline2,
  Paragraph,
} from "../components/ContentPagesGeneralStyling";

export default function HouseholdServicesInfoPage() {
  const { t } = useTranslation();

  const anchorListItemsMap = anchorList
    .filter((item) => item.text !== "Haushaltsnahe Dienstleistungen")
    .map((anchor) => (
      <AnchorListItem key={anchor.text}>
        <a href={anchor.url}>{anchor.text}</a>
      </AnchorListItem>
    ));

  const listHouseholdServices = [
    {
      text: t("HouseholdServicesInfo.Section2.ListItem1"),
    },
    {
      text: t("HouseholdServicesInfo.Section2.ListItem2"),
    },
    {
      text: t("HouseholdServicesInfo.Section2.ListItem3"),
    },
    {
      text: t("HouseholdServicesInfo.Section2.ListItem4"),
    },
    {
      text: t("HouseholdServicesInfo.Section2.ListItem5"),
    },
    {
      text: t("HouseholdServicesInfo.Section2.ListItem6"),
    },
    {
      text: t("HouseholdServicesInfo.Section2.ListItem7"),
    },
    {
      text: t("HouseholdServicesInfo.Section2.ListItem8"),
    },
  ];

  const listHouseholdServicessMap = listHouseholdServices.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  return (
    <>
      <ContentWrapper>
        <StepHeaderButtons text={anchorBack.text} url={anchorBack.url} />
        <FormHeader
          title={t("HouseholdServicesInfo.Section1.Heading")}
          intro={t("HouseholdServicesInfo.Section1.Text")}
        />
        <Headline2>{t("HouseholdServicesInfo.Section2.Heading")}</Headline2>
        <Paragraph>{t("HouseholdServicesInfo.Section2.Text")}</Paragraph>
        <List aria-label="simple-list">{listHouseholdServicessMap}</List>
        <Paragraph>{t("HouseholdServicesInfo.Section2.Text2")}</Paragraph>

        <Headline2>{t("HouseholdServicesInfo.Section3.Heading")}</Headline2>
        <Paragraph>{t("HouseholdServicesInfo.Section3.Text")}</Paragraph>
        <Paragraph>{t("HouseholdServicesInfo.Section3.Text2")}</Paragraph>

        <Headline2>{t("HouseholdServicesInfo.Section4.Heading")}</Headline2>
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
