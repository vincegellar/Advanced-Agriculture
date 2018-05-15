import { connect } from 'react-redux';
import PlantComponent from '../components/Plant';

const mapStateToProps = (state, ownProps) => {
  return state.plants[ownProps.info.id];
};

const mapDispatchToProps = () => {
  return {};
};

const Plant = connect(
    mapStateToProps,
    mapDispatchToProps
)(PlantComponent);

export default Plant;
