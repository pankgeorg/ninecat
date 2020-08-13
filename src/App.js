import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import Navigation from "./pages/Navigation";
import PharmaMap from "./pages/PharmaMap";
import DadTools from "./pages/DadTools";
import { root, tools, pharma } from "./constants";

export default () => (
  <>
    <Router>
      <Navigation />
      <Switch>
        <Route path={pharma} exact>
          <PharmaMap />
        </Route>
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
