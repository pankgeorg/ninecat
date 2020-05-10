import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import Navigation from "./pages/Navigation";
import DadTools from "./pages/DadTools";
import { root, tools } from "./constants";

export default () => (
  <>
    <Router>
      <Navigation />
      <Switch>
        <Route path={root} exact>
          <HomePage />
        </Route>
        <Route path={tools} exact>
          <DadTools />
        </Route>
      </Switch>
    </Router>
  </>
);
