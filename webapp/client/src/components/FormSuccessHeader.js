import PropTypes from "prop-types";
import styled from "styled-components";

const SuccessAlertArea = styled.div`
  &.alert {
    border-radius: 0;
    border: 0;
    padding: var(--spacing-05);
  }

  &.alert-success {
    background-color: var(--success-color);
    color: var(--inverse-text-color);
  }
`;

const Intro = styled.p`
  font-size: var(--text-medium);
`;

export default function FormSuccessHeader({ title, intro, hideIntro }) {
  return (
    <>
      <SuccessAlertArea className="alert alert-success" role="alert">
        <h1>{title}</h1>
      </SuccessAlertArea>
      {intro && !hideIntro && <Intro>{intro}</Intro>}
    </>
  );
}

FormSuccessHeader.propTypes = {
  title: PropTypes.string.isRequired,
  intro: PropTypes.oneOfType([PropTypes.string, PropTypes.element]),
  hideIntro: PropTypes.bool,
};

FormSuccessHeader.defaultProps = {
  intro: undefined,
  hideIntro: false,
};