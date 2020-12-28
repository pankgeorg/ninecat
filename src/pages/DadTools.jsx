import React from "react";
import c from "classnames";
import {
  H5,
  Callout,
  Position,
  ProgressBar,
  Card,
  FileInput,
  Button,
  Collapse,
  Menu,
  Toaster
} from "@blueprintjs/core";
import { Column, Table, CopyCellsMenuItem } from "@blueprintjs/table";
import styles from "./DadTools.module.css";
import {
  FETCH_STATES,
  inputId,
  backendURL,
  dadFileUploadURL
} from "../constants";

const INITIAL_TEXT = "Επιλέξτε αρχείο";
const DadTools = props => {
  const toasterRef = React.useRef(null);
  const [buttonText, setButtonText] = React.useState(INITIAL_TEXT);
  const [response, setResponse] = React.useState(null);
  const [responseReady, setResponseReady] = React.useState(
    FETCH_STATES.NOT_STARTED
  );
  const [collapseOpen, setCollapseOpen] = React.useState(false);
  const reset = () => {
    setButtonText(INITIAL_TEXT);
    setResponse(null);
    setResponseReady(FETCH_STATES.NOT_STARTED);
    setCollapseOpen(false);
    document.getElementById(inputId).value = "";
    document.getElementById(inputId).type = "";
    document.getElementById(inputId).type = "file";
  };

  const upload = file => {
    const formData = new FormData();
    formData.append("file", file);
    setResponseReady(FETCH_STATES.STARTED);
    fetch(backendURL + dadFileUploadURL, {
      method: "POST",
      body: formData
    })
      .then(resp => {
        setResponseReady("got reply");
        if (resp.ok) return resp.json(); // if the response is a JSON object
        throw new Error("Network response was not ok");
      })
      .then(success => {
        setResponseReady(FETCH_STATES.SUCCESS);
        setResponse(success);
      })
      .catch(error => {
        setResponseReady(FETCH_STATES.ERROR);
        setResponse(null);
      });
  };

  const handleFiles = e => {
    const inputElem = document.getElementById(inputId);
    const { files } = inputElem;
    if (!files || !files.length === 1) return;
    setButtonText(`Επιλέχθηκε το αρχείο ${files[0].name}`);
    upload(files[0]);
  };

  const renderBodyContextMenu = table => context => {
    return (
      <Menu>
        <CopyCellsMenuItem
          context={context}
          getCellData={(row, col) => table?.[row]?.[col]}
          text="Copy"
        />
      </Menu>
    );
  };
  return (
    <div
      className={c(
        "ma2",
        "flex",
        "flex-wrap",
        "justify-center",
        styles.container
      )}
    >
      <Toaster ref={toasterRef} position={Position.TOP_RIGHT} />
      <div className={c("flex", "flex-column", "w-75", "mw8-ns")}>
        <Card className={c("flex", "flex-column", "justify-center")}>
          <H5>Ανεβάστε το pdf</H5>
          <div className={c("flex", "justify-between", "items-center")}>
            <FileInput
              className={c("w-75")}
              text={buttonText}
              onInputChange={handleFiles}
              inputProps={{ id: inputId }}
              large
            />
            <div>
              <Button intent="danger" icon="cross" onClick={reset}>
                Μηδενισμός
              </Button>
            </div>
          </div>
        </Card>
        <div className={c("w-100")}>
          <br />
          {responseReady === FETCH_STATES.NOT_STARTED && ""}
          {responseReady === FETCH_STATES.STARTED && (
            <>
              <div>Loading...</div>
              <ProgressBar animate intent="success" stripes />
            </>
          )}
          {responseReady === FETCH_STATES.SUCCESS && response && (
            <>
              <Callout intent="success" className={c("bp3-running-text")}>
                <H5>Επιτυχία</H5>
                <div className={c("mw6")}>
                  Η μεταφόρτωση και η επεξερασία ολοκληρώθηκαν. Τα περιεχόμενα
                  του αρχείου βρίσκονται διαθέσιμα προς μεταφόρτωση για τα
                  επόμενα 10 λεπτά στον παρακάτω σύνδεσμο. Οι προεπιλεγμένες
                  τιμές εμφανίζονται και στον παρακάτω πίνακα.
                </div>
                <ul>
                  <li>
                    Κατεβάστε το{" "}
                    <a
                      download
                      href={backendURL + response.pdfDownload}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      pdf
                    </a>
                    <br /> ή
                  </li>
                  <li>
                    Κατεβάστε το{" "}
                    <a
                      download
                      href={backendURL + response.excelDownload}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      excel{" "}
                    </a>
                    <br /> ή
                  </li>
                  <li>
                    Αντιγράψτε τα δεδομένα για επικόλληση σε Excel
                    <br /> ή
                  </li>
                  <li>δείτε τον πίνακα, επιλέξτε όλα τα κελιά</li>
                </ul>
              </Callout>
              <div className={c("flex")}>
                <Button
                  className={c("mv2")}
                  onClick={() => setCollapseOpen(!collapseOpen)}
                >
                  {(!collapseOpen && "άνοιγμα ") || "κλείσιμο "} πίνακα
                </Button>{" "}
                <div className={c("w1")} />
                <Button
                  intent="primary"
                  className={c("mv2")}
                  onClick={() => {
                    const csv = response.table
                      .map(row => row.join("\t"))
                      .join("\n");
                    const csvBlob = new Blob([csv], { type: "text/plain" });
                    const newItem = new window.ClipboardItem({
                      "text/plain": csvBlob
                    });
                    navigator.clipboard.write([newItem]).then(
                      success =>
                        toasterRef.current.show({
                          icon: "check",
                          message:
                            "Ο πίνακας αντιγράφηκε! Δοκιμάστε επικόλληση στο Excel",
                          intent: "success"
                        }),
                      fail =>
                        toasterRef.current.show({
                          icon: "cross",
                          message: "Αποτυχία αντιγραφής",
                          intent: "danger"
                        })
                    );
                  }}
                >
                  αντιγραφή{" "}
                </Button>
              </div>
              <Collapse isOpen={collapseOpen}>
                <Table
                  enableFocus="true"
                  enableFocusedCell="true"
                  defaultColumnWidth={75}
                  getCellClipboardData={(row, col) =>
                    response.table?.[row]?.[col]
                  }
                  numRows={3}
                  bodyContextMenuRenderer={renderBodyContextMenu(
                    response.table || [[]]
                  )}
                >
                  {response.table[0]?.map((i, t) => (
                    <Column
                      key={t}
                      width="2em"
                      cellRenderer={(row, col) => (
                        <span>{response?.table?.[row]?.[col]}</span>
                      )}
                    />
                  ))}
                </Table>
              </Collapse>
            </>
          )}
          {responseReady === FETCH_STATES.ERROR && "error"}
        </div>
      </div>
    </div>
  );
};

export default DadTools;
