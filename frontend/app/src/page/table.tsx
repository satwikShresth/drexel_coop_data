import React, { useEffect, useState } from "react";
import TableComponent from "./../components/table/table";
import axios, { AxiosError, AxiosResponse } from "axios";

const Table: React.FC = () => {
   const [headers, setHeaders] = useState<{ accessorKey: string; header: string }[]>([]);
   const [tableSize, setTableSize] = useState<number>(0);
   const [error, setError] = useState<string | null>(null);

   useEffect(() => {
      fetch('http://localhost:8000/salary/header')
         .then(response => {
            if (!response.ok) {
               throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
         })
         .then((data) => {
            if (data.length > 0) {
               setHeaders(data);
            }
         })
         .catch((error) => setError(`Error fetching data: ${error.message}`));
   }, []);


   useEffect(() => {
      fetch('http://localhost:8000/salary/size')
         .then(response => {
            if (!response.ok) {
               throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
         })
         .then((data) => setTableSize(data))
         .catch((error) => setError(`Error fetching data: ${error.message}`));
   }, []);


   const fetchData = async (start: number, end: number): Promise<any[]> => {
      try {
         const response: AxiosResponse<any[]> = await axios.get(`http://localhost:8000/salary/data`, {
            params: {
               start,
               end,
            },
         });
         return response.data;
      } catch (error: any | AxiosError) {

         if (axios.isAxiosError(error) && error.response) {
            throw new Error(`HTTP error! status: ${error.response.status}`);
         }

         throw new Error(`An unknown error occurred: ${error.message}`);
      }
   };

   const GetTable: React.FC = () => {
      return (
         (!error)
            ? <TableComponent fetchData={fetchData} headers={headers} size={tableSize} />
            : <div> Error: {error} </div>
      );
   };


   return (
      <GetTable />
   );
};

export default Table;
