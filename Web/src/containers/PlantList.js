import { connect } from 'react-redux';
import PlantListComponent from '../components/PlantList';

const mapStateToProps = (state) => {
  return {plants: state.plants};
};

const mapDispatchToProps = () => {
  return {};
};

const PlantList = connect(
    mapStateToProps,
    mapDispatchToProps
)(PlantListComponent);

export default PlantList;
