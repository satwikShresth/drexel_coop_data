import { Field } from 'formik';
import "./form.css"
import 'nouislider/distribute/nouislider.css';

interface TextInputProps { id: string; label: string; }
export const TextInput: React.FC<TextInputProps> = ({ id, label }) => {
   return (
      <div className="mb-4">
         <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor={id}>
            {label}
         </label>
         <Field
            id={id} name={id} type="text"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
         />
      </div>
   );
};

interface SliderInputProps { id: string; label: string; min: number; max: number; step: number; value: number; onChange: (value: number) => void; unit?: string; showNotApplicable?: string; notApplicable?: boolean; onNotApplicableChange?: (value: boolean) => void; }
export const SliderInput: React.FC<SliderInputProps> = ({
   id,
   label,
   min,
   max,
   step,
   value,
   onChange,
   unit = undefined,
   showNotApplicable = undefined,
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


interface CheckboxProps { id: string; label: string; }
export const Checkbox: React.FC<CheckboxProps> = ({ id, label }) => {
   return (
      <div className="mt-2">
         <label className="inline-flex items-center">
            <Field
               type="checkbox"
               name={id}
               className="form-checkbox"
            />
            <span className="ml-2">{label}</span>
         </label>
      </div>
   );
};

interface RadioGroupProps { name: string; label: string; options: string[]; }
export const RadioGroup: React.FC<RadioGroupProps> = ({ name, label, options }) => {
   return (
      <div className="mb-4">
         <label className="block text-gray-700 text-sm font-bold mb-2">
            {label}
         </label>
         <div className="flex">
            {options.map((option) => (
               <label key={option} className="inline-flex items-center mr-4">
                  <Field
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
