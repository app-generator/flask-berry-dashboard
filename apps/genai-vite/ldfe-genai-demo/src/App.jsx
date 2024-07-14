import { useState, useEffect } from "react";
import "./App.css";
import lens from "./assets/lens.png";
import loadingGif from "./assets/loading.gif";

function App() {
  const [prompt, updatePrompt] = useState(undefined);
  const [openaiprompt, updateOpenAIPrompt] = useState(undefined);
  const [loading, setLoading] = useState(false);
  const [openailoading, setopenaiLoading] = useState(false);
  const [answer, setAnswer] = useState(undefined);
  const [openaianswer, setopenaiAnswer] = useState(undefined);

  useEffect(() => {
    if (prompt != null && prompt.trim() === "") {
      setAnswer(undefined);
    }
  }, [prompt]);

  useEffect(() => {
    if (openaiprompt != null && openaiprompt.trim() === "") {
      setopenaiAnswer(undefined);
    }
  }, [openaiprompt]);

  const sendPrompt = async (event) => {
    if (event.key !== "Enter") {
      return;
    }

    try {
      setLoading(true);

      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      };

      console. log("request: ", requestOptions) // debug
      const res = await fetch("/api/ask", requestOptions);

      if (!res.ok) {
        throw new Error("Something went wrong");
      }

      const { message } = await res.json();
      setAnswer(message);
    } catch (err) {
      console.error(err, "err");
    } finally {
      setLoading(false);
    }
  };


  const sendOpenAIPrompt = async (event) => {
    if (event.key !== "Enter") {
      return;
    }

    try {
      setopenaiLoading(true);

      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ openaiprompt }),
      };

      console. log("request: ", requestOptions) // debug
      const res = await fetch("/api/askopenai", requestOptions);

      if (!res.ok) {
        throw new Error("Something went wrong");
      }

      const { message } = await res.json();
      setopenaiAnswer(message);
    } catch (err) {
      console.error(err, "err");
    } finally {
      setopenaiLoading(false);
    }
  };



  console. log("answer: ", answer) // debug

  return (
    <div className="app">

{/* *check* below is old bedrock div - commented out as we are now using openai for everything */}
      {/* <div className="app-container">
        
        <div className="spotlight__wrapper">
          <input
            type="text"
            className="spotlight__input"
            placeholder="Bedrock RAG - ask your question here..."
            disabled={loading}
            style={{
              backgroundImage: loading ? `url(${loadingGif})` : `url(${lens})`,
            }}
            onChange={(e) => updatePrompt(e.target.value)}
            onKeyDown={(e) => sendPrompt(e)}
          />
          <div className="spotlight__answer">{answer && <p>{answer}</p>}</div>
        </div>
      </div> */}

      <div className="app-container">
        
        <div className="spotlight__wrapper">
          <input
            type="text"
            className="spotlight__input"
            placeholder="OpenAI NLP to SQL - ask your question here..."
            wrap="soft"
            disabled={openailoading}
            style={{
              backgroundImage: openailoading ? `url(${loadingGif})` : `url(${lens})`,
            }}
            onChange={(e) => updateOpenAIPrompt(e.target.value)}
            onKeyDown={(e) => sendOpenAIPrompt(e)}
          />
          <div className="spotlight__answer">{openaianswer && <p>{openaianswer}</p>}</div>
        </div>
      </div>

    </div>
  );
}

export default App;
