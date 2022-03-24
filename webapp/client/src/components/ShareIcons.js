import React from "react";
import { SocialIcon } from "react-social-icons";
import { isMobile } from "react-device-detect";
import styled from "styled-components";
import PropTypes from "prop-types";
import addPlausibleGoal from "../lib/helpers";

const FacebookIcon = styled(SocialIcon)`
  // This is needed for the hover effect on the background when going over the icon
  .social-svg-icon:hover + .social-svg-mask {
    fill: #2f4779 !important;
  }

  .social-svg-mask:hover {
    fill: #2f4779 !important;
  }
`;

const WhatsappIcon = styled(SocialIcon)`
  .social-svg-icon:hover + .social-svg-mask {
    fill: #25c05f !important;
  }

  .social-svg-mask:hover {
    fill: #25c05f !important;
  }
`;

const EmailIcon = styled(SocialIcon)`
  .social-svg-icon:hover + .social-svg-mask {
    fill: #6b6b6d !important;
  }

  .social-svg-mask:hover {
    fill: #6b6b6d !important;
  }
`;

export default function ShareIcons({
  promoteUrl,
  shareText,
  mailSubject,
  sourcePage,
  plausibleDomain,
}) {
  const facebookFeedUrl = `https://www.facebook.com/sharer/sharer.php?u=${promoteUrl}&quote=${shareText}`;
  const mailto = `mailto:?subject= ${encodeURIComponent(
    mailSubject
  )}&body=${encodeURIComponent(shareText)}`;
  const whatsappText = `https://wa.me?text=${shareText}`;
  return (
    <div>
      <FacebookIcon
        className="mr-2"
        network="facebook"
        url={facebookFeedUrl}
        target="_blank"
        onClick={() =>
          addPlausibleGoal(plausibleDomain, "Facebook icon clicked", {
            method: sourcePage,
          })
        }
      />
      {isMobile && (
        <WhatsappIcon
          className="mr-2"
          network="whatsapp"
          url={whatsappText}
          onClick={() =>
            addPlausibleGoal(plausibleDomain, "Whatsapp icon clicked", {
              method: sourcePage,
            })
          }
        />
      )}
      <EmailIcon
        network="email"
        url={mailto}
        onClick={() =>
          addPlausibleGoal(plausibleDomain, "Email icon clicked", {
            method: sourcePage,
          })
        }
      />
    </div>
  );
}

ShareIcons.propTypes = {
  promoteUrl: PropTypes.string.isRequired,
  shareText: PropTypes.string.isRequired,
  mailSubject: PropTypes.string.isRequired,
  sourcePage: PropTypes.string.isRequired,
  plausibleDomain: PropTypes.string,
};

ShareIcons.defaultProps = {
  plausibleDomain: null,
};