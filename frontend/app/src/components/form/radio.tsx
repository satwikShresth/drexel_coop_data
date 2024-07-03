import "./form.css"
import 'react-datepicker/dist/react-datepicker.css'

import { Field } from "formik";

interface RadioGroupProps { name: string; label: string; options: string[];[key: string]: any; }
const RadioGroup: React.FC<RadioGroupProps> = ({ name, label, options, ...rest }) => {
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
                     {...rest}
                  />
                  <span className="ml-2">{option}</span>
               </label>
            ))}
         </div>
      </div>
   );
};

export default RadioGroup;
