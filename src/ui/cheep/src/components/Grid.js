import React, { Component } from 'react';
import './Grid.css';
import Word from "./Word.js";

class Grid extends Component {
  constructor(props) {
    super(props);
    this.state = {
        words: [],
        categories: [],
        colorMap: [],
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
      const colorMap = new Array(words.length).fill(null);
      this.setState({ words, categories, colorMap });
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
          alert(`Yippeeee. It is a part of ${content["category"].name}`);
          this.colorWords();
          this.clearSelection();
        } else if (content["category"]) {
          alert(`Already tried and the answer is ${content["category"].name}`);
          this.colorWords();
          this.clearSelection();
        } else {
          alert("Booooo that's wrong");
          this.clearSelection()
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
  }

  getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  colorWords() {
    let colorForCategory = this.getRandomColor()
    this.state.selection.forEach((selection, index) => {
      const idx = this.state.words.findIndex(word => selection.data === word.data);
      if (idx >= 0) {
        const currentState = this.state;
        currentState.colorMap[idx] = colorForCategory;
        this.setState(currentState);
      }
    });
  }
  
  clearSelection() {
    const currentState = this.state;
    currentState.selection = [];
    this.setState(currentState);
  }

  toggleSelection(word) {
    if (this.state.selection.includes(word)) {
      const idx = this.state.selection.indexOf(word);
      this.state.selection.splice(idx, 1);
    } else {
      this.state.selection.push(word);
    }
  }

  wordsInGroupsOfFours() {
    const wordsInGroups = [];
    for (let i=0; i<16-1; i+=4) {
      wordsInGroups.push(this.state.words.slice(i, i+4));
    }
    return wordsInGroups;
  }

  render() {
    return (
        <div className='game-board'>
          <div className="container-fluid gap-3 text-center justify-content-md-center">
                  {this.wordsInGroupsOfFours().map((words, index_of_row) => (
                      <div key={index_of_row} className="row justify-content-lg-center">
                          {words.map((word, index_of_word) => (
                            <Word toggleSelection={this.toggleSelection.bind(this)} key={index_of_row*4 + index_of_word} word={word} category={this.getCategoryForWord(word, this.state.categories)} color={this.state.colorMap[index_of_row*4 + index_of_word]}/>
                          ))}
                      </div>
                  ))}
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
