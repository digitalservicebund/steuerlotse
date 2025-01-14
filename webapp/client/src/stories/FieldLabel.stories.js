import React from "react";

import FieldLabel from "../components/FieldLabel";

export default {
  title: "Form Fields/Label",
  component: FieldLabel,
};

function Template(args) {
  return <FieldLabel {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  fieldId: "some-id",
  label: {
    text: "Freischaltcode",
  },
};

export const WithAllExtras = Template.bind({});
WithAllExtras.args = {
  ...Default.args,
  label: {
    text: "Grad der Behinderung",
    help: "Tragen Sie bitte hier den Grad der Behinderung ein. Der Grad der Behinderung, abgekürzt GdB, wird mit einem ärztlichen Gutachten individuell festgelegt. Er steht ebenfalls auf dem Behindertenausweis.",
    showOptionalTag: true,
    exampleInput: "z.B. 25, 30, 35 etc.",
  },
  details: {
    title: "Wo finde ich diese Nummer?",
    text: "Wenn Sie sich beim Steuerlotsen erfolgreich registriert haben, bekommen Sie von Ihrer Finanzverwaltung einen Brief mit Ihrem persönlichen Freischaltcode zugeschickt. Den Freischaltcode finden Sie auf der letzten Seite des Briefes.",
  },
};
