import React, { useEffect, useState } from 'react';
import RowComponent from './row'

interface TableProps {
   data: any[];
   headers: string[];
   loading: boolean;
   error: string | null;
   rowsPerPage: number;
}

const TableComponent: React.FC<TableProps> = ({ data, headers, loading, error, rowsPerPage }) => {
   const [currentPage, setCurrentPage] = useState(1);
   const [containerHeight, setContainerHeight] = useState(window.innerHeight - 200); // Initial height minus some offset

   useEffect(() => {
      const handleResize = () => {
         setContainerHeight(window.innerHeight - 100); // Update height minus some offset
      };

      window.addEventListener('resize', handleResize);
      return () => {
         window.removeEventListener('resize', handleResize);
      };
   }, []);

   if (loading) {
      return <div>Loading...</div>;
   }

   if (error) {
      return <div>{error}</div>;
   }

   const startIndex = (currentPage - 1) * rowsPerPage;
   const paginatedData = data.slice(startIndex, startIndex + rowsPerPage);
   const totalPages = Math.ceil(data.length / rowsPerPage);

   const handlePageChange = (newPage: number) => {
      if (newPage >= 1 && newPage <= totalPages) {
         setCurrentPage(newPage);
      }
   };

   return (
      <div className="relative w-full">
         <div className="overflow-auto " style={{ maxHeight: `${containerHeight}px` }}>
            <table className="w-full bg-white border border-gray-200 mt-4">
               <thead className='sticky top-3 bg-white'>
                  <tr>
                     {headers.map((header) => (
                        <th key={header} className="py-2 px-4 border-b">{header}</th>
                     ))}
                  </tr>
               </thead>
               <tbody>
                  {paginatedData.map((item, index) => (
                     <RowComponent key={index} item={item} headers={headers} />
                  ))}
               </tbody>
            </table>
         </div>
         <div className="flex justify-between items-center mt-4">
            <button
               onClick={() => handlePageChange(currentPage - 1)}
               disabled={currentPage === 1}
               className="py-2 px-4 border bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
            >
               Previous
            </button>
            <span>
               Page {currentPage} of {totalPages}
            </span>
            <button
               onClick={() => handlePageChange(currentPage + 1)}
               disabled={currentPage === totalPages}
               className="py-2 px-4 border bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
            >
               Next
            </button>
         </div>
      </div>
   );
};

export default TableComponent;
