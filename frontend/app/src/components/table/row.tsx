import React, { useState } from 'react';

interface RowProps {
   item: any;
   headers: string[];
}

const RowComponent: React.FC<RowProps> = ({ item, headers }) => {
   const [isOpen, setIsOpen] = useState(false);

   return (
      <>
         <tr onClick={() => setIsOpen(!isOpen)}>
            {headers.map((header) => (
               <td key={header} className="py-2 px-4 border-b">{item[header]}</td>
            ))}
         </tr>
         {isOpen && (
            <tr>
               <td colSpan={headers.length} className="py-2 px-4 border-b">
                  {/* Additional details or content can go here */}
                  Expanded content for {item[headers[0]]}
               </td>
            </tr>
         )}
      </>
   );
};

export default RowComponent;
