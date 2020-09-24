import React from "react";
import { useQuery, gql } from "@apollo/client";

const PharmaMap = () => {
  const { loading, error, data } = useQuery(gql`
    query Pharmacy {
      pharmacy {
        address
        area
        id
        name
        tel
        type
        updated_at
      }
    }
  `);
  console.log(loading, error, data);
  return <div>test</div>;
};
export default PharmaMap;
