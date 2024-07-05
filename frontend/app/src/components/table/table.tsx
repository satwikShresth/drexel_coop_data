import React, { useMemo, useEffect, useState } from 'react';
import {
   useReactTable,
   getCoreRowModel,
   ColumnDef,
   flexRender,
   PaginationState,
} from '@tanstack/react-table';

interface TableProps {
   fetchData: (start: number, end: number) => Promise<any>;
   headers: any[];
   size: number | null;
}

const TableComponent: React.FC<TableProps> = ({ fetchData, headers, size }) => {
   const [data, setData] = useState<any[]>([]);
   const [loading, setLoading] = useState<boolean>(false);
   const [error, setError] = useState<string | null>(null);
   const [pagination, setPagination] = useState<PaginationState>({
      pageIndex: 0,
      pageSize: 10,
   });

   useEffect(() => {
      const fetchPageData = async () => {
         setLoading(true);
         try {
            const fetchedData = await fetchData(
               pagination.pageIndex * pagination.pageSize,
               (pagination.pageIndex + 1) * pagination.pageSize
            );
            setData(fetchedData);
            setLoading(false);
         } catch (err) {
            setError(`Error fetching data: ${(err as Error).message}`);
            setLoading(false);
         }
      };

      fetchPageData();
   }, [fetchData, pagination]);

   const columns = useMemo<ColumnDef<any>[]>(
      () => headers.map((header: string) => ({
         accessorKey: header.toLowerCase(),
         header: header,
      })),
      [headers]
   );

   const table = useReactTable({
      data,
      columns,
      getCoreRowModel: getCoreRowModel(),
      state: {
         pagination,
      },
      onPaginationChange: setPagination,
      manualPagination: true,
      pageCount: (size && size % pagination.pageSize != 0)
         ? (Math.floor(size / pagination.pageSize)) + 1
         : (size) ? Math.floor((size / pagination.pageSize)) : -1,
   });

   if (loading) {
      return <div>Loading...</div>;
   }

   if (error) {
      return <div>Error: {error}</div>;
   }

   const GotoPage: React.FC = () => {
      return (
         <div className="items-center rounded mt-4 w-20 h-15 focus:outline-none focus:ring-2 focus:ring-blue-500" >
            <label className="font-semibold text-gray-700 text-sm">Go to page:</label>
            <input
               className="border border-gray-300 rounded p-2 w-15 h-9 focus:outline-none focus:ring-2 focus:ring-blue-500"
               type="number"
               defaultValue={table.getState().pagination.pageIndex + 1}
               onChange={e => {
                  const page = e.target.value ? Number(e.target.value) - 1 : 0;
                  table.setPageIndex(page);
               }}
            />
         </div>

      )
   }

   const PrevNextButtons: React.FC = () => {
      return (
         <div className="flex gap-9 mt-4">
            <button
               className="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75"
               onClick={() => table.previousPage()}
               disabled={!table.getCanPreviousPage()}
            >
               {'prev'}
            </button>
            <span className="flex items-center gap-2">
               <div>Page</div>
               <strong>
                  {table.getState().pagination.pageIndex + 1} of{' '}
                  {table.getPageCount().toLocaleString()}
               </strong>
            </span>
            <button
               className="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75"
               onClick={() => table.nextPage()}
               disabled={!table.getCanNextPage()}
            >
               {'next'}
            </button>
         </div>

      )
   }


   const PageSizeDrop: React.FC = () => {
      return (
         <div className=" items-center rounded focus:outline-none focus:ring-2 focus:ring-blue-500" >
            <label className="font-semibold text-gray-700 text-sm">Show:</label>
            <select
               value={table.getState().pagination.pageSize}
               onChange={e => {
                  table.setPageSize(Number(e.target.value));
               }}
               className="border border-gray-300 p-2 w-15 h-9 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
               {[10, 15, 20, 25, 30, 35, 40, 45, 50].map(pageSize => (
                  <option key={pageSize} value={pageSize}>
                     {pageSize}
                  </option>
               ))}
            </select>
         </div>
      )
   }

   const TableHeaders: React.FC = () => {
      return (
         <thead>
            {table.getHeaderGroups().map((headerGroup) => (
               <tr key={headerGroup.id}>
                  {headerGroup.headers.map((header) => (
                     <th key={header.id} className="px-4 py-2 border">
                        {flexRender(
                           header.column.columnDef.header,
                           header.getContext()
                        )}
                     </th>
                  ))}
               </tr>
            ))}
         </thead>
      )
   }


   const TableBody: React.FC = () => {
      console.log(table.getRowModel().rows[0].getVisibleCells())
      return (
         <tbody>
            {table.getRowModel().rows.map((row) => (
               <tr key={row.id}>
                  {row.getVisibleCells().map((cell) => (
                     <td key={cell.id} className="px-4 py-2 border">
                        {flexRender(
                           cell.column.columnDef.cell,
                           cell.getContext()
                        )}
                     </td>
                  ))}
               </tr>
            ))}
         </tbody>
      )
   }

   return (
      <>
         <div className="flex justify-between items-center gap-2 bg-white">
            <GotoPage />
            <PrevNextButtons />
            <PageSizeDrop />
         </div>

         <div>
            <table className="table-auto w-full">
               <TableHeaders />
               <TableBody />
            </table>
         </div>
      </>
   );
};

export default TableComponent;

