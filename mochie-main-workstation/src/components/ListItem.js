// {data} is reading the data variable that is passed down from CustomerListPage
import { Link } from "react-router-dom";

const ListItem = (props) => {
    console.log('the data is ', props.data)
    console.log ('the index is ', props.index)
    return (
        <div>
           <Link to = {`/cust_detail/${props.data.name}`}> <li>{props.data.name}</li></Link>
            <li >{props.data.abbreviation}</li>
            <li>{props.index}</li>
        </div>

    );
}

export default ListItem