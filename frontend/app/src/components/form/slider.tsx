import "./form.css"
import 'nouislider/distribute/nouislider.css';
import 'react-datepicker/dist/react-datepicker.css'

import { Field } from "formik";

interface SliderInputProps {
   id: string;
   label: string;
   min: number;
   max: number;
   step: number;
   value: number;
   onChange: (value: number) => void;
   unit?: string;
   showNotApplicable?: string;
   notApplicable?: boolean;
   onNotApplicableChange?: (value: boolean) => void;
   required?: boolean;
   [key: string]: any;
}

const SliderInput: React.FC<SliderInputProps> = ({
   id,
   label,
   min,
   max,
   step,
   value,
   onChange,
   unit = undefined,
   showNotApplicable = undefined,
   required = false,
   notApplicable = false,
   onNotApplicableChange,
}) => {
   return (
      <div className="mb-4">
         <label className="relative block text-gray-700 text-sm font-bold mb-2" htmlFor={id}>
            {label} <span className="absolute right-0 text-sm font-bold text-gray-700">{value} {unit}</span>
         </label>
         <input
            id={id}
            type="range"
            min={min}
            max={max}
            step={step}
            value={value}
            onChange={(e) => onChange(Number(e.target.value))}
            className={`slider ${notApplicable ? 'slider-disabled' : ''}`}
            disabled={notApplicable}
            required={required && !notApplicable}
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

export default SliderInput;
