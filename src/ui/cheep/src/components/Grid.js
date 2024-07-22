import React, { Component } from 'react';

class Grid extends Component {
  constructor(props) {
    super(props);
    this.state = {
        words: [],
    };
  }

  // Fetch data when the component mounts
  componentDidMount() {
    this.fetchData();
  }
  
  fetchData = async () => {
    try {
      const response = await fetch('http://localhost:8000/init');
      const data = await response.json();
      const words = data["words"];
      this.setState({ words });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  render() {
    return (
        <div className="container text-center">
            <div className="row">
                {this.state.words.map((word, index) => (
                    <button key={index} className="col">
                    {word.data}
                    </button>
                ))}
          </div>
        </div>
      );
  }
}

export default Grid;
