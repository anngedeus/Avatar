import streamlit as st

st.title("Create Your Avatar with Ready Player Me")

# HTML and JavaScript for Ready Player Me integration and displaying the avatar in Model Viewer
ready_player_me_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport"
        content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Create Avatar</title>
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
            background-color: #4CAF50;
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
            height: 500px;
        }
    </style>
    <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
</head>
<body>
    <input type="button" class="custom-button" value="Open Ready Player Me" onClick="displayIframe()" />
    <p id="avatarUrl">Avatar URL:</p>

    <iframe id="frame" class="frame" allow="camera *; microphone *; clipboard-write" hidden></iframe>

    <!-- Model viewer with camera controls but no auto-rotate -->
    <model-viewer id="avatarViewer" camera-controls></model-viewer>

    <script>
        const subdomain = 'demo';  // Replace with your custom subdomain
        const frame = document.getElementById('frame');
        const viewer = document.getElementById('avatarViewer');

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
            }

            // Get user ID
            if (json.eventName === 'v1.user.set') {
                console.log(`User with ID ${json.data.id} set: ${JSON.stringify(json)}`);
            }
        }

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

# Display the Ready Player Me iframe in the Streamlit app
st.components.v1.html(ready_player_me_html, height=800)
