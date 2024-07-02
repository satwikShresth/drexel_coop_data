import "./form.css"
import 'nouislider/distribute/nouislider.css';
import 'react-datepicker/dist/react-datepicker.css'
import { Field } from "formik";

interface TextInputProps {
   id: string;
   label: string;
   [key: string]: any; 
}
const TextInput: React.FC<TextInputProps> = ({ id, label, ...rest }) => {
   return (
      <div className="mb-4">
         <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor={id}>
            {label}
         </label>
         <Field
            id={id}
            name={id}
            type="text"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            {...rest}
         />
      </div>
   );
};

 export default TextInput;
