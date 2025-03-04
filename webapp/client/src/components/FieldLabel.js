import React from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import FieldLabelScaffolding from "./FieldLabelScaffolding";
import { labelPropType } from "../lib/propTypes";

const Label = styled.label`
  &.field-label {
    margin-bottom: var(--spacing-01);
  }

  &.field-label-example {
    margin-bottom: var(--spacing-01);
  }
`;

export default function FieldLabel(props) {
  const { fieldId } = props;
  return (
    <FieldLabelScaffolding
      {...props}
      render={(innerContent, className) => (
        <Label htmlFor={fieldId} className={className}>
          {innerContent}
        </Label>
      )}
    />
  );
}

FieldLabel.propTypes = {
  fieldId: PropTypes.string.isRequired,
  label: labelPropType,
  details: FieldLabelScaffolding.propTypes.details,
};

FieldLabel.defaultProps = {
  ...FieldLabelScaffolding.defaultProps,
};
