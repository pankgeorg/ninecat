import React from "react";

export default () => (
  <>
    <section className="flex vh-75 items-center justify-center washed-yellow bg-dark-green sans-serif">
      <header className="center f1 italics">ας μιλήσουμε</header>
    </section>
    <section className="flex flex-row-ns flex-column items-center justify-between bg-yellow navy">
      <div className="w-20-ns outline pa2 ma2 code flex items-center justify-center">
        <div className="">ready?</div>
      </div>
      <div className="w-20-ns outline pa2 ma2 code flex items-center justify-center">
        <div className="">chat now</div>
      </div>

      <div className="w-20-ns outline pa2 ma2 code flex items-center justify-center">
        <div className="">t</div>
      </div>
      <div className="w-20-ns outline pa2 ma2 code flex items-center justify-center">
        <div className="">about</div>
      </div>
    </section>
    <section className="flex vh-25 outline items-center justify-center dark-green bg-washed-yellow serif">
      <header>find someone to talk to, now</header>
    </section>
    <section className="flex vh-25 items-center justify-center dark-green bg-washed-yellow serif">
      <article className="flex items-center justify-between">
        <div>left for guideline</div>
        <div>right for chat</div>
      </article>
    </section>
  </>
);
