import "./form.css"
import 'nouislider/distribute/nouislider.css';
import 'react-datepicker/dist/react-datepicker.css'

import { Field, FieldProps } from "formik";
import Select from 'react-select';
import { useCallback, useState } from "react";

interface OptionType {
   label: string;
   value: string;
}

interface CitySelectProps {
   id: string;
   label: string;
   optionsCallback: (query: string) => Promise<any>;
   showNotApplicable?: string;
   notApplicable?: boolean;
   onNotApplicableChange?: (value: boolean) => void;
}

export const CitySelect: React.FC<CitySelectProps & FieldProps> = ({
   id,
   label,
   optionsCallback,
   field,
   form,
   showNotApplicable = undefined,
   notApplicable = false,
   onNotApplicableChange,
}) => {
   const [options, setOptions] = useState<OptionType[]>([]);
   const [loading, setLoading] = useState(false);

   const handleInputChange = useCallback((inputValue: string) => {
      setLoading(true);
      optionsCallback(inputValue)
         .then((fetchedOptions) => {
            setOptions(fetchedOptions);
         })
         .finally(() => setLoading(false));
   }, [optionsCallback]);


   const handleChange = (option: OptionType | null) => {
      form.setFieldValue(field.name, option ? option.value : '');
   };

   const selectedOption = options.find(option => option.value === field.value);

   return (
      <div className="mb-4">
         <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor={id}>
            {label}
         </label>
         <Select
            id={id}
            options={options}
            value={selectedOption || null}
            onChange={handleChange}
            onInputChange={handleInputChange}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            isClearable
            isLoading={loading}
            isDisabled={notApplicable}
         />
         {showNotApplicable && (
            <div className="mt-2">
               <label className="inline-flex items-center">
                  <Field
                     type="checkbox"
                     name={`${id}NotApplicable`}
                     checked={notApplicable}
                     onChange={(e: any) => onNotApplicableChange?.(e.target.checked)}
                     className="form-checkbox"
                  />
                  <span className="ml-2 text-gray-700 text-sm font-bold">{showNotApplicable}</span>
               </label>
            </div>
         )}
      </div>
   );
};
export default CitySelect;
