
import React from 'react';
import { Formik, Form } from 'formik';
import { RadioGroup, SliderInput, TextInput } from '../components/form';

interface FormValues { companyName: string; position: string; salary: number; salaryNotApplicable: boolean; requiredHours: number; requiredHoursNotApplicable: boolean; coopYear: number; major: string; coopCycle: string; }
const CoopForm: React.FC = () => {
   const initialValues: FormValues = {
      companyName: '',
      position: '',
      salary: 50,
      salaryNotApplicable: false,
      requiredHours: 40,
      requiredHoursNotApplicable: false,
      coopYear: 2022,
      major: '',
      coopCycle: '',
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
               <TextInput id="companyName" label="Name of the company" />
               <TextInput id="position" label="Position" />

               <SliderInput
                  id="salary"
                  label="Salary"
                  min={0}
                  max={100}
                  step={1}
                  value={values.salary}
                  onChange={(value: any) => setFieldValue('salary', value)}
                  unit="$/hr"
                  showNotApplicable= "Unpaid"
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

               <SliderInput
                  id="coopYear"
                  label="Coop Year"
                  min={2015}
                  max={2030}
                  step={1}
                  value={values.coopYear}
                  onChange={(value: any) => setFieldValue('coopYear', value)}
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
