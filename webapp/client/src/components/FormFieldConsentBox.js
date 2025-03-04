import PropTypes from "prop-types";
import styled from "styled-components";
import FormFieldScaffolding from "./FormFieldScaffolding";
import checkedIcon from "../assets/icons/checked.svg";

const ConsentBox = styled.div`
  &.checkbox {
    padding: 0;
    margin-top: var(--spacing-02);
    flex-wrap: inherit;
  }

  &.consent-box {
    background-color: var(--bg-highlight-color);
    ${({ disable }) =>
      disable &&
      `
        background-color: var(--beige-200);
        color: var(--grey-900);
  `}
    padding: var(--spacing-04);
  }

  &.checkbox input {
    width: 30px;
    height: 30px;
    opacity: 0;
  }

  &.checkbox input:focus-visible + label {
    box-shadow: 0 0 0 3px var(--focus-color);
    background-color: var(--focus-color);
  }

  &.checkbox input:checked ~ label.checkmark {
    background-color: var(--link-color);
    ${({ disable }) =>
      disable &&
      `
        background-color: var(--blue-400);
        border-color: var( --grey-500);
  `}
    background-image: url(${checkedIcon});
    background-repeat: no-repeat;
    background-size: 22px;
    background-position: center;
  }

  & label.checkmark {
    display: block;
    width: 30px;
    height: 30px;
    cursor: pointer;
    ${({ disable }) =>
      disable &&
      `
        cursor: default;
  `}
    background: white;
    position: absolute;
    border: 2px solid var(--text-color);
  }
`;

function FormFieldConsentBox({
  fieldName,
  fieldId,
  checked,
  required,
  autofocus,
  labelText,
  errors,
  disable,
}) {
  return (
    <FormFieldScaffolding
      {...{
        fieldName,
        errors,
      }}
      hideLabel
      render={() => (
        <ConsentBox
          disable={disable}
          className="form-row checkbox consent-box col-lg-10"
        >
          <input
            disabled={disable}
            type="checkbox"
            id={fieldId}
            name={fieldName}
            required={required}
            defaultChecked={checked}
            // TODO: autofocus is under review.
            // eslint-disable-next-line
            autoFocus={autofocus}
          />
          {/* TODO: there should be only one label for an input */}
          {/* eslint-disable-next-line */}
          <label htmlFor={fieldId} className="checkmark" />
          <label
            htmlFor={fieldId}
            className="col-sm-10 col-form-label ml-3 pt-0"
          >
            {labelText}
          </label>
        </ConsentBox>
      )}
    />
  );
}

FormFieldConsentBox.propTypes = {
  fieldName: PropTypes.string.isRequired,
  fieldId: PropTypes.string.isRequired,
  labelText: PropTypes.oneOfType([PropTypes.string, PropTypes.element])
    .isRequired,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  checked: PropTypes.bool,
  required: PropTypes.bool,
  autofocus: PropTypes.bool,
  disable: PropTypes.bool,
};

FormFieldConsentBox.defaultProps = {
  checked: false,
  required: false,
  autofocus: false,
  disable: false,
};

export default FormFieldConsentBox;
