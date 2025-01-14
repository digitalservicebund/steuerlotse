import PropTypes from "prop-types";
import { React, useState } from "react";
import StepNavButtons from "./StepNavButtons";
import { waitingMomentMessagePropType } from "../lib/propTypes";

export default function StepFormAsync({
  children,
  action,
  csrfToken,
  explanatoryButtonText,
  showOverviewButton,
  nextButtonLabel,
  plausibleGoal,
  plausibleDomain,
  plausibleProps,
  sendDisableCall,
  waitingMessages,
}) {
  const [loading, setLoading] = useState(false);
  // eslint-disable-next-line no-promise-executor-return
  const delay = (ms) => new Promise((res) => setTimeout(res, ms));

  async function makeFetchCall(formData) {
    const startTime = Date.now();

    fetch(action, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        const endTime = Date.now();
        const duration = endTime - startTime;
        const firstMinDuration = 2000;
        const spinnerMessageChangeTime = 10000;
        const secondMinDuration = 12000;

        if (duration < firstMinDuration) {
          return Promise.resolve(delay(firstMinDuration - duration)).then(
            () => response
          );
        }
        if (
          duration > spinnerMessageChangeTime &&
          duration < secondMinDuration
        ) {
          return Promise.resolve(delay(secondMinDuration - duration)).then(
            () => response
          );
        }

        return response;
      })
      .then((response) => {
        if (response.redirected) {
          window.location = response.url;
        } else if (response.ok) {
          return response.text();
        }
        return Promise.reject(response);
      })
      .then((text) => {
        const parser = new DOMParser();
        const htmlDoc = parser.parseFromString(text, "text/html");
        document.body.innerHTML = htmlDoc.body.innerHTML;
        window.renderReact();
      })
      .catch((error) => {
        console.log(error);
      });
  }

  function sendDisableCallAndFetch(event) {
    event.preventDefault();
    const { target } = event;

    const formData = new FormData(target);

    if (sendDisableCall !== undefined) {
      setLoading(true);
      sendDisableCall();
    }

    makeFetchCall(formData);
  }

  return (
    <form id="theForm" noValidate onSubmit={sendDisableCallAndFetch}>
      <input type="hidden" name="csrf_token" value={csrfToken} />
      {children}
      <StepNavButtons
        explanatoryButtonText={explanatoryButtonText}
        showOverviewButton={showOverviewButton}
        nextButtonLabel={nextButtonLabel}
        plausibleGoal={plausibleGoal}
        plausibleDomain={plausibleDomain}
        plausibleProps={plausibleProps}
        loading={loading}
        waitingMessages={waitingMessages}
      />
    </form>
  );
}

StepFormAsync.propTypes = {
  children: PropTypes.node,
  action: PropTypes.string.isRequired,
  csrfToken: PropTypes.string.isRequired,
  showOverviewButton: PropTypes.bool,
  explanatoryButtonText: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.element,
  ]),
  nextButtonLabel: PropTypes.string,
  plausibleGoal: PropTypes.string,
  plausibleProps: PropTypes.shape({ method: PropTypes.string }),
  plausibleDomain: PropTypes.string,
  sendDisableCall: PropTypes.any,
  waitingMessages: waitingMomentMessagePropType,
};

StepFormAsync.defaultProps = {
  ...StepNavButtons.defaultProps,
  sendDisableCall: undefined,
  waitingMessages: undefined,
};
