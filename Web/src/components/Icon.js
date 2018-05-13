import React, { Component } from 'react';
import '@mdi/font/css/materialdesignicons.min.css';

class Icon extends Component {
  render() {
    return <i className={"mdi mdi-" + this.props.name}/>;
  }
}

export default Icon;
