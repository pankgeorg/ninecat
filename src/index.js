import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import PG from "./pgeorgakopoulos";
import * as serviceWorker from "./serviceWorker";
import "tachyons";

ReactDOM.render(
  <React.StrictMode>
    {window.location.href.indexOf("pankgeorg.com") !== -1 && <PG />}
    {window.location.href.indexOf("silentech.gr") !== -1 && <PG />}
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
