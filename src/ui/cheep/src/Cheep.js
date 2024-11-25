import React, { Component } from 'react';
import Grid from './components/Grid';
import "./Cheep.css";


class Cheep extends Component {
  render() {
    return (
      <div>
        <div className="lightning">
          <div className="noisy m-4">
            <span>july. 2024</span>
            C.H.E.E.P
          </div>
          <div className="noisy m-4">
            the game
            <span>infinite connections</span>
          </div>
      </div>
        <Grid></Grid>
      </div>
    );
  }
}

export default Cheep;
