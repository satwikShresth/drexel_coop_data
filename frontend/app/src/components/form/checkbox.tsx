import "./form.css"
import 'nouislider/distribute/nouislider.css';
import 'react-datepicker/dist/react-datepicker.css'

import { Field } from "formik";

interface CheckboxProps {
   id: string;
   label: string;
   [key: string]: any;
}

const Checkbox: React.FC<CheckboxProps> = ({ id, label, ...rest }) => {
   return (
      <div className="mt-2">
         <label className="inline-flex items-center">
            <Field
               type="checkbox"
               name={id}
               className="form-checkbox"
               {...rest}
            />
            <span className="ml-2">{label}</span>
         </label>
      </div>
   );
};

export default Checkbox;
