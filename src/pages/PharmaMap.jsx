import React, { useState, useCallback, useMemo } from "react";
import { Select } from "@blueprintjs/select";
import { Button, MenuItem, Radio, RadioGroup } from "@blueprintjs/core";
import { useQuery, gql } from "@apollo/client";
import css from "./PharmaMap.module.css";

const PharmaSelect = ({ onSelect = () => {} }) => {
  const [pharmacy, setPharmacyInternal] = useState(null);
  const setPharmacy = useCallback(
    item => setPharmacyInternal(item) || onSelect(item),
    [onSelect]
  );
  const [qText, setQText] = useState(null);
  const setText = useCallback(t => setQText(`%${t}%`), [setQText]);
  const { loading, data: { pharmacy: data } = {} } = useQuery(
    gql`
      query Pharmacy($qText: String) {
        pharmacy(
          where: {
            _or: [
              { address: { _ilike: $qText } }
              { name: { _ilike: $qText } }
              { tel: { _ilike: $qText } }
              { area: { _ilike: $qText } }
            ]
          }
        ) {
          address
          area
          id
          name
          tel
          type
          updated_at
        }
      }
    `,
    { variables: { qText } }
  );
  return (
    <Select
      items={(!loading && data?.length && data) || []}
      onQueryChange={setText}
      onItemSelect={setPharmacy}
      popoverProps={{ className: css.list, usePortal: false }}
      itemRenderer={(
        { name, area, address, id, tel },
        { handleClick, modifiers }
      ) => (
        <MenuItem
          key={id}
          active={modifiers.active}
          label={tel}
          onClick={handleClick}
          text={`${name}, ${address} ${area}`}
        />
      )}
      noResults={<MenuItem disabled text="No results." />}
    >
      <Button
        text={pharmacy?.name || "Select Pharmacy"}
        rightIcon="double-caret-vertical"
      />
    </Select>
  );
};

const AreaSelect = ({ onSelect = () => {}, selectedValue }) => {
  const [item, setItemInternal] = useState(null);
  const setItem = useCallback(
    ({ area }) => setItemInternal(area) || onSelect(area),
    [onSelect]
  );
  const [qText, setQText] = useState(null);
  const setText = useCallback(t => setQText(`%${t}%`), [setQText]);
  const { loading, data: { items: data } = {} } = useQuery(
    gql`
      query Pharmacy($qText: String) {
        items: pharmacy(
          where: { area: { _ilike: $qText } }
          distinct_on: area
        ) {
          area
        }
      }
    `,
    { variables: { qText } }
  );
  return (
    <Select
      items={(!loading && data?.length && data) || []}
      onQueryChange={setText}
      onItemSelect={setItem}
      popoverProps={{ className: css.list, usePortal: false }}
      itemRenderer={({ area }, { handleClick, modifiers }) => (
        <MenuItem
          key={area}
          active={modifiers.active}
          onClick={handleClick}
          text={area}
        />
      )}
      noResults={<MenuItem disabled text="No results." />}
    >
      <Button
        text={item || selectedValue || "Select area"}
        rightIcon="double-caret-vertical"
      />
    </Select>
  );
};

const fmtDate = date =>
  `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
export default () => {
  const today = useMemo(() => fmtDate(new Date()), []);
  const tomorrow = useMemo(
    () => fmtDate(new Date(+new Date() + 86400000)),
    []
  );
  const in2Days = useMemo(
    () => fmtDate(new Date(+new Date() + 2 * 86400000)),
    []
  );

  const [area, setArea] = useState("ΑΜΠΕΛΟΚΗΠΟΙ");
  const [date, setDate] = useState(today);
  const { loading, data: { duty: data } = {} } = useQuery(
    gql`
      query Duties($date: date, $area: String) {
        duty: pharmacy_duty(
          order_by: [{ area: asc_nulls_last }, { updated_at: desc_nulls_last }]
          where: { date: { _eq: $date }, area: { _eq: $area } }
        ) {
          id
          name
          time
          date
          area
          pharmacy {
            address
            name
            area
            tel
            places {
              lat
              lng
            }
          }
        }
      }
    `,
    { variables: { date, area } }
  );
  return (
    <>
      <AreaSelect onSelect={setArea} selectedValue={area} />
      <PharmaSelect area />
      <RadioGroup
        label=""
        onChange={e => setDate(e.target.value)}
        selectedValue={date}
      >
        <Radio label={`Today ${today}`} value={today} />
        <Radio label={`Tomorrow ${tomorrow}`} value={tomorrow} />
        <Radio label={in2Days} value={in2Days} />
      </RadioGroup>
      <table className="bp3-html-table .modifier">
        <thead>
          <tr>
            <th>ΦΑΡΜΑΚΕΙΟ</th>
            <th>ΗΜ/ΝΙΑ</th>
            <th>ΠΕΡΙΟΧΗ</th>
            <th>ΩΡΑ</th>
            <th>ΔΙΕΥΘΥΝΣΗ</th>
          </tr>
        </thead>
        <tbody>
          {!loading &&
            data?.map(
              ({
                id,
                name,
                date: d,
                area: a,
                time,
                pharmacy: { address, places: [{ lng, lat }] = [{}] } = {}
              }) => (
                <tr key={id}>
                  <td>{name}</td>
                  <td>{d}</td>
                  <td>{a}</td>
                  <td>{time}</td>
                  <td>{address}</td>
                  <td>
                    <code>
                      {lng}, {lat}
                    </code>
                  </td>
                  <td>
                    <img
                      alt="Pharmacy map"
                      src={`https://maps.googleapis.com/maps/api/staticmap?center=${lat},${lng}&zoom=16&markers=color:orange|"${lat},${lng}"&size=400x400&key=AIzaSyAMhdXXo_RO9fPYMOT97jMWBVTkYQ03b4s`}
                    />
                  </td>
                </tr>
              )
            )}
        </tbody>
      </table>
    </>
  );
};
