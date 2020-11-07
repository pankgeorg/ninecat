import React from "react";
import css from "./HomePage.module.css";

const WeatherStation = () => {
  return (
    <div className={css.weatherContainer}>
      <pre>Measurements at Neo Psychiko, Greece.</pre>
      <pre>
        BME680 sensor, Feather HUZZAH, coded in Lua. Still in development!
      </pre>
      <div className={css.weatherFrames}>
        <iframe
          title="Weather status in Neo Psychiko"
          src="https://metabase.pankgeorg.com/public/dashboard/680eb6ec-ebdf-4691-ab73-994f14d4540e?created_at=past0days~"
          frameBorder="0"
          width="100%"
          height="400"
          allowtransparency
        />
      </div>
    </div>
  );
};

export default WeatherStation;
