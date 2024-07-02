import React from "react";

interface TableProps { data: any[]; headers: string[]; loading: boolean; error: string | null }
const TableComponent: React.FC<TableProps> = ({ data, headers, loading, error }) => {

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

export default TableComponent;
