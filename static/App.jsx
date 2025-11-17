const { useState } = React;

function App() {
    const [name, setName] = useState('');
    const [message, setMessage] = useState('');
    const [titleBar, setTitleBar] = useState('Make me say something');

    const postMessage = async (e) => {
        e.preventDefault();

        if (name.trim() === '' && message.trim() === '') {
            return;
        }

        const dataString = JSON.stringify({
            message: message,
            author: name
        });

        try {
            const response = await fetch('/matrix/api/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: dataString
            });

            if (response.status === 200) {
                setTitleBar('Message received, the board will refresh every 5 minutes');
                setName('');
                setMessage('');
            } else {
                setTitleBar('Something went wrong! Ooops');
                console.error('Error:', response.status);
            }
        } catch (error) {
            setTitleBar('Something went wrong! Ooops');
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <div align="center" className="top">
                <img src={window.APP_CONFIG.rcLogoUrl} alt="RC Logo" />
                <h1>RC Dynamic Display</h1>
                <h2 id="titleBar">{titleBar}</h2>

                <form onSubmit={postMessage}>
                    <input
                        type="text"
                        placeholder="Name (Optional!)"
                        style={{ width: '10%' }}
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                    <input
                        type="text"
                        style={{ width: '50%' }}
                        placeholder="Message"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                    />
                    <input type="submit" value="Say it" />
                </form>

                <img
                    src={window.APP_CONFIG.persistentJpgUrl}
                    style={{ width: '100%' }}
                    alt="Display"
                />
            </div>

            <div style={{ borderBottom: 'solid' }}></div>

            <h2>What is it?</h2>
            <p>
                The RC dynamic display is an LED dot matrix display which shows relevant
                information for those in the space, including:
            </p>
            <ul>
                <li><a href="https://www.recurse.com/calendar">Upcoming Events</a></li>
                <li><a href={window.APP_CONFIG.getMessagesUrl}>Public Messages</a></li>
                <li>Weather <a href="https://api.weather.gov">Powered by api.weather.gov</a></li>
            </ul>

            <h2>Program Me!</h2>
            <a href="https://github.com/redSlug/dynamic-display">Submit a pull request</a>

            <h2>Feedback/Content</h2>
            <p>
                You can give feedback on the project via this
                <a href="https://goo.gl/forms/qfSTRsV8FGikyNP32">Survey</a>.
            </p>
        </div>
    );
}
