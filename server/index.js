const express = require('express');
const axios = require('axios');
const app = express();
const { exec } = require('child_process');
const { spawn } = require('child_process');

app.use(express.json());
let idleTimer = 0;
let defaultPrompt = 'Answer The Following: %QUESTION%';

app.post('/llama', async (req, res) => {
    const prompt = req.body.prompt;
    //print the received prompt
    serverStatus = idleTimer > 0 ? 'Server is running: ' + idleTimer : 'Server is not running';
    console.log('Received prompt: ' + prompt + ' || ' + serverStatus);
    let result = await runRequest(prompt);
    if(result === 'Server starting'){
        res.status(200).json({ message: 'Server starting' });
    }
    else if(result === 'Error making request to llama'){
        res.status(500).json({ error: 'Error making request to llama' });
    }
    else if(result === 'Error starting server'){
        res.status(500).json({ error: 'Error starting server' });
    }
    else{
        res.json(result);
    }
});
app.post('/llamapreprompt', async (req, res) => {
    let query = defaultPrompt.replace('%QUESTION%', req.body.prompt);
    //print the received prompt
    serverStatus = idleTimer > 0 ? 'Server is running: ' + idleTimer : 'Server is not running';
    console.log('Received prompt: ' + query + ' || ' + serverStatus);
    let result = await runRequest(query);
    if(result === 'Server starting'){
        res.status(200).json({ message: 'Server starting' });
    }
    else if(result === 'Error making request to llama'){
        res.status(500).json({ error: 'Error making request to llama' });
    }
    else if(result === 'Error starting server'){
        res.status(500).json({ error: 'Error starting server' });
    }
    else{
        res.json(result);
    }
});
app.post('/llamasetprompt', async (req, res) => {
    const prompt = req.body.newPrompt;
    //if no prompt is provided, return the current prompt
    if (!prompt) {
        res.json({ prompt: defaultPrompt });
    }
    else {
        const oldPromptValue = defaultPrompt;
        defaultPrompt = prompt;
        console.log('Prompt set to: ' + prompt);
        res.json({ prompt: defaultPrompt, oldPrompt: oldPromptValue});
    }
});


async function runRequest(question) {
    const data = {
        "model": "llama3",
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "stream": false
    };
    const headers = {
        'Content-Type': 'application/json'
    };
    try {
        const response = await axios.post('http://localhost:11434/api/chat', data, { headers: headers });
        idleTimer = 5;
        return response.data['message']['content'];
        //res.json(response.data['message']['content']);
    } catch (error) {
        //check if ollama_llama_server.exe is running
        //if it is not running, start the server
        //if it is running, return an error message
        const serverStatus = checkAndStartServer();
        if (serverStatus === 1) {
            return 'Server starting';
            //res.status(200).json({ message: 'Server starting' });
        }
        else if (serverStatus === 0) {
            return 'Error making request to llama';
            //res.status(500).json({ error: 'Error making request to llama' });
        }
        else {
            console.log(serverStatus);
            return 'Error starting server';
            //res.status(500).json({ error: 'Error starting server' });
        }
    }
}

function checkAndStartServer() {
    exec('tasklist', (err, stdout, stderr) => {
        if (err) {
            console.error(`exec error: ${err}`);
            return "Error getting tasklist";
        }
        // Check if 'ollama_llama_server.exe' is in the list of running tasks
        if (!stdout.includes('ollama_llama_server.exe')) {
            startServer();
            return 1;
        } else {
            // If it's already running, return an error message
            console.error('ollama_llama_server.exe is already running');
            return 0;
        }
    });
    return 1;
}
function startServer() {
    const child = spawn('ollama', ['run', 'llama3'], {
        detached: true,
        stdio: 'ignore'
    });
    child.unref();
    idleTimer = 5;
}

app.listen(3002, () => {
    console.log('Server is running on port 3002');
});
//decrament the idle timer every minute
setInterval(() => {
    if (idleTimer > 0) {
        idleTimer--;
        console.log('Server will time out in ' + idleTimer + ' minutes');
        //if the idle timer reaches 0, kill the server
        if (idleTimer === 0) {
            exec('taskkill /IM ollama_llama_server.exe /F', (err, stdout, stderr) => {
                if (err) {
                    console.error(`exec error: ${err}`);
                    return;
                }
                console.log('Server killed');
            });
        }
    }
}, 60000);