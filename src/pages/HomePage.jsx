import React from "react";
import { H3, Card, Elevation, Tag } from "@blueprintjs/core";
import cls from "classnames";
import styles from "./HomePage.module.css";

const HomePage = props => {
  const clContainer = cls(
    styles.container,
    "pa2",
    "justify-center",
    "flex",
    "items-center"
  );

  const clTagbox = cls(styles.tagBox, "flex", "flex-wrap", "mt5");
  const tags = [
    "JavaScript",
    "React",
    "Python",
    "SQL",
    "MS/Excel",
    "Washing dishes",
    "Sailing"
  ];
  return (
    <div className={clContainer}>
      <Card elevation={Elevation.TWO} interactive>
        <H3>Hey, it&apos;s Panagiotis</H3>
        <pre>
          Software Engineer, sailor
          <br />
          Working for intelligencia.ai
          <br />
          in the bright city of Athens
        </pre>
        <div className={clTagbox}>
          <div className="w-two-thirds">
            {tags.map(tag => (
              <Tag className="mb2 mr2" minimal round key={tag}>
                {tag}
              </Tag>
            ))}
          </div>
        </div>
        <code className="mt4 db">
          <a
            target="_blank"
            rel="noreferrer noopener"
            href="mailto:pankgeorg@gmail.com"
          >
            mail me?
          </a>
        </code>
      </Card>
    </div>
  );
};
export default HomePage;
