import React from "react";
import { Navbar, Alignment, Button, Menu, Popover } from "@blueprintjs/core";
import MenuItemLink from "../components/MenuItemLink";
import ButtonLink from "../components/ButtonLink";

export default () => (
  <Navbar>
    <Navbar.Group align={Alignment.LEFT}>
      <Navbar.Heading>Panagiotis</Navbar.Heading>
      <Navbar.Divider />
      <ButtonLink to="/" className="bp3-minimal" icon="code" text="Home" />
      <Popover
        content={
          <Menu>
            <MenuItemLink
              icon="th-derived"
              text="ΕΛΠΕ pdf to table"
              to="/dadtools"
            />
          </Menu>
        }
      >
        <Button className="bp3-minimal" icon="build" text="dadtools" />
      </Popover>
    </Navbar.Group>
  </Navbar>
);
