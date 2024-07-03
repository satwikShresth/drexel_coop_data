import React, { useEffect, useState } from "react";
import TableComponent from "./../components/table/table";

const Table: React.FC = () => {
   const [data, setData] = useState<any[]>([]);
   const [headers, setHeaders] = useState<{ accessorKey: string; header: string }[]>([]);
   const [loading, setLoading] = useState<boolean>(true);
   const [error, setError] = useState<string | null>(null);

   useEffect(() => {
      fetch('http://localhost:8000/data')
         .then(response => {
            if (!response.ok) {
               throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
         })
         .then(data => {
            setData(data);
            if (data.length > 0) {
               setHeaders(Object.keys(data[0]).map(key => ({
                  accessorKey: key,
                  header: key.charAt(0).toUpperCase() + key.slice(1),
               })));
            }
            setLoading(false);
         })
         .catch(error => {
            setError(`Error fetching data: ${error.message}`);
            setLoading(false);
         });
   }, []);


   return (
      <TableComponent
         data={data}
         headers={headers}
         loading={loading}
         error={error}
      />
   );
};

export default Table;
