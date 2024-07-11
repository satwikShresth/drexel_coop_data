import "./form.css";
import 'react-datepicker/dist/react-datepicker.css';
import { Field, FieldProps } from "formik";
import CreatableSelect from 'react-select/creatable';
import Select from 'react-select';
import React, { useCallback, useState, useEffect } from "react";

interface OptionType {
   label: string;
   value: string;
}

interface CitySelectProps {
   id: string;
   label: string;
   optionsCallback: (query: string) => Promise<OptionType[]>;
   placeholder?: string;
   noOptionsMessage?: string;
   showNotApplicable?: string;
   notApplicable?: boolean;
   onNotApplicableChange?: (value: boolean) => void;
   isCreatable?: boolean;
}

interface CreateSelectSwitchProps {
   isCreatable?: boolean;
   [key: string]: any;
}
const CreatableSelectSwitch: React.FC<CreateSelectSwitchProps> = ({ isCreatable = false, ...props }) => {
   if (isCreatable) {
      return <CreatableSelect {...props} />;
   } else {
      return <Select {...props} />;
   }
};

const AutocompleteSelect: React.FC<CitySelectProps & FieldProps> = ({
   id,
   label,
   optionsCallback,
   field,
   form,
   placeholder = "Select...",
   noOptionsMessage = "No options available...",
   onNotApplicableChange,
   showNotApplicable = undefined,
   notApplicable = false,
   isCreatable = false
}) => {
   const [options, setOptions] = useState<OptionType[]>([]);
   const [loading, setLoading] = useState(false);
   const [value, setValue] = useState<OptionType | null>();

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
      setValue(option)
   };

   useEffect(() => {
      if (field.value) {
         optionsCallback(field.value).then((fetchedOptions) => {
            setOptions(fetchedOptions);
         });
      }
   }, [field.value, optionsCallback]);



   return (
      <div className="mb-4">
         <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor={id}>
            {label}
         </label>
         <CreatableSelectSwitch
            isCreatable={isCreatable}
            id={id}
            options={options}
            onChange={handleChange}
            onInputChange={handleInputChange}
            value={value}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            isClearable
            isLoading={loading}
            isDisabled={notApplicable}
            placeholder={placeholder}
            noOptionsMessage={() => noOptionsMessage}
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

export default AutocompleteSelect;
