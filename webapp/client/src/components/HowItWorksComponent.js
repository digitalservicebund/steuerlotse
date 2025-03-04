import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import styled from "styled-components";
import ButtonAnchor from "./ButtonAnchor";

const Box = styled.div`
  border-left: ${(props) =>
    props.border ? "none" : "2px solid var(--beige-500)"};
`;

const InnerBox = styled.div`
  padding-left: var(--spacing-09);
  display: flex;
  position: relative;
  justify-content: space-between;
  padding-bottom: 100px;
`;

const Icon = styled.img`
  position: absolute;
  top: 0;
  left: -26.5px;
  border-radius: 100%;
  height: 50px;
  width: 50px;
`;

const Figure = styled.figure`
  width: 100%;
  max-width: 476px;
  border-radius: 50px;
  box-shadow: 20px 20px 50px rgba(0, 0, 0, 0.35);

  @media (max-width: 768px) {
    max-width: 180px;
  }
  img {
    width: 100%;
    height: auto;
    object-fit: contain;
  }
`;

const Headline3 = styled.h3`
  font-size: var(--text-2xl);
  margin-bottom: var(--spacing-06);

  @media (max-width: 768px) {
    font-size: var(--text-medium-big);
  }
`;

const Column = styled.div`
  margin-right: 3rem;
  max-width: 253px;
  display: ${(props) => props.button && "flex"};
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;

  @media (max-width: 768px) {
    margin-right: 2rem;
    max-width: 200px;
  }

  @media (max-width: 575px) {
    margin-right: 0;
    max-width: 100%;
  }
`;

const InnerContent = styled.div`
  display: flex;
  flex-wrap: wrap;

  @media (max-width: 768px) {
    margin-right: var(--spacing-06);
  }

  @media (max-width: 575px) {
    justify-content: start;
  }
`;

const Div = styled.div`
  display: flex;
  justify-content: center;

  @media (max-width: 1279px) {
    display: none;
  }
`;

const DeadlineContainer = styled.div`
  background-color: var(--blue-100);
  padding: var(--spacing-03);
  width: fit-content;
  margin: var(--spacing-06) 0;
`;

export default function HowItWorksComponent({
  heading,
  text,
  icon,
  image,
  variant,
  plausibleDomain,
  button,
  deadline,
}) {
  const { t } = useTranslation();
  const plausiblePropsEligibilityStartButton = {
    method: "Sofunktionierts / CTA Jetzt starten",
  };
  return (
    <Box border={variant}>
      <InnerBox>
        <Icon src={icon.iconSrc} alt={icon.altText} />
        <InnerContent>
          <Column button={button}>
            <div>
              <Headline3>{heading}</Headline3>
              {deadline && <DeadlineContainer>{deadline}</DeadlineContainer>}
              {text && <p>{text}</p>}
            </div>
            {button && (
              <Div>
                <ButtonAnchor
                  url="/eligibility/step/welcome?link_overview=False"
                  plausibleGoal={t("howItWorksPage.startButton.plausibleGoal")}
                  plausibleProps={plausiblePropsEligibilityStartButton}
                  plausibleDomain={plausibleDomain}
                  disabled
                >
                  {t("howItWorksPage.startButton.text")}
                </ButtonAnchor>
              </Div>
            )}
          </Column>
          <Figure>
            <picture>
              <source media="(min-width: 769px)" srcSet={image.srcSetDesktop} />
              <source media="(min-width: 320px)" srcSet={image.srcSetMobile} />
              <img src={image.src} alt={image.alt} srcSet={image.srcSet} />
            </picture>
          </Figure>
        </InnerContent>
      </InnerBox>
    </Box>
  );
}

HowItWorksComponent.propTypes = {
  heading: PropTypes.string,
  text: PropTypes.string,
  icon: PropTypes.shape({
    iconSrc: PropTypes.string,
    altText: PropTypes.string,
  }),
  image: PropTypes.shape({
    src: PropTypes.string,
    srcSet: PropTypes.string,
    srcSetDesktop: PropTypes.string,
    srcSetMobile: PropTypes.string,
    alt: PropTypes.string,
  }),
  variant: PropTypes.bool,
  plausibleDomain: PropTypes.string,
  button: PropTypes.shape({
    url: PropTypes.string,
    plausibleGoal: PropTypes.string,
    plausibleProps: PropTypes.shape({
      props: PropTypes.shape({
        method: PropTypes.string,
      }),
    }),
  }),
  deadline: PropTypes.string,
};

HowItWorksComponent.defaultProps = {
  heading: null,
  text: null,
  icon: null,
  image: null,
  variant: null,
  plausibleDomain: null,
  button: null,
  deadline: null,
};
