import React from "react";
import css from "./HomePage.module.css";

const WeatherStation = () => {
  return (
    <div className={css.weatherContainer}>
      <pre>
        Measurements at Neo Psychiko. BME680 sensor, Arduino UNO WiFi. Still in
        development!
      </pre>
      <div className={css.weatherFrames}>
        <iframe
          title="Map of Neo Psychiko"
          src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d2568.4506037981296!2d23.781829902238808!3d38.00230216426231!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sen!2sgr!4v1600930911444!5m2!1sen!2sgr"
          width="600"
          height="400"
          style={{ border: 0 }}
          allowFullScreen=""
          aria-hidden="false"
          tabIndex="0"
        />
        <iframe
          title="Weather status in Neo Psychiko"
          src="https://metabase.pankgeorg.com/public/question/b4ecb030-bb7d-48db-837e-00597bfc860b"
          frameBorder="0"
          width="800"
          height="400"
          allowtransparency
        />
      </div>
    </div>
  );
};

export default WeatherStation;
