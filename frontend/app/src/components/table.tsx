import { useState, useEffect } from "react";

export default function Table(): any {

   const [data, setData] = useState<any[]>([]);
   const [headers, setHeaders] = useState<string[]>([]);
   const [loading, setLoading] = useState<boolean>(true);
   const [error, setError] = useState<string | null>(null);

   useEffect(() => {
      // Fetch data from the API
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
               setHeaders(Object.keys(data[0]));
            }
            setLoading(false);
         })
         .catch(error => {
            setError(`Error fetching data: ${error.message}`);
            setLoading(false);
         });
   }, []);

   if (loading) {
      return <div>Loading...</div>;
   }

   if (error) {
      return <div>{error}</div>;
   }

   return (
      <table className="min-w-full bg-white border border-gray-200 mt-4">
         <thead>
            <tr>
               {headers.map((header) => (
                  <th key={header} className="py-2 px-4 border-b">{header}</th>
               ))}
            </tr>
         </thead>
         <tbody>
            {data.map((item, index) => (
               <tr key={index}>
                  {headers.map((header) => (
                     <td key={header} className="py-2 px-4 border-b">{item[header]}</td>
                  ))}
               </tr>
            ))}
         </tbody>
      </table>
   );

};
