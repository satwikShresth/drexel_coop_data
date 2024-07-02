import "./form.css"
import 'nouislider/distribute/nouislider.css';
import 'react-datepicker/dist/react-datepicker.css'

import DatePicker from "react-datepicker";

interface DatePickerInputProps {
   id: string;
   label: string;
   selectedDate: Date;
   onChange: (date: Date | null) => void;
   [key: string]: any;
}
const DatePickerInput: React.FC<DatePickerInputProps> = ({
   id,
   label,
   selectedDate,
   onChange,
}) => {
   return (
      <div className="mb-4">
         <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor={id}>
            {label}
         </label>
         <DatePicker
            id={id}
            selected={selectedDate}
            onChange={(date: any) => onChange(date)}
            showYearPicker
            dateFormat="yyyy"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
         />
      </div>
   );
};

export default DatePickerInput;
