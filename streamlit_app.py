import streamlit as st
import streamlit.components.v1 as components

st.title("Create Your Avatar with Ready Player Me")

ready_player_me_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <style>
        html, body, .frame {
            width: 100%;
            height: 600px;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans,
                Droid Sans, Helvetica Neue, sans-serif;
            font-size: 14px;
            border: none;
        }
        .custom-button {
            display: inline-block;
            font-size: 16px;
            padding: 12px 24px;
            color: white;
            background-color: purple;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.3s;
        }
        .custom-button:hover {
            background-color: #45a049;
            transform: scale(1.05);
        }
        .custom-button:active {
            background-color: #3e8e41;
            transform: scale(1);
        }
        model-viewer {
            width: 100%;
            height: 1600px;
            object-fit: cover;
            camera-controls;
            camera-orbit: 0deg 90deg 1.2m;  /* Closer zoom, focus on the top half */
            field-of-view: 25deg;  /* Narrow the field of view for a zoomed-in effect */
            min-camera-orbit: 0deg 90deg 1m;
            max-camera-orbit: 0deg 90deg 1.5m;
        }
        #chatbox {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            max-width: 500px;
            height: 150px;
            background-color: rgba(0, 0, 0, 0.8);
            border-radius: 10px;
            padding: 10px;
            color: white;
            display: none;  /* Initially hidden */
            flex-direction: column;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        #chatbox-header {
            font-weight: bold;
            margin-bottom: 10px;
        }
        #chat-history {
            flex-grow: 1;
            overflow-y: auto;
            margin-bottom: 10px;
            font-size: 12px;
        }
        #chat-input {
            padding: 10px;
            border: none;
            border-radius: 5px;
            width: 90%;
            font-size: 12px;
        }
    </style>
    <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
</head>
<body>
    <input type="button" class="custom-button" value="Open Ready Player Me" onClick="displayIframe()" />
    <p id="avatarUrl">Avatar URL:</p>

    <iframe id="frame" class="frame" allow="camera *; microphone *; clipboard-write" hidden></iframe>

    <!-- Model viewer with zoomed-in camera controls -->
    <model-viewer id="avatarViewer" camera-controls></model-viewer>

    <!-- Floating Chatbox (Initially hidden) -->
    <div id="chatbox">
        <div id="chatbox-header">Chat with Avatar</div>
        <div id="chat-history"></div>
        <input id="chat-input" type="text" placeholder="Type your message..." />
    </div>

    <script>
        const subdomain = 'demo';  // Replace with your custom subdomain
        const frame = document.getElementById('frame');
        const viewer = document.getElementById('avatarViewer');
        const chatInput = document.getElementById("chat-input");
        const chatHistory = document.getElementById("chat-history");
        const chatbox = document.getElementById("chatbox");

        frame.src = `https://${subdomain}.readyplayer.me/avatar?frameApi`;

        window.addEventListener('message', subscribe);
        document.addEventListener('message', subscribe);

        function subscribe(event) {
            const json = parse(event);

            if (json?.source !== 'readyplayerme') {
                return;
            }

            // Subscribe to all events sent from Ready Player Me once the frame is ready
            if (json.eventName === 'v1.frame.ready') {
                frame.contentWindow.postMessage(
                    JSON.stringify({
                        target: 'readyplayerme',
                        type: 'subscribe',
                        eventName: 'v1.**'
                    }),
                    '*'
                );
            }

            // Get avatar GLB URL
            if (json.eventName === 'v1.avatar.exported') {
                console.log(`Avatar URL: ${json.data.url}`);
                document.getElementById('avatarUrl').innerHTML = `Avatar URL: ${json.data.url}`;
                frame.hidden = true;

                // Set the GLB model URL in the Model Viewer
                viewer.src = json.data.url;

                // Show the floating chatbox after the avatar is selected
                chatbox.style.display = "flex";
            }

            // Get user ID
            if (json.eventName === 'v1.user.set') {
                console.log(`User with ID ${json.data.id} set: ${JSON.stringify(json)}`);
            }
        }

        // Handle chat input and response simulation
        chatInput.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                let message = chatInput.value;
                
                // Display user message
                chatHistory.innerHTML += `<div>Me: ${message}</div>`;
                chatInput.value = '';

                // Simulate avatar response (this is where you would add LLM integration)
                setTimeout(() => {
                    let avatarResponse = "Simulated avatar response";  // Replace with API call
                    chatHistory.innerHTML += `<div>Avatar: ${avatarResponse}</div>`;
                    chatHistory.scrollTop = chatHistory.scrollHeight;  // Auto-scroll to bottom
                }, 500);
            }
        });

        function parse(event) {
            try {
                return JSON.parse(event.data);
            } catch (error) {
                return null;
            }
        }

        function displayIframe() {
            frame.hidden = false;
        }
    </script>
</body>
</html>
"""

components.html(ready_player_me_html, height=800)
