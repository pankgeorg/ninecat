import React from "react";
import { Link } from "react-router-dom";
import { Icon, Classes } from "@blueprintjs/core";

const MenuItemLink = props => {
  const { to, href, icon, text } = props;
  const handleLinkClick = e => e.target.parentElement.parentElement.click();

  return (
    <li className={Classes.POPOVER_DISMISS}>
      <Link
        onClick={handleLinkClick}
        to={to || href}
        className="bp3-menu-item"
      >
        <Icon icon={icon} />
        <div className="bp3-text-overflow-ellipsis bp3-fill">{text}</div>
      </Link>
    </li>
  );
};
export default MenuItemLink;
