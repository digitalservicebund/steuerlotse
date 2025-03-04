import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldYesNo from "./FormFieldYesNo";

describe("FormFieldYesNo", () => {
  let props;
  const onChangeHandler = jest.fn();

  beforeEach(() => {
    props = {
      fieldName: "fooName",
      fieldId: "fooId",
      label: {
        text: "foo",
      },
      errors: [],
      onChangeHandler,
    };
    render(<FormFieldYesNo {...props} />);
  });

  describe("When Ja clicked", () => {
    const user = userEvent.setup();

    it("should activate Ja field", async () => {
      await user.click(screen.getByText("Ja"));

      expect(screen.getByText("Ja")).toHaveClass("active");
    });

    it("should be checked", async () => {
      await user.click(screen.getByText("Ja"));

      expect(screen.getByLabelText("Ja")).toBeChecked();
    });

    it("should not set active class on Nein field", async () => {
      await user.click(screen.getByText("Ja"));

      expect(screen.getByText("Nein")).not.toHaveClass("active");
    });

    it("should call the change handler with yes", async () => {
      await user.click(screen.getByText("Ja"));

      expect(onChangeHandler).toHaveBeenCalled();

      const changeEvent = onChangeHandler.mock.calls[0][0];
      expect(changeEvent.target.value).toEqual("yes");
    });
  });

  describe("When Nein clicked", () => {
    const user = userEvent.setup();

    it("should activate Nein field", async () => {
      await user.click(screen.getByText("Nein"));

      expect(screen.getByText("Nein")).toHaveClass("active");
    });

    it("should check Nein Field", async () => {
      await user.click(screen.getByText("Nein"));

      expect(screen.getByLabelText("Nein")).toBeChecked();
    });

    it("should not activate Ja field", async () => {
      await user.click(screen.getByText("Nein"));

      expect(screen.getByText("Ja")).not.toHaveClass("active");
    });

    it("should call the change handler with no", async () => {
      await user.click(screen.getByText("Nein"));

      expect(onChangeHandler).toHaveBeenCalled();

      const changeEvent = onChangeHandler.mock.calls[0][0];
      expect(changeEvent.target.value).toEqual("no");
    });
  });

  describe("When using keyboard input", () => {
    const user = userEvent.setup();

    it("should set focus on yes field when pressing tab", async () => {
      await user.tab();

      expect(screen.getByLabelText("Ja")).toHaveFocus();
    });

    it("should keep focus on yes field when pressing tab and then space", async () => {
      await user.tab();
      await user.keyboard(" ");

      expect(screen.getByLabelText("Ja")).toHaveFocus();
    });

    it("should activate Ja Field when pressing tab and then space", async () => {
      await user.tab();
      await user.keyboard(" ");

      expect(screen.getByText("Ja")).toHaveClass("active");
    });

    it("should check Ja Field when pressing tab and then space", async () => {
      await user.tab();
      await user.keyboard(" ");

      expect(screen.getByLabelText("Ja")).toBeChecked();
    });
  });
});
