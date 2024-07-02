import { RadioGroup, RangeInput, TextInput } from "../components/form";

const CoopForm: React.FC = () => {
   return (
      <div className="max-w-2xl mx-auto p-4 bg-white shadow-md rounded-md">
         <form>
            <div className="mb-4">
               <TextInput id="companyName" label="Company Name" />
               <TextInput id="position" label="Position" />
               <RangeInput id="salary" label="Salary" min={0} max={120} unit="$/hr" showNotApplicable />
               <RangeInput id="hours" label="Required hours" min={10} max={60} unit="Hours/week" />
               <RangeInput id="coopYear" label="Year" min={2023} max={2027} />
               <TextInput id="major" label="Major" />
               <RadioGroup name="coopCycle" label="Co-op Cycle" options={['Fall/Winter', 'Spring/Summer']} />
               <RadioGroup name="experience" label="Experience" options={['1st', '2nd', '3rd']} />
            </div>
         </form>
      </div>
   );
};

export default CoopForm;
