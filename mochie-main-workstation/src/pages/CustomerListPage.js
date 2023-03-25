import React from 'react'
import ListItem from '../components/ListItem'
import us_states_list_data from '../assets/us_states_list_data'

const CustomerListPage = () => {

    return (
        <div>
            <div className='container' id ='view-customer-list'>
                { us_states_list_data.map((row,index) => (
                    <ListItem data={row}  key={index} />
                    ))}

            </div>
        </div>

    )
}

export default CustomerListPage