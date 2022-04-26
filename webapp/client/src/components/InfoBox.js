import styled from "styled-components";
import { t } from "i18next";
import ButtonAnchor from "./ButtonAnchor";
import { anchorAnmelden } from "../lib/contentPagesAnchors";

const Box = styled.div`
  background-color: var(--beige-200);
  padding-top: var(--spacing-09);
  margin-top: var(--spacing-10);
`;
const InnerBox = styled.div`
  display: flex;
  flex-direction: column;
  padding-left: var(--spacing-03);
  padding-right: var(--spacing-03);
  margin: 0 auto;
  max-width: var(--main-max-width);

  @media (min-width: 768px) {
    flex-direction: row;
  }
`;

const TextBox = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  @media (min-width: 768px) {
    padding-bottom: var(--spacing-09);
  }
`;
const BoxHeadline = styled.h2`
  padding-bottom: var(--spacing-06);
  margin: 0;
  font-size: var(--text-2xl);

  @media (min-width: 1024px) {
    font-size: var(--text-5xl);
  }
`;
const BoxText = styled.span`
  padding-bottom: var(--spacing-06);
`;
const Figure = styled.figure`
  margin: 0;

  img {
    max-width: 500px;
    height: auto;
  }
`;

export default function InfoBox() {
  return (
    <Box>
      <InnerBox>
        <TextBox className="info-box__text">
          <BoxHeadline>{t("InfoBox.heading")}</BoxHeadline>
          <BoxText>{t("InfoBox.text")}</BoxText>
          <ButtonAnchor url={anchorAnmelden.url}>
            {anchorAnmelden.text}
          </ButtonAnchor>
        </TextBox>
        <Figure className="info-box__figure">
          <img src="images/teaser-image.png" alt="teaser img" />
        </Figure>
      </InnerBox>
    </Box>
  );
}