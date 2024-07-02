import React from 'react';
import { Formik, Form, Field } from 'formik';
import { CitySelect, DatePickerInput, RadioGroup, SliderInput, TextInput } from '../components/form';

const fetchCities = async (query: string) => {
   try {
      const response = await fetch(
         !query
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

interface FormValues { location: string | any; cityNotApplicable: boolean; companyName: string; position: string; salary: number; salaryNotApplicable: boolean; requiredHours: number; requiredHoursNotApplicable: boolean; coopYear: number; major: string; coopCycle: string; experience: string; }
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
      cityNotApplicable: false,
      major: '',
      coopCycle: '',
      experience: '',
   };


   return (
      <Formik
         initialValues={initialValues}
         onSubmit={(values) => {
            console.log(values);
         }}
      >
         {({ values, setFieldValue }) => (
            <Form className="max-w-2xl mx-auto p-4 bg-white shadow-md rounded-md">
               <TextInput id="companyName" label="Company Name" />
               <TextInput id="position" label="Position" />

               <Field
                  name="location"
                  label="Location"
                  component={CitySelect}
                  id="location"
                  optionsCallback={fetchCities}
                  showNotApplicable="Remote"
                  notApplicable={values.cityNotApplicable}
                  onNotApplicableChange={(checked: any) => {
                     setFieldValue('cityNotApplicable', checked);
                     if (checked) {
                        setFieldValue('location', '');
                     }
                  }}
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
               />

               <TextInput id="major" label="Major" />

               <RadioGroup
                  name="coopCycle"
                  label="Co-op Cycle"
                  options={['Fall/Winter', 'Spring/Summer']}
               />

               <RadioGroup
                  name="experience"
                  label="Experience"
                  options={['1st', '2nd', '3rd']}
               />

               <button
                  type="submit"
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
               >
                  Submit
               </button>
            </Form>
         )}
      </Formik>
   );
};

export default CoopForm;
