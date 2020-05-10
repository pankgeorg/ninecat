import React from "react";
import { Navbar, Alignment, Button, Menu, Popover } from "@blueprintjs/core";
import MenuItemLink from "../components/MenuItemLink";
import ButtonLink from "../components/ButtonLink";
import { root, tools } from "../constants";

export default () => (
  <Navbar>
    <Navbar.Group align={Alignment.LEFT}>
      <Navbar.Heading>Panagiotis</Navbar.Heading>
      <Navbar.Divider />
      <ButtonLink to={root} className="bp3-minimal" icon="code" text="Home" />
      <Popover
        content={
          <Menu>
            <MenuItemLink
              icon="th-derived"
              text="xref pdf to table"
              to={tools}
            />
          </Menu>
        }
      >
        <Button className="bp3-minimal" icon="build" text="Tools" />
      </Popover>
    </Navbar.Group>
  </Navbar>
);
