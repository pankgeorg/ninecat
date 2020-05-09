import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import Navigation from "./pages/Navigation";
import DadTools from "./pages/DadTools";

export default () => (
  <>
    <Router>
      <Navigation />
      <Switch>
        <Route path="/" exact>
          <HomePage />
        </Route>
        <Route path="/dadtools" exact>
          <DadTools />
        </Route>
      </Switch>
    </Router>
  </>
);
