
import us_states_list_data from "../assets/us_states_list_data";


const CustomerDetailPage = ({customerName}) => {
  console.log("props:",{customerName})
//   let customerName = match.params.id
//   let customer = us_states_list_data.find(row => row.name === customerName)
  return(
     <div>
        <h2>On this page, a detailed customer view page will be rendered here. </h2>
        {customerName}

     </div>
  );
}

export default CustomerDetailPage;