import React from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";
import InfoBox from "../components/InfoBox";
import {
  ContentWrapper,
  List,
  ListItem,
  Headline1,
  Headline2,
  Paragraph,
  ParagraphLarge,
  HeadingBox,
  InnerContent,
} from "../components/ContentPagesGeneralStyling";

const Picture = styled.picture`
  margin: var(--spacing-09) 0 0;
  display: block;

  @media (min-width: 768px) {
    grid-column-start: between-column;
    grid-column-end: column-end;
    grid-row-start: row1-end;
    grid-row-end: row-end;
    align-self: end;
    margin: 0;
  }

  img {
    width: 100%;
    height: auto;
    object-fit: contain;
  }
`;

export default function InfoForRelativesPage() {
  const { t } = useTranslation();

  const ListDependents = [
    {
      text: t("InfoForRelatives.Section2.ListItem1"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem2"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem3"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem4"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem5"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem6"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem7"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem8"),
    },
    {
      text: t("InfoForRelatives.Section2.ListItem9"),
    },
  ];

  const ListDependentsMap = ListDependents.map((item) => (
    <ListItem key={item.text}>{item.text}</ListItem>
  ));

  return (
    <div>
      <ContentWrapper>
        <InnerContent>
          <Picture>
            <img src="../images/info-angehoerige.jpeg" alt="to be changed" />
          </Picture>
          <HeadingBox>
            <Headline1>{t("InfoForRelatives.Section1.Heading")}</Headline1>
            <ParagraphLarge>
              {t("InfoForRelatives.Section1.Text")}
            </ParagraphLarge>
          </HeadingBox>
        </InnerContent>
      </ContentWrapper>
      <ContentWrapper>
        <Headline2>{t("InfoForRelatives.Section2.Heading")}</Headline2>
        <Paragraph>{t("InfoForRelatives.Section2.Text")}</Paragraph>
        <List aria-label="simple-list">{ListDependentsMap}</List>

        <Headline2>{t("InfoForRelatives.Section3.Heading")}</Headline2>
        <Paragraph>{t("InfoForRelatives.Section3.Text")}</Paragraph>
      </ContentWrapper>
      <InfoBox />
    </div>
  );
}
