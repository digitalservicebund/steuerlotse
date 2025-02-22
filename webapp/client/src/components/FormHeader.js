import PropTypes from "prop-types";
import FormHeaderIntro from "./FormHeaderIntro";

export default function FormHeader({ title, intro, hideIntro }) {
  const paragraphs = [].concat(intro); // intro could be an array or a single string/element/object. This will give us an array in both situations.
  return (
    <div className="section-intro">
      <h1 className="section-title">{title}</h1>
      {intro && !hideIntro && <FormHeaderIntro paragraphs={paragraphs} />}
    </div>
  );
}

FormHeader.propTypes = {
  title: PropTypes.string.isRequired,
  intro: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.element,
    PropTypes.object,
    PropTypes.arrayOf(
      PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.element,
        PropTypes.object,
      ])
    ),
  ]),
  hideIntro: PropTypes.bool,
};

FormHeader.defaultProps = {
  intro: undefined,
  hideIntro: false,
};
