import React, { Component } from 'react';
import './Word.css';

class Word extends Component {
  constructor(props) {
    super(props);
    this.state = {
        category: this.props.category,
        word: this.props.word,
        isActive: false,
        toggleSelection: this.props.toggleSelection,
    };
    // This binding is necessary to make `this` work in the callback    
    this.toggleActive = this.toggleActive.bind(this);
  }
  toggleActive() {
    this.state.toggleSelection(this.state.word);
    const current_state = this.state;
    current_state.isActive = !current_state.isActive;
    this.setState(current_state);
  }

  render() {
    return (
        <button onClick={this.toggleActive} className={`tile col-lg-2 m-2 ${this.state.isActive ? 'active' : ''}`} style={{backgroundColor: this.props.color}}>
            {this.state.word.data}
        </button>
      );
    }
}

export default Word;
