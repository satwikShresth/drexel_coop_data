import React, { useState } from 'react';

interface TextInputProps { id: string; label: string; }
export const TextInput: React.FC<TextInputProps> = ({ id, label }) => {
   return (
      <div className="mb-4">
         <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor={id}>
            {label}
         </label>
         <input
            id={id}
            type="text"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
         />
      </div>
   );
};

interface RangeInputProps { id: string; label: string; min: number; max: number; unit?: string; showNotApplicable?: boolean; }
export const RangeInput: React.FC<RangeInputProps> = ({ id, label, min, max, unit, showNotApplicable }) => {
   const [value, setValue] = useState<number>(min);
   const [notApplicable, setNotApplicable] = useState<boolean>(false);

   const handleRangeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setValue(parseInt(event.target.value, 10));
   };

   const handleCheckboxChange = () => {
      setNotApplicable(!notApplicable);
   };

   return (
      <div className="mb-4">
         <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor={id}>
            {label}
         </label>
         <div className="flex items-center">
            <input
               id={id}
               type="range"
               min={min}
               max={max}
               value={value}
               onChange={handleRangeChange}
               className="flex-grow"
               disabled={notApplicable}
            />
            <span className="ml-4 text-gray-700">{value} {unit}</span>
         </div>
         {showNotApplicable && (
            <div className="mt-2">
               <label className="inline-flex items-center">
                  <input
                     type="checkbox"
                     className="form-checkbox"
                     checked={notApplicable}
                     onChange={handleCheckboxChange}
                  />
                  <span className="ml-2">Not Applicable</span>
               </label>
            </div>
         )}
      </div>
   );
};

interface CheckboxProps { label: string; }
export const Checkbox: React.FC<CheckboxProps> = ({ label }) => {
   return (
      <div className="mt-2">
         <label className="inline-flex items-center">
            <input
               type="checkbox"
               className="form-checkbox"
            />
            <span className="ml-2">{label}</span>
         </label>
      </div>
   );
};

interface RadioGroupProps { name: string; options: string[]; label: string; }
export const RadioGroup: React.FC<RadioGroupProps> = ({ name, options, label }) => {
   return (
      <div className="mb-4">
         <label className="block text-gray-700 text-sm font-bold mb-2">
            {label}
         </label>
         <div className="flex">
            {options.map((option) => (
               <label key={option} className="inline-flex items-center mr-4">
                  <input
                     type="radio"
                     name={name}
                     value={option}
                     className="form-radio"
                  />
                  <span className="ml-2">{option}</span>
               </label>
            ))}
         </div>
      </div>
   );
};
