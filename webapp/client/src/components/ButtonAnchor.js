import PropTypes from "prop-types";
import styled from "styled-components";

const Button = styled.button`
   {
    box-sizing: border-box;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: var(--button-height);
    font-size: var(--text-medium);
    font-family: var(--font-bold);
    line-height: 1;
    color: var(--inverse-text-color);
    background-color: var(--link-color);
    cursor: pointer;
    text-decoration: none;
    border: none;
    padding: 18px 16px;
    transition: color var(--transition-behaviour) var(--transition-time),
      background-color var(--transition-behaviour) var(--transition-time),
      background var(--transition-behaviour) var(--transition-time);

    &.outline {
      color: var(--text-color);
      background-color: var(--inverse-text-color);
      outline: 1px solid var(--border-color);
    }

    &.narrow {
      height: var(--button-height-narrow);
    }

    &.high {
      height: var(--button-height-high);
    }

    &:active,
    &.active {
      background-color: var(--link-active-hover-color);
      color: var(--inverse-text-color);
    }

    &:hover {
      color: var(--inverse-text-color);
      background-color: var(--link-hover-color);
      text-decoration: none;

      .anchor-btn__icon.translate-x {
        transform: translatex(10%);
      }

      &:active,
      &.active {
        background-color: var(--link-active-hover-color);
      }
    }

    &:focus-visible {
      color: var(--focus-text-color);
      outline: none;
      box-shadow: none;
      background: linear-gradient(
        var(--focus-color) calc(100% - 4px),
        var(--focus-text-color) 4px
      );
    }
  }
`;
const AnchorButtonText = styled.span`
   {
    padding: 0 8px;
  }
`;
const AnchorButtonIcon = styled.span`
   {
    padding: 0 8px;

    svg {
      display: block;
      margin: auto;
      max-height: 36px;
      max-width: 36px;
    }
  }
`;

function Text({ children }) {
  return (
    <AnchorButtonText className="anchor-btn__text">{children}</AnchorButtonText>
  );
}

Text.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]).isRequired,
};

function Icon({ children, hoverVariant }) {
  const iconClasses = `anchor-btn__icon ${hoverVariant}`;

  return (
    <AnchorButtonIcon className={iconClasses}>{children}</AnchorButtonIcon>
  );
}

Icon.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]).isRequired,
  hoverVariant: PropTypes.oneOf(["translate-x"]),
};
Icon.defaultProps = {
  hoverVariant: null,
};

export default function ButtonAnchor({
  children,
  onClick,
  url,
  name,
  download,
  variant,
  buttonStyle,
  additionalClass,
  external,
}) {
  const btnClasses = `anchor-btn ${variant} ${buttonStyle} ${
    additionalClass || ""
  }`;
  const relation = [];
  let target = false;
  if (external) {
    target = "_blank";
    relation.push("noopener");
  }

  return (
    <Button
      as={url ? "a" : ""}
      className={btnClasses}
      href={url}
      name={name}
      download={download}
      external={external}
      target={target || undefined}
      rel={url ? relation : undefined}
      onClick={onClick}
    >
      {children}
    </Button>
  );
}

ButtonAnchor.Text = Text;
ButtonAnchor.Icon = Icon;

ButtonAnchor.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]).isRequired,
  onClick: PropTypes.func,
  url: PropTypes.string,
  name: PropTypes.string,
  download: PropTypes.bool,
  external: PropTypes.bool,
  buttonStyle: PropTypes.oneOf(["default", "narrow", "high"]),
  variant: PropTypes.oneOf(["primary", "outline"]),
  additionalClass: PropTypes.string,
};

ButtonAnchor.defaultProps = {
  url: undefined,
  onClick: undefined,
  name: undefined,
  download: false,
  external: false,
  variant: "primary",
  buttonStyle: "default",
  additionalClass: undefined,
};
