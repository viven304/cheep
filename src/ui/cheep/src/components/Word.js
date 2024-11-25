import React, { Component } from 'react';
import './Word.css';

class Word extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { word, isActive, toggleSelection, color } = this.props;
    return (
        <button onClick={() => toggleSelection(word)} className={`tile col-lg-2 m-2 ${isActive ? 'active' : ''}`} style={{backgroundColor: color}}>
            {word.data}
        </button>
      );
    }
}

export default Word;
