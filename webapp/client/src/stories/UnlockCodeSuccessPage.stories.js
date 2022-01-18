import React from "react";
import UnlockCodeSuccessPage from "../pages/UnlockCodeSuccessPage";

export default {
  title: "Pages/UnlockCodeSuccess",
  component: UnlockCodeSuccessPage,
};

function Template(args) {
  return <UnlockCodeSuccessPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  prevUrl: "/unlock_code_revocation/step/data_input",
  nextUrl: "/unlock_code_request/step/data_input",
  download: true,
  steuerErklaerungLink: "unlock_code_activation/step/data_input",
  vorbereitungsHilfeLink: "/download_preparation",
};
