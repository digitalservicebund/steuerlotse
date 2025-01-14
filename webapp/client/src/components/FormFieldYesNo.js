import { useState } from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import styled from "styled-components";
import FormFieldScaffolding from "./FormFieldScaffolding";
import FieldLabelForSeparatedFields from "./FieldLabelForSeparatedFields";

const YesNo = styled.div`
  & .switch-yes,
  .switch-no {
    padding: 1rem 1.45rem;

    color: var(--text-color) !important;
    background: var(--bg-white) !important;
    font-size: var(--text-s);
    box-shadow: none;
    border-radius: 0;
    border: 1px solid var(--border-color) !important;
  }

  & .switch-no {
    margin-left: -1px; // To hide double border in the middle
  }

  & .switch-yes:focus-within:not(:hover),
  .switch-no:focus-within:not(:hover) {
    padding: 1rem 1.45rem calc(1rem - 3px) 1.45rem;
    position: relative;
    z-index: 1;

    color: var(--focus-text-color) !important;
    background: var(--focus-color) !important;

    border: 1px solid var(--border-color) !important;
    border-bottom: 0px solid black !important;
    box-shadow: 0px 4px 0px var(--text-color);
  }

  & .switch-yes.active,
  .switch-no.active {
    color: var(--inverse-text-color) !important;
    background: var(--link-color) !important;
    border-radius: 0;
    border: 1px solid var(--link-color) !important;
  }

  & .switch-yes:active,
  .switch-no:active {
    box-shadow: 0 0 0 3px var(--focus-color) !important;
  }

  & .switch-yes:hover,
  .switch-no:hover,
  .switch-yes.active:hover,
  .switch-no.active:hover,
  .switch-yes:focus-within:hover,
  .switch-no:focus-within:hover {
    color: var(--inverse-text-color) !important;

    background: var(--link-hover-color) !important;
    border: 1px solid var(--link-hover-color) !important;
  }

  & input[type="radio"] {
    opacity: 0;
    position: absolute;
  }

  label {
    margin: 0; // Overwrite general label styling
  }
`;

function FormFieldYesNo({
  fieldName,
  fieldId,
  value,
  required,
  autofocus,
  label,
  details,
  errors,
  onChangeHandler,
}) {
  const [selectedValue, setSelectedValue] = useState(value);
  const yesFieldId = `${fieldId}-yes`;
  const noFieldId = `${fieldId}-no`;

  const toggleYesNoButton = (event) => {
    setSelectedValue(event.target.value);
  };

  const switchYesClassNames = classNames("switch-yes", {
    active: selectedValue === "yes",
  });

  const switchNoClassNames = classNames("switch-no", {
    active: selectedValue === "no",
  });

  return (
    <FormFieldScaffolding
      {...{
        fieldName,
        errors,
      }}
      hideLabel
      render={() => (
        <YesNo>
          <fieldset id={fieldId} name={fieldId}>
            <FieldLabelForSeparatedFields {...{ label, fieldId, details }} />
            <label htmlFor={yesFieldId} className={switchYesClassNames}>
              <input
                type="radio"
                id={yesFieldId}
                name={fieldId}
                required={required}
                value="yes"
                defaultChecked={selectedValue === "yes"}
                onClick={toggleYesNoButton}
                onChange={onChangeHandler}
              />
              Ja
            </label>
            <label htmlFor={noFieldId} className={switchNoClassNames}>
              <input
                type="radio"
                id={noFieldId}
                name={fieldId}
                required={required}
                autoFocus={autofocus || Boolean(errors.length)}
                value="no"
                defaultChecked={selectedValue === "no"}
                onClick={toggleYesNoButton}
                onChange={onChangeHandler}
              />
              Nein
            </label>
          </fieldset>
        </YesNo>
      )}
    />
  );
}

FormFieldYesNo.propTypes = {
  fieldName: PropTypes.string.isRequired,
  fieldId: PropTypes.string.isRequired,
  value: PropTypes.string,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.object]).isRequired,
  details: FieldLabelForSeparatedFields.propTypes.details,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  required: PropTypes.bool,
  autofocus: PropTypes.bool,
  onChangeHandler: PropTypes.func,
};

FormFieldYesNo.defaultProps = {
  value: undefined,
  required: false,
  autofocus: false,
  details: FieldLabelForSeparatedFields.defaultProps.details,
  onChangeHandler: undefined,
};

export default FormFieldYesNo;
