import React from "react";
import { Link } from "react-router-dom";

const MenuItemLink = props => {
  const { to, href, icon, text } = props;
  const handleLinkClick = e => e.target.parentElement.parentElement.click();

  return (
    <Link
      onClick={handleLinkClick}
      to={to || href}
      className={`bp3-button bp3-minimal bp3-icon-${icon}`}
    >
      {text}
    </Link>
  );
};
export default MenuItemLink;
