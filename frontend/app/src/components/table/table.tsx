import React, { useMemo } from 'react';
import {
   useReactTable,
   getCoreRowModel,
   ColumnDef,
   flexRender,
} from '@tanstack/react-table';

interface TableProps {
   data: any[];
   headers: { accessorKey: string; header: string }[];
   loading: boolean;
   error: string | null;
}

const TableComponent: React.FC<TableProps> = ({ data, headers, loading, error }) => {
   const columns = useMemo<ColumnDef<any>[]>(
      () => headers.map(header => ({
         accessorKey: header.accessorKey,
         header: header.header,
      })),
      [headers]
   );

   const table = useReactTable({
      data,
      columns,
      getCoreRowModel: getCoreRowModel(),
   });

   if (loading) {
      return <div>Loading...</div>;
   }

   if (error) {
      return <div>Error: {error}</div>;
   }

   return (
      <table className="table-auto w-full">
         <thead>
            {table.getHeaderGroups().map(headerGroup => (
               <tr key={headerGroup.id}>
                  {headerGroup.headers.map(header => (
                     <th key={header.id} className="px-4 py-2 border">
                        {flexRender(header.column.columnDef.header, header.getContext())}
                     </th>
                  ))}
               </tr>
            ))}
         </thead>
         <tbody>
            {table.getRowModel().rows.map(row => (
               <tr key={row.id}>
                  {row.getVisibleCells().map(cell => (
                     <td key={cell.id} className="px-4 py-2 border">
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                     </td>
                  ))}
               </tr>
            ))}
         </tbody>
      </table>
   );
};

export default TableComponent;


