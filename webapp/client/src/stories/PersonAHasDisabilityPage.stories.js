import React from "react";

import PersonAHasDisabilityPage from "../pages/PersonAHasDisabilityPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/PersonAHasDisabilityPage",
  component: PersonAHasDisabilityPage,
};

function Template(args) {
  return <PersonAHasDisabilityPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title:
      "Möchten Sie Angaben zu einer Behinderung oder Pflegebedürftigkeit machen?",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    personAHasDisability: {
      value: null,
      errors: [],
    },
  },
  prevUrl: "test",
  numUsers: 1,
};

export const WithError = Template.bind({});
WithError.args = {
  ...Default.args,
  fields: {
    personAHasDisability: {
      value: "yes",
      errors: ["Falsche Eingabe"],
    },
  },
};

export const JointTaxes = Template.bind({});
JointTaxes.args = {
  ...Default.args,
  numUsers: 2,
};
