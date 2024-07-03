import React, { useState } from 'react';

interface RowProps {
   item?: any;
   callback?: any;
   headers: string[];
}
export const RowIter: React.FC<RowProps> = ({ callback, headers }) => {
   return (
      <>
         {
            headers.map(
               (header: any) => (
                  <td key={header} className="py-2 px-4 border-b">{callback(header)}</td>
               )
            )
         }
      </>
   );
};

const RowComponent: React.FC<RowProps> = ({ item, headers }) => {
   const [isOpen, setIsOpen] = useState(false);

   return (
      <>
         <tr
            onClick={() => setIsOpen(!isOpen)}
            className={`cursor-pointer ${isOpen ? 'bg-gray-100' : 'hover:bg-gray-50'}`}
         >
            <td className="py-2 px-4 border-b text-center">
               {isOpen ? '-' : '+'}
            </td>
            {
               <RowIter callback={(header: any) => item[header]} headers={headers} />
            }
         </tr>
         {isOpen && (
            <tr>
               <td colSpan={headers.length + 1} className="py-2 px-4 border-b bg-gray-100">
                  {Array.from({ length: 6 }, (_, i) => (
                     <div key={i}>
                        Expanded content for {item[headers[0]]}
                     </div>
                  ))}
               </td>
            </tr>
         )}
      </>
   );
};

export default RowComponent;

