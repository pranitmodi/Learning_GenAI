import { useState } from "react";
import "./index.css";

const App = () => {
  const [image, setImage] = useState(null);
  const [error, setError] = useState("");
  const [value, setValue] = useState("");
  const [response, setResponse] = useState("");

  const surpriseOptions = [
    'Does the image have a whale?',
    'Does the image have puppies?',
    'is the image a meme?',
    'is the image a cat?'
  ]

  const surprise = async() => {
    const random = Math.floor(Math.random() * surpriseOptions.length);
    setValue(surpriseOptions[random]);
  }

  const analyzeImage = async() => {
    if(!image){
      setError("Error! Must have an existing image!");
      return;
    }
    if(!value){
      setError("Error! Must have a question!");
      return;
    }
    try {
      const options = {
        method: 'POST',
        body: JSON.stringify({message:value}),
        headers: {"Content-Type": "application/json"}
      }
      const response = await fetch(`http://localhost:8000/gemini`,options);
      const data = await response.text();
      console.log(data);  
      setResponse(data);
    }
    catch (err) {
      console.error(err);
      setError("An error occurred while analyzing the image");
    }
  }

  const clear = () => {
    setResponse("");
    setError("");
    setValue("");
    setImage(null);
  }

  const uploadImage = async(e) => {
    const formData = new FormData();
    formData.append('file', e.target.files[0]);
    setImage(e.target.files[0]);

    try {
      const options = {
        method: 'POST',
        body: formData
      }
      const response = await fetch('http://localhost:8000/upload', options);
      const data = await response.json();
      console.log(data);
    }
    catch (error) {
      console.error(error);
      setError("An error occurred while uploading the image");
    }
  }

  return (
    <div className="app">
      {image && <div className="img">
        <img alt="Nothing Uploaded" src={URL.createObjectURL(image)}/>
      </div>}

      {!response && <p className="extra-info">
        <span>
          <label htmlFor="files"><em>Upload an image</em></label>
          <input onChange={uploadImage} id="files" type="file" accept="image/*" hidden/>
        </span>
        to ask questions about. 
      </p>}

      <p>
        What do you want to know about the image? <br/>
        <button className="surprise" onClick={surprise} >Surprise me!</button>
      </p>

      <div className="input-container">
        <input className="askQuestion" type="text" placeholder="What is in the image..." value={value} onChange={(e) => setValue(e.target.value)}/>
        {(!response && !error) && <button onClick={analyzeImage}>Ask me</button>}
        {(response || error) && <button onClick={clear}>Clear</button>}
      </div>

      {error && <p>{error}</p>}
      {response && <p>{response}</p>}
    </div>
  );
}

export default App;
