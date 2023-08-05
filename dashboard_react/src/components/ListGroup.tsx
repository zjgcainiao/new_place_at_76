import { MDBListGroup, MDBListGroupItem } from "mdb-react-ui-kit";

function ListGroup() {
  return (
    <>
      <h1>List</h1>
      <MDBListGroup style={{ minWidth: "22rem" }} light>
        <MDBListGroupItem active noBorders aria-current="true" className="px-3">
          Cras justo odio
        </MDBListGroupItem>
        <MDBListGroupItem noBorders className="px-3">
          Dapibus ac facilisis in
        </MDBListGroupItem>
        <MDBListGroupItem noBorders className="px-3">
          Morbi leo risus
        </MDBListGroupItem>
        <MDBListGroupItem noBorders className="px-3">
          Porta ac consectetur ac
        </MDBListGroupItem>
        <MDBListGroupItem noBorders className="px-3">
          Vestibulum at eros
        </MDBListGroupItem>
      </MDBListGroup>
    </>
  );
}

export default ListGroup;
