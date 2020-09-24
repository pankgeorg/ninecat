import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import {
  ApolloClient,
  ApolloProvider,
  InMemoryCache,
  HttpLink
} from "@apollo/client";
import HomePage from "./pages/HomePage";
import Navigation from "./pages/Navigation";
import PharmaMap from "./pages/PharmaMap";
import DadTools from "./pages/DadTools";
import WeatherStation from "./pages/WeatherStation";
import { root, tools, pharma, weather, hasura as uri } from "./constants";

const createApolloClient = authToken => {
  return new ApolloClient({
    link: new HttpLink({
      uri
      /* headers: {
        Authorization: `Bearer ${authToken}`
      } */
    }),
    cache: new InMemoryCache()
  });
};

export default () => {
  const client = createApolloClient();

  return (
    <>
      <ApolloProvider client={client}>
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

            <Route path={weather} exact>
              <WeatherStation />
            </Route>
          </Switch>
        </Router>
      </ApolloProvider>
    </>
  );
};
