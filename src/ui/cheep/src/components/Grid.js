import React, { Component } from 'react';
import './Grid.css';
import Word from "./Word.js";

class Grid extends Component {
  constructor(props) {
    super(props);
    this.state = {
        words: [],
        categories: [],
        selection: [],
    };
  }

  // Fetch data when the component mounts
  componentDidMount() {
    this.fetchData();
  }
  
  fetchData = async () => {
    try {
      const response = await fetch('http://localhost:8000/puzzle/state/init');
      const data = await response.json();
      const words = data["words"];
      const categories = data["unsolved_categories"];
      this.setState({ words, categories });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  validateSelection = async () =>  {
    try {
        const rawResponse = await fetch('http://localhost:8000/selection', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({data: this.state.selection})
        });
        const content = await rawResponse.json();
        if (content["validation_result"]) {
          alert("Yippeeee");
        } else {
          alert("Booooooo");
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
  }

  toggleSelection(word) {
    if (this.state.selection.includes(word)) {
      const idx = this.state.selection.indexOf(word);
      this.state.selection.splice(idx, 1);
    } else {
      this.state.selection.push(word);
    }
  }

  render() {
    return (
        <div className='game-board'>
          <div className="container-fluid gap-3 text-center justify-content-md-center">
              <div className="row justify-content-lg-center">
                  {this.state.words.map((word, index) => (
                      <Word toggleSelection={this.toggleSelection.bind(this)} key={index} word={word} category={this.getCategoryForWord(word, this.state.categories)}/>
                  ))}
              </div>
              <div className='row p-2'>
                <div className='col'>
                  <button onClick={this.validateSelection} className='btn btn-outline-dark' type='submit'>Submit</button>
                </div>
              </div>
          </div>
        </div>
      );
  }
  getCategoryForWord(word, categories) {
    for (const category of categories) {
      if (category.words.map((obj) => obj.data).includes(word.data)) {
        return category;
      }
    }
  }
}

export default Grid;
