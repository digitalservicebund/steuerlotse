import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import { ReactComponent as FailureIcon } from "../assets/icons/failure_icon.svg";

export default function DisplayFailureIcon({ title, errorDetails }) {
  const { t } = useTranslation();
  return (
    <div className="section-intro panel simple-card">
      <div className="row p-0">
        <div className="col-12 col-sm-2 failure-success-icon">
          <FailureIcon alt={t("filing.failure.icon_alt")} />
        </div>
        <div className="col-12 col-sm-10">
          <h1 className="headline">{title}</h1>
          {errorDetails.map((errorDetail) => (
            <p className="result-text">{errorDetail}</p>
          ))}
        </div>
      </div>
    </div>
  );
}

DisplayFailureIcon.propTypes = {
  title: PropTypes.string.isRequired,
  errorDetails: PropTypes.array,
};

DisplayFailureIcon.defaultProps = {
  errorDetails: [],
};
