import React from 'react';
import "./coop.css"
import * as Yup from 'yup';
import { Formik, Form, Field } from 'formik';
import DatePickerInput from '../components/form/date';
import TextInput from '../components/form/text';
import CitySelect from '../components/form/city';
import SliderInput from '../components/form/slider';
import RadioGroup from '../components/form/radio';

const fetchCities = async (query: string) => {
   try {
      const response = await fetch(
         !(query)
            ? 'http://localhost:8000/uscities'
            : `http://localhost:8000/uscities?query=${query}`
      );
      if (!response.ok) {
         throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      return result.map((item: { city: string; state_id: string }) => ({
         value: `${item.city}, ${item.state_id}`,
         label: `${item.city}, ${item.state_id}`,
      }));
   } catch (error) {
      console.error('Error fetching data:', error);
      return [];
   }
};


const validationSchema = Yup.object().shape({
   companyName: Yup.string().required('Company Name is required'),
   position: Yup.string().required('Position is required'),
   salary: Yup.number().required('Salary is required').min(0, 'Salary must be greater than or equal to 0'),
   requiredHours: Yup.number().required('Required Hours are required').min(0, 'Hours must be greater than or equal to 0'),
   coopYear: Yup.number().required('Coop Year is required'),
   location: Yup.string().required('Location is required'),
   major: Yup.string().required('Major is required'),
   coopCycle: Yup.string().required('Co-op Cycle is required'),
   experience: Yup.string().required('Experience is required'),
});

interface FormValues {
   location: string | any;
   locationNotApplicable: boolean;
   companyName: string;
   position: string;
   salary: number;
   salaryNotApplicable: boolean;
   requiredHours: number;
   requiredHoursNotApplicable: boolean;
   coopYear: number;
   major: string;
   coopCycle: string;
   experience: string;
}

const CoopForm: React.FC = () => {
   const initialValues: FormValues = {
      companyName: '',
      position: '',
      salary: 15,
      salaryNotApplicable: false,
      requiredHours: 40,
      requiredHoursNotApplicable: false,
      coopYear: new Date().getFullYear(),
      location: '',
      locationNotApplicable: false,
      major: '',
      coopCycle: '',
      experience: '',
   };


   return (
      <Formik
         initialValues={initialValues}
         validationSchema={validationSchema}
         onSubmit={(values) => {
            console.log(values);
         }}
      >
         {({ values, setFieldValue }) => (
            <Form className="max-w-2xl mx-auto p-4 bg-white shadow-md rounded-md">
               <TextInput id="companyName" label="Company Name" required />

               <TextInput id="position" label="Position" required />

               <Field
                  name="location"
                  label="Location"
                  component={CitySelect}
                  id="location"
                  optionsCallback={fetchCities}
                  showNotApplicable="Remote"
                  notApplicable={values.locationNotApplicable}
                  onNotApplicableChange={(checked: any) => {
                     setFieldValue('locationNotApplicable', checked);
                     if (checked) {
                        setFieldValue('location', 'Remote');
                     }
                  }}
                  required={true}
               />

               <SliderInput
                  id="salary"
                  label="Salary"
                  min={0}
                  max={100}
                  step={1}
                  value={values.salary}
                  onChange={(value: any) => setFieldValue('salary', value)}
                  unit="$/hr"
                  showNotApplicable="Unpaid"
                  notApplicable={values.salaryNotApplicable}
                  onNotApplicableChange={(checked: any) => {
                     setFieldValue('salaryNotApplicable', checked);
                     if (checked) {
                        setFieldValue('salary', 0);
                     }
                  }}
                  required={true}
               />

               <SliderInput
                  id="requiredHours"
                  label="Required Hours"
                  min={0}
                  max={80}
                  step={1}
                  value={values.requiredHours}
                  onChange={(value: any) => setFieldValue('requiredHours', value)}
                  unit="hr"
                  required={true}
               />

               <DatePickerInput
                  id="coopYear"
                  label="Coop Year"
                  selectedDate={new Date(values.coopYear, 0, 1)}
                  onChange={(date) => {
                     if (date) {
                        setFieldValue('coopYear', date.getFullYear());
                     }
                  }}
                  required
               />

               <TextInput id="major" label="Major" required />


               <RadioGroup
                  name="coopCycle"
                  label="Co-op Cycle"
                  options={['Fall/Winter', 'Spring/Summer']}
                  required
               />

               <RadioGroup
                  name="experience"
                  label="Experience"
                  options={['1st', '2nd', '3rd']}
                  required
               />

               <button
                  type="submit"
                  className={`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline`}
               >
                  Submit
               </button>

            </Form>
         )}
      </Formik>
   );
};

export default CoopForm;
